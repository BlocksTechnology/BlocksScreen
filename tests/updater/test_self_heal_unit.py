import asyncio
import os
import time
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

import updater.service as updater_service
from updater.service import UpdateService


@pytest.fixture(autouse=True)
def _isolate_state(tmp_path_factory, monkeypatch):
    state_dir = tmp_path_factory.mktemp("state")
    state_path = state_dir / "updater_state.json"
    monkeypatch.setattr(updater_service, "_STATE_PATH", state_path)
    monkeypatch.setattr(
        updater_service, "_FAULT_MARKER_PATH", state_dir / "selfheal_fault.json"
    )


@pytest.fixture
def no_head(monkeypatch):
    """The first crash-loop rung reads HEAD; keep it off the real install tree."""
    monkeypatch.setattr(updater_service, "git_get_hash", AsyncMock(return_value=""))


class TestStateFields:
    def test_state_with_new_fields_persists_atomically(self, tmp_path: Path):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        data = {
            "BlocksScreen": {
                "prev_hash": "abc123",
                "last_good": "def456",
                "golden": "ghi789",
                "last_failed_remote": "jkl012",
                "fast_attempt": 1,
                "nrestarts_baseline": 5,
            }
        }
        ok = svc._write_state(data)
        assert ok
        loaded = svc._read_state()
        assert loaded["BlocksScreen"]["last_good"] == "def456"
        assert loaded["BlocksScreen"]["golden"] == "ghi789"
        assert loaded["BlocksScreen"]["last_failed_remote"] == "jkl012"
        assert loaded["BlocksScreen"]["fast_attempt"] == 1
        assert loaded["BlocksScreen"]["nrestarts_baseline"] == 5

    def test_read_state_with_missing_fields_returns_defaults(self):
        svc = UpdateService()
        svc._state_path = Path("/nonexistent/state.json")
        state = svc._read_state()
        assert state == {}

    def test_read_state_skips_non_dict_entries(self, tmp_path: Path):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        svc._state_path.write_text('{"ok": {"a": 1}, "bad": 3}')
        assert svc._read_state() == {"ok": {"a": 1}}

    def test_write_state_is_atomic_via_temp_file(self, tmp_path: Path):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        data = {"test": {"key": "value"}}
        ok = svc._write_state(data)
        assert ok
        assert svc._state_path.exists()
        assert svc._read_state() == data

    def test_failed_write_leaves_no_temp(self, tmp_path: Path):
        svc = UpdateService()
        svc._state_path = tmp_path / "state" / "state.json"
        with patch.object(Path, "replace", side_effect=OSError("EIO")):
            assert svc._write_state({"a": {}}) is False
        assert list(svc._state_path.parent.iterdir()) == []

    def test_sweep_removes_only_stale_temps(self, tmp_path: Path):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        svc._inflight_path = tmp_path / "inflight.json"
        old = tmp_path / ".updater_state_old"
        fresh = tmp_path / ".updater_inflight_fresh"
        old.write_text("{")
        fresh.write_text("{")
        stale = time.time() - updater_service._STALE_TEMP_S - 60
        os.utime(old, (stale, stale))
        svc._sweep_stale_temps()
        assert not old.exists() and fresh.exists()

    @pytest.mark.parametrize("raw", [b"", b"\x00" * 64, b'{"a": {', b"[1]"])
    def test_corrupt_state_kept_once_and_defaults(self, tmp_path: Path, raw, caplog):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        svc._state_path.write_bytes(raw)
        assert svc._read_state() == {}
        assert svc._read_state() == {}
        assert (tmp_path / "state.json.corrupt").read_bytes() == raw
        assert sum("corrupt" in r.message for r in caplog.records) == 1


class TestBlessHealthy:
    def test_bless_healthy_sets_last_good_and_clears_counter(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "old_hash",
                    "last_good": "old_good",
                    "golden": "golden_hash",
                    "fast_attempt": 3,
                }
            }
            svc._write_state(state_before)

            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 10
                ok = await svc.bless_healthy("BlocksScreen", "a" * 40)

            assert ok
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["last_good"] == "a" * 40
            assert state_after["BlocksScreen"]["fast_attempt"] == 0
            assert state_after["BlocksScreen"]["nrestarts_baseline"] == 10

        asyncio.run(run_test())

    def test_bless_healthy_seeds_golden_on_first_bless(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "old_hash",
                }
            }
            svc._write_state(state_before)

            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 5
                ok = await svc.bless_healthy("BlocksScreen", "a" * 40)

            assert ok
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["golden"] == "a" * 40

        asyncio.run(run_test())

    def test_bless_healthy_does_not_overwrite_golden(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "old_hash",
                    "golden": "c" * 40,
                    "fast_attempt": 2,
                }
            }
            svc._write_state(state_before)

            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 8
                ok = await svc.bless_healthy("BlocksScreen", "a" * 40)

            assert ok
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["golden"] == "c" * 40
            assert state_after["BlocksScreen"]["last_good"] == "a" * 40

        asyncio.run(run_test())

    def test_golden_advances_after_repeated_blesses(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"golden": "c" * 40}})
            goldens = []
            with patch("updater.service.get_service_nrestarts", return_value=0):
                for h in ["a", "b", "b", "a", "a", "a"]:
                    await svc.bless_healthy("BlocksScreen", h * 40)
                    goldens.append(svc._read_state()["BlocksScreen"]["golden"][0])
            assert goldens == ["c", "c", "c", "c", "c", "a"]

        asyncio.run(run_test())

    def test_bless_forgets_only_its_own_bad_commit(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._bad_commit_path.write_text("b" * 40 + "\n")
            with patch("updater.service.get_service_nrestarts", return_value=0):
                await svc.bless_healthy("BlocksScreen", "a" * 40)
                assert svc._read_bad_commit() == "b" * 40
                await svc.bless_healthy("BlocksScreen", "b" * 40)
            assert svc._read_bad_commit() == ""

        asyncio.run(run_test())

    def test_bless_healthy_clears_nrestarts_sample_ring(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._nrestarts_samples = {
                "BlocksScreen": [(time.monotonic(), 5), (time.monotonic(), 7)]
            }

            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 10
                ok = await svc.bless_healthy("BlocksScreen", "a" * 40)

            assert ok
            assert svc._nrestarts_samples.get("BlocksScreen", []) == []

        asyncio.run(run_test())

    def test_bless_healthy_with_invalid_component_returns_false(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            ok = await svc.bless_healthy("NonExistent", "a" * 40)
            assert not ok

        asyncio.run(run_test())

    def test_bless_healthy_requires_valid_git_hash_format(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 5
                ok = await svc.bless_healthy("BlocksScreen", "not_a_hash")
            assert not ok

        asyncio.run(run_test())

    def test_bless_healthy_writes_atomically_on_power_cut_resilience(self, tmp_path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {"BlocksScreen": {"prev_hash": "abc", "fast_attempt": 2}}
            svc._write_state(state_before)

            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 7
                with patch.object(
                    svc, "_write_state", wraps=svc._write_state
                ) as mock_write:
                    await svc.bless_healthy("BlocksScreen", "a" * 40)
                    mock_write.assert_called_once()
                    written_data = mock_write.call_args[0][0]
                    assert written_data["BlocksScreen"]["last_good"] == "a" * 40
                    assert written_data["BlocksScreen"]["nrestarts_baseline"] == 7
                    assert written_data["BlocksScreen"]["fast_attempt"] == 0

        asyncio.run(run_test())


class TestReconcileWithNewFields:
    def test_reconcile_persists_dropped_non_dict_entries(self, tmp_path: Path, caplog):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        svc._state_path.write_text('{"ok": {"a": 1}, "bad": 3}')
        with caplog.at_level("WARNING"):
            asyncio.run(svc.reconcile())
        assert svc._read_state_file() == {"ok": {"a": 1}}
        assert "bad" in caplog.text

    def test_reconcile_clamps_fast_attempt_to_0_3(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "abc123",
                    "fast_attempt": 5,
                }
            }
            svc._write_state(state_before)

            await svc.reconcile()

            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["fast_attempt"] == 3

        asyncio.run(run_test())

    def test_reconcile_drops_corrupt_last_good_hash(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "abc123",
                    "last_good": "not_a_valid_hash",
                }
            }
            svc._write_state(state_before)

            await svc.reconcile()

            state_after = svc._read_state()
            assert "last_good" not in state_after["BlocksScreen"]

        asyncio.run(run_test())

    def test_reconcile_drops_corrupt_golden_hash(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "abc123",
                    "golden": "incomplete",
                }
            }
            svc._write_state(state_before)

            await svc.reconcile()

            state_after = svc._read_state()
            assert "golden" not in state_after["BlocksScreen"]

        asyncio.run(run_test())

    def test_reconcile_drops_corrupt_last_failed_remote(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "abc123",
                    "last_failed_remote": "bad_hash",
                }
            }
            svc._write_state(state_before)

            await svc.reconcile()

            state_after = svc._read_state()
            assert "last_failed_remote" not in state_after["BlocksScreen"]

        asyncio.run(run_test())

    def test_reconcile_preserves_valid_hashes(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            valid_hash = "a" * 40
            state_before = {
                "BlocksScreen": {
                    "prev_hash": valid_hash,
                    "last_good": valid_hash,
                    "golden": valid_hash,
                    "last_failed_remote": valid_hash,
                    "fast_attempt": 2,
                    "nrestarts_baseline": 5,
                }
            }
            svc._write_state(state_before)

            await svc.reconcile()

            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["last_good"] == valid_hash
            assert state_after["BlocksScreen"]["golden"] == valid_hash
            assert state_after["BlocksScreen"]["last_failed_remote"] == valid_hash
            assert state_after["BlocksScreen"]["fast_attempt"] == 2
            assert state_after["BlocksScreen"]["nrestarts_baseline"] == 5

        asyncio.run(run_test())


class TestStaleDaemonFlag:
    @pytest.mark.parametrize(
        ("loaded", "flagged"), [("old", True), ("disk", False), ("", False)]
    )
    def test_flags_restart_only_when_loaded_code_differs(
        self, tmp_path: Path, monkeypatch, loaded: str, flagged: bool
    ):
        hash_file = tmp_path / "updater-code-hash"
        sentinel = tmp_path / "updater-restart-needed"
        hash_file.write_text(loaded + "\n")
        monkeypatch.setattr(updater_service, "code_hash_path", lambda: hash_file)
        monkeypatch.setattr(updater_service, "restart_sentinel_path", lambda: sentinel)
        monkeypatch.setattr(updater_service, "code_hash", lambda: "disk")
        UpdateService()._flag_stale_daemon()
        assert sentinel.exists() is flagged
        if flagged:
            assert sentinel.read_text() == "code\n"

    def test_missing_hash_file_is_a_no_op(self, tmp_path: Path, monkeypatch):
        sentinel = tmp_path / "updater-restart-needed"
        monkeypatch.setattr(
            updater_service, "code_hash_path", lambda: tmp_path / "absent"
        )
        monkeypatch.setattr(updater_service, "restart_sentinel_path", lambda: sentinel)
        UpdateService()._flag_stale_daemon()
        assert not sentinel.exists()

    def test_reconcile_applies_the_flagged_restart(self, tmp_path: Path, monkeypatch):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        applied = AsyncMock()
        monkeypatch.setattr(svc, "_reconcile_locked", AsyncMock())
        monkeypatch.setattr(svc, "_apply_deferred_restart", applied)
        assert asyncio.run(svc.reconcile())
        applied.assert_awaited_once()


class TestNRestartsTracking:
    def test_nrestarts_sample_ring_init_on_daemon_start(self):
        svc = UpdateService()
        assert not hasattr(svc, "_nrestarts_samples") or svc._nrestarts_samples == {}

    def test_read_state_drops_malformed_entry(self, tmp_path: Path):
        """A non-dict entry must not reach callers that do comp.get() (daemon start)."""
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        svc._state_path.write_text('{"x": "bad", "y": {"nrestarts_baseline": 3}}')
        assert svc._read_state() == {"y": {"nrestarts_baseline": 3}}
        svc._prime_nrestarts_sample_ring()
        assert svc._nrestarts_samples["y"][0][1] == 3

    def test_nrestarts_sample_ring_primed_from_baseline(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state = {
                "BlocksScreen": {
                    "prev_hash": "abc123",
                    "nrestarts_baseline": 10,
                }
            }
            svc._write_state(state)

            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 10
                svc._prime_nrestarts_sample_ring()

            if "BlocksScreen" in svc._nrestarts_samples:
                samples = svc._nrestarts_samples["BlocksScreen"]
                if samples:
                    _, nrestarts = samples[0]
                    assert nrestarts == 10

        asyncio.run(run_test())

    def test_nrestarts_trailing_window_detects_5_in_180s(self):
        svc = UpdateService()
        svc._nrestarts_samples = {"BlocksScreen": []}
        now = time.monotonic()
        svc._nrestarts_samples["BlocksScreen"] = [
            (now - 170, 10),
            (now - 120, 12),
            (now - 60, 14),
            (now, 15),
        ]

        detected = svc._check_crash_loop("BlocksScreen", 15)
        assert detected

    def test_nrestarts_trailing_window_ignores_old_samples(self):
        svc = UpdateService()
        svc._nrestarts_samples = {"BlocksScreen": []}
        now = time.monotonic()
        svc._nrestarts_samples["BlocksScreen"] = [
            (now - 200, 10),
            (now - 190, 11),
            (now, 12),
        ]

        detected = svc._check_crash_loop("BlocksScreen", 12)
        assert not detected

    def test_fresh_device_starts_tracking_without_baseline(self):
        svc = UpdateService()
        assert "BlocksScreen" not in svc._nrestarts_samples
        assert not svc._check_crash_loop("BlocksScreen", 3)  # first sight: no trip
        assert svc._nrestarts_samples["BlocksScreen"]  # but now tracking
        assert svc._check_crash_loop("BlocksScreen", 8)  # +5 within window: trips

    def test_nrestarts_sliding_window_only_counts_delta_in_window(self):
        svc = UpdateService()
        svc._nrestarts_samples = {"BlocksScreen": []}
        now = time.monotonic()
        svc._nrestarts_samples["BlocksScreen"] = [
            (now - 200, 5),
            (now - 50, 7),
            (now, 9),
        ]

        detected = svc._check_crash_loop("BlocksScreen", 9)
        assert not detected


class TestRecoveryLadder:
    def test_run_recovery_rung_1_resets_to_last_good(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "old",
                    "last_good": "a" * 40,
                    "fast_attempt": 0,
                }
            }
            svc._write_state(state_before)

            with patch("updater.service.git_reset_to_hash") as mock_reset:
                mock_reset.return_value = (True, "")
                with patch.object(svc, "_restart_ui_service") as mock_restart:
                    mock_restart.return_value = True
                    ok = await svc.run_recovery_rung("BlocksScreen", 1)

            assert ok
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["fast_attempt"] == 1

        asyncio.run(run_test())

    def test_run_recovery_rung_counter_saturates_at_3(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {
                "BlocksScreen": {
                    "prev_hash": "old",
                    "golden": "a" * 40,
                    "fast_attempt": 3,
                }
            }
            svc._write_state(state_before)

            with patch("updater.service.git_reset_to_hash") as mock_reset:
                mock_reset.return_value = (True, "")
                with patch.object(svc, "_restart_ui_service") as mock_restart:
                    mock_restart.return_value = True
                    ok = await svc.run_recovery_rung("BlocksScreen", 10)

            assert ok
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["fast_attempt"] == 3

        asyncio.run(run_test())

    def test_run_recovery_rung_skips_when_no_last_good(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            state_before = {"BlocksScreen": {"prev_hash": "old"}}
            svc._write_state(state_before)

            ok = await svc.run_recovery_rung("BlocksScreen", 1)
            assert not ok

        asyncio.run(run_test())

    def test_run_recovery_rung_with_unknown_component_fails(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            ok = await svc.run_recovery_rung("Unknown", 1)
            assert not ok

        asyncio.run(run_test())

    def test_fresh_device_rung1_skip_still_advances_counter(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old"}})
            ok = await svc.run_recovery_rung("BlocksScreen", 1)
            assert not ok
            assert svc._read_state()["BlocksScreen"]["fast_attempt"] == 1

        asyncio.run(run_test())

    def test_rung2_heals_to_own_branch_ref(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            ui = next(c for c in svc._components if c.name == "BlocksScreen")
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 1}})
            with (
                patch("updater.service.git_fetch") as m_fetch,
                patch("updater.service.git_ref_hash") as m_ref,
                patch("updater.service.git_reset_to_hash") as m_reset,
                patch("updater.service.git_tree_has_path", return_value=True),
                patch.object(svc, "_restart_ui_service") as m_restart,
            ):
                m_fetch.return_value = (True, "")
                m_ref.return_value = "b" * 40
                m_reset.return_value = (True, "")
                m_restart.return_value = True
                ok = await svc.run_recovery_rung("BlocksScreen", 2)
            assert ok
            assert m_fetch.call_count == 1
            assert (
                len(m_fetch.call_args[0]) == 1
            )  # path only, no bad "origin" positional
            # Reset to the resolved SHA, never the movable ref name.
            assert m_ref.call_args[0][1] == f"origin/{ui.branch}"
            assert m_reset.call_args[0][1] == "b" * 40
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["last_failed_remote"] == "b" * 40
            assert state_after["BlocksScreen"]["fast_attempt"] == 2

        asyncio.run(run_test())

    def test_rung2_records_failed_tip_even_if_restart_fails(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 1}})
            with (
                patch("updater.service.git_fetch") as m_fetch,
                patch("updater.service.git_ref_hash") as m_ref,
                patch("updater.service.git_reset_to_hash") as m_reset,
                patch("updater.service.git_tree_has_path", return_value=True),
                patch.object(svc, "_restart_ui_service") as m_restart,
            ):
                m_fetch.return_value = (True, "")
                m_ref.return_value = "b" * 40
                m_reset.return_value = (True, "")
                m_restart.return_value = False  # tip fails to boot
                ok = await svc.run_recovery_rung("BlocksScreen", 2)
            assert not ok
            # last_failed_remote must persist so forward-heal never retries this bad tip.
            assert svc._read_state()["BlocksScreen"]["last_failed_remote"] == "b" * 40

        asyncio.run(run_test())

    @pytest.mark.parametrize("why", ["bad", "pinned"])
    def test_rung2_skips_crashed_tip_and_pins(self, tmp_path: Path, why: str):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"fast_attempt": 1}})
            ui = next(c for c in svc._components if c.name == "BlocksScreen")
            if why == "bad":
                svc._bad_commit_path.write_text("b" * 40 + "\n")
            else:
                ui.version = "c" * 40
            with (
                patch("updater.service.git_fetch", return_value=(True, "")),
                patch("updater.service.git_ref_hash", return_value="b" * 40),
                patch("updater.service.git_tree_has_path", return_value=True),
                patch("updater.service.git_reset_to_hash") as m_reset,
            ):
                ok = await svc.run_recovery_rung("BlocksScreen", 2)
            assert not ok
            m_reset.assert_not_called()

        asyncio.run(run_test())

    def test_rung2_offline_fetch_does_not_reset(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old"}})
            with (
                patch("updater.service.git_fetch") as m_fetch,
                patch("updater.service.git_reset_to_hash") as m_reset,
            ):
                m_fetch.return_value = (False, "network")
                ok = await svc.run_recovery_rung("BlocksScreen", 2)
            assert not ok
            m_reset.assert_not_called()

        asyncio.run(run_test())


class TestSupervisor:
    @pytest.mark.usefixtures("no_head")
    def test_handle_crash_loop_runs_next_rung(self, tmp_path, monkeypatch):
        monkeypatch.setattr(updater_service, "_RECOVERY_SETTLE_S", 0)

        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 0}})
            with (
                patch("updater.service.get_service_nrestarts") as m_nr,
                patch.object(svc, "run_recovery_rung") as m_rung,
            ):
                m_nr.return_value = 12
                m_rung.return_value = True
                await svc._handle_crash_loop(12)
            m_rung.assert_called_once_with("BlocksScreen", 1)

        asyncio.run(run_test())

    @pytest.mark.parametrize(
        ("head", "recorded"), [("b" * 40, True), ("a" * 40, False)]
    )
    def test_first_rung_records_unblessed_head(self, tmp_path, head, recorded):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"last_good": "a" * 40}})
            with (
                patch("updater.service._RECOVERY_SETTLE_S", 0),
                patch("updater.service.get_service_nrestarts", return_value=0),
                patch("updater.service.git_get_hash", return_value=head),
                patch.object(svc, "run_recovery_rung", return_value=True),
            ):
                await svc._handle_crash_loop(6)
            assert svc._read_bad_commit() == (head if recorded else "")

        asyncio.run(run_test())

    def test_crash_loop_waits_for_forward_heal_update(self, tmp_path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._forward_healing = True
            with patch.object(svc, "run_recovery_rung") as m_rung:
                await svc._handle_crash_loop(6)
            m_rung.assert_not_called()

        asyncio.run(run_test())

    def test_handle_crash_loop_saturates_and_marks_fault(self, tmp_path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 3}})
            with (
                patch("updater.service.get_service_nrestarts") as m_nr,
                patch.object(svc, "run_recovery_rung") as m_rung,
            ):
                m_nr.return_value = 20
                m_rung.return_value = True
                await svc._handle_crash_loop(20)
            m_rung.assert_not_called()
            assert svc._fault_marker_path.exists()

        asyncio.run(run_test())


class TestForwardHeal:
    def _svc(self, tmp_path: Path, **comp: object) -> UpdateService:
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        svc._write_state({"BlocksScreen": {"fast_attempt": 3} | comp})
        return svc

    def _target(self, svc: UpdateService, tip: str = "c" * 40) -> str:
        with (
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_ref_hash", return_value=tip),
            patch("updater.service.git_tree_has_path", return_value=True),
        ):
            return asyncio.run(svc.forward_heal_target())

    def test_new_tip_is_a_target(self, tmp_path):
        assert self._target(self._svc(tmp_path)) == "c" * 40

    def test_waits_while_printing(self, tmp_path, printing):
        printing.return_value = True
        assert self._target(self._svc(tmp_path)) == ""

    def test_skips_when_not_in_fallback(self, tmp_path):
        assert self._target(self._svc(tmp_path, fast_attempt=1)) == ""

    def test_skips_already_attempted_tip(self, tmp_path):
        assert self._target(self._svc(tmp_path, last_failed_remote="c" * 40)) == ""

    def test_skips_crash_looped_tip(self, tmp_path):
        svc = self._svc(tmp_path)
        svc._bad_commit_path.write_text("c" * 40 + "\n")
        assert self._target(svc) == ""

    def test_skips_pinned_version(self, tmp_path):
        svc = self._svc(tmp_path)
        next(c for c in svc._components if c.name == "BlocksScreen").version = "d" * 40
        assert self._target(svc) == ""

    def test_offline_skips(self, tmp_path):
        svc = self._svc(tmp_path)
        with patch("updater.service.git_fetch", return_value=(False, "network")):
            assert asyncio.run(svc.forward_heal_target()) == ""

    @pytest.mark.parametrize("ok", [True, False])
    def test_heal_runs_the_update_path(self, tmp_path, ok):
        svc = self._svc(tmp_path)
        seen: list[bool] = []

        async def update(_name: str) -> bool:
            seen.append(svc._forward_healing)
            return ok

        with (
            patch.object(svc, "update_component", side_effect=update),
            patch("updater.service.get_service_nrestarts", return_value=0),
        ):
            assert asyncio.run(svc.forward_heal("c" * 40)) is ok
        after = svc._read_state()["BlocksScreen"]
        assert seen == [True] and not svc._forward_healing
        assert after["last_failed_remote"] == "c" * 40
        assert after["fast_attempt"] == (0 if ok else 3)

    def test_heal_skipped_once_blessed(self, tmp_path):
        svc = self._svc(tmp_path, fast_attempt=0)
        with patch.object(svc, "update_component") as m_update:
            assert not asyncio.run(svc.forward_heal("c" * 40))
        m_update.assert_not_called()


class TestNRestartsReader:
    def test_get_service_nrestarts_parses_value(self):
        async def run_test():
            with patch("updater.service._run") as m_run:
                m_run.return_value = (True, "7\n")
                got = await updater_service.get_service_nrestarts(
                    "BlocksScreen.service"
                )
            assert got == 7

        asyncio.run(run_test())

    def test_get_service_nrestarts_non_numeric_returns_zero(self):
        async def run_test():
            with patch("updater.service._run") as m_run:
                m_run.return_value = (True, "[not set]\n")
                got = await updater_service.get_service_nrestarts(
                    "BlocksScreen.service"
                )
            assert got == 0

        asyncio.run(run_test())

    def test_get_service_nrestarts_failed_call_returns_zero(self):
        async def run_test():
            with patch("updater.service._run") as m_run:
                m_run.return_value = (False, "boom")
                got = await updater_service.get_service_nrestarts(
                    "BlocksScreen.service"
                )
            assert got == 0

        asyncio.run(run_test())


class TestStateConcurrency:
    """A bless that lands while a recovery/forward-heal is mid git-reset must not be lost."""

    def test_bless_during_rung1_is_not_clobbered(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state(
                {
                    "BlocksScreen": {
                        "last_good": "a" * 40,
                        "golden": "a" * 40,
                        "fast_attempt": 1,
                    }
                }
            )
            entered = asyncio.Event()
            release = asyncio.Event()

            async def slow_reset(_path, _ref):
                entered.set()
                await release.wait()
                return (True, "")

            new_hash = "b" * 40
            with (
                patch("updater.service.git_reset_to_hash", side_effect=slow_reset),
                patch("updater.service.get_service_nrestarts", return_value=0),
                patch.object(svc, "_restart_ui_service", return_value=True),
            ):
                rung = asyncio.create_task(svc.run_recovery_rung("BlocksScreen", 1))
                await entered.wait()
                await svc.bless_healthy("BlocksScreen", new_hash)
                release.set()
                await rung

            after = svc._read_state()["BlocksScreen"]
            assert after["last_good"] == new_hash
            assert after["fast_attempt"] == 0

        asyncio.run(run_test())

    def test_bless_during_forward_heal_is_not_clobbered(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"golden": "a" * 40, "fast_attempt": 2}})
            new_hash = "b" * 40

            async def update(_name: str) -> bool:
                await svc.bless_healthy("BlocksScreen", new_hash)
                return True

            with (
                patch.object(svc, "update_component", side_effect=update),
                patch("updater.service.get_service_nrestarts", return_value=0),
            ):
                await svc.forward_heal("c" * 40)

            after = svc._read_state()["BlocksScreen"]
            assert after["last_good"] == new_hash
            assert after["last_failed_remote"] == "c" * 40

        asyncio.run(run_test())


class TestCorruptionHardening:
    """A corrupt/tampered state file must never crash the supervisor or brick self-heal."""

    def test_reconcile_drops_non_dict_component_entry(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state(
                {"BlocksScreen": "not-a-dict", "klipper": {"last_good": "a" * 40}}
            )
            await svc._reconcile_self_heal_state()
            state = svc._read_state()
            assert "BlocksScreen" not in state
            assert state["klipper"]["last_good"] == "a" * 40

        asyncio.run(run_test())

    @pytest.mark.usefixtures("no_head")
    def test_handle_crash_loop_tolerates_non_dict_entry(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": "not-a-dict"})
            with (
                patch("updater.service.get_service_nrestarts", return_value=0),
                patch("updater.service._RECOVERY_SETTLE_S", 0),
                patch.object(svc, "run_recovery_rung", return_value=True),
            ):
                await svc._handle_crash_loop(6)  # must not raise

        asyncio.run(run_test())

    def test_bless_coerces_non_dict_component_entry(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": "not-a-dict"})
            with patch("updater.service.get_service_nrestarts", return_value=0):
                ok = await svc.bless_healthy("BlocksScreen", "b" * 40)  # must not raise
            assert ok
            comp = svc._read_state()["BlocksScreen"]
            assert comp["last_good"] == "b" * 40
            assert comp["fast_attempt"] == 0

        asyncio.run(run_test())

    def test_bless_repairs_invalid_golden(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"golden": "xyz", "last_good": 123}})
            with patch("updater.service.get_service_nrestarts", return_value=0):
                await svc.bless_healthy("BlocksScreen", "b" * 40)
            comp = svc._read_state()["BlocksScreen"]
            assert comp["golden"] == "b" * 40  # invalid golden repaired
            assert comp["last_good"] == "b" * 40

        asyncio.run(run_test())

    @pytest.mark.usefixtures("no_head")
    def test_handle_crash_loop_tolerates_non_int_fast_attempt(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"fast_attempt": "three"}})
            with (
                patch("updater.service.get_service_nrestarts", return_value=0),
                patch("updater.service._RECOVERY_SETTLE_S", 0),
                patch.object(svc, "run_recovery_rung", return_value=True) as m_rung,
            ):
                await svc._handle_crash_loop(6)  # must not raise
                m_rung.assert_awaited_once_with("BlocksScreen", 1)

        asyncio.run(run_test())

    def test_run_recovery_rung_survives_corrupt_state_with_failed_write(self, tmp_path):
        """Compound fault (updater_stress.py): a corrupt non-dict entry plus a failed
        counter-write leaves the re-read state corrupt, so the rung must guard before
        .get on it instead of crashing with AttributeError."""

        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": "not-a-dict"})
            with patch.object(svc, "_write_state", return_value=False):
                ok = await svc.run_recovery_rung("BlocksScreen", 1)  # must not raise
            assert not ok

        asyncio.run(run_test())

    def test_reconcile_locked_survives_corrupt_state_and_failed_repair(self, tmp_path):
        """Boot heal (updater_stress.py): a corrupt non-dict entry plus an unreadable
        HEAD and a failed git_repair must not crash _reconcile_locked."""

        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            repo = tmp_path / "repo"
            repo.mkdir()  # or the heal-loop short-circuits on not path.exists()
            ui = next(c for c in svc._components if c.name == "BlocksScreen")
            ui.path = repo
            svc._write_state({"BlocksScreen": "not-a-dict"})
            with (
                patch("updater.service.git_get_hash", return_value=""),
                patch(
                    "updater.service.git_repair", return_value=(False, "repair fail")
                ),
                patch.object(UpdateService, "_reclone_component", return_value=False),
            ):
                await svc._reconcile_locked()  # must not raise
            assert "BlocksScreen" not in svc._read_state()  # entry sanitized away

        asyncio.run(run_test())


class TestDiskFullRecovery:
    """Rung 0: purge bytecode, reclaim, and never reset the tree on a full disk."""

    def _svc(self, tmp_path: Path) -> UpdateService:
        from updater.models import ComponentConfig

        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        svc._components = [
            ComponentConfig(name="BlocksScreen", kind="git", path=tmp_path, order=99)
        ]
        return svc

    def test_full_disk_skips_git_rungs(self, tmp_path, disk):
        disk.free.return_value = 50.0

        async def run_test():
            svc = self._svc(tmp_path)
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 0}})
            with patch.object(svc, "run_recovery_rung") as m_rung:
                await svc._handle_crash_loop(12)
            m_rung.assert_not_called()
            disk.reclaim.assert_awaited_once_with(tmp_path)
            assert disk.purge.call_count == 2

        asyncio.run(run_test())

    @pytest.mark.usefixtures("no_head")
    def test_space_ok_purges_then_runs_rung(self, tmp_path, disk, monkeypatch):
        monkeypatch.setattr(updater_service, "_RECOVERY_SETTLE_S", 0)

        async def run_test():
            svc = self._svc(tmp_path)
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 0}})
            with (
                patch("updater.service.get_service_nrestarts", return_value=12),
                patch.object(svc, "run_recovery_rung", return_value=True) as m_rung,
            ):
                await svc._handle_crash_loop(12)
            m_rung.assert_called_once_with("BlocksScreen", 1)
            disk.purge.assert_any_call(tmp_path / "BlocksScreen")
            disk.reclaim.assert_not_awaited()

        asyncio.run(run_test())
