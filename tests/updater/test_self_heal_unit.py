import asyncio
import time
from pathlib import Path
from unittest.mock import patch

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

    def test_write_state_is_atomic_via_temp_file(self, tmp_path: Path):
        svc = UpdateService()
        svc._state_path = tmp_path / "state.json"
        data = {"test": {"key": "value"}}
        ok = svc._write_state(data)
        assert ok
        assert svc._state_path.exists()
        assert svc._read_state() == data


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
                    "golden": "original_golden",
                    "fast_attempt": 2,
                }
            }
            svc._write_state(state_before)

            with patch("updater.service.get_service_nrestarts") as mock_nrestarts:
                mock_nrestarts.return_value = 8
                ok = await svc.bless_healthy("BlocksScreen", "a" * 40)

            assert ok
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["golden"] == "original_golden"
            assert state_after["BlocksScreen"]["last_good"] == "a" * 40

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


class TestNRestartsTracking:
    def test_nrestarts_sample_ring_init_on_daemon_start(self):
        svc = UpdateService()
        assert not hasattr(svc, "_nrestarts_samples") or svc._nrestarts_samples == {}

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

    def test_rung2_forward_heals_to_origin_main_ref(self, tmp_path: Path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 1}})
            with (
                patch("updater.service.git_fetch") as m_fetch,
                patch("updater.service.git_ref_hash") as m_ref,
                patch("updater.service.git_reset_to_hash") as m_reset,
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
            assert m_reset.call_args[0][1] == "origin/main"
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
    def test_forward_heal_skips_when_not_in_fallback(self, tmp_path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 0}})
            with patch("updater.service.git_fetch") as m_fetch:
                ok = await svc._forward_heal_once()
            assert not ok
            m_fetch.assert_not_called()

        asyncio.run(run_test())

    def test_forward_heal_skips_already_failed_tip(self, tmp_path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state(
                {
                    "BlocksScreen": {
                        "prev_hash": "old",
                        "fast_attempt": 3,
                        "last_failed_remote": "b" * 40,
                    }
                }
            )
            with (
                patch("updater.service.git_fetch") as m_fetch,
                patch("updater.service.git_ref_hash") as m_ref,
                patch("updater.service.git_reset_to_hash") as m_reset,
            ):
                m_fetch.return_value = (True, "")
                m_ref.return_value = "b" * 40
                ok = await svc._forward_heal_once()
            assert not ok
            m_reset.assert_not_called()

        asyncio.run(run_test())

    def test_forward_heal_upgrades_on_new_tip(self, tmp_path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state(
                {
                    "BlocksScreen": {
                        "prev_hash": "old",
                        "fast_attempt": 3,
                        "last_failed_remote": "b" * 40,
                    }
                }
            )
            with (
                patch("updater.service.git_fetch") as m_fetch,
                patch("updater.service.git_ref_hash") as m_ref,
                patch("updater.service.git_reset_to_hash") as m_reset,
                patch("updater.service.get_service_nrestarts") as m_nr,
                patch.object(svc, "_restart_ui_service") as m_restart,
            ):
                m_fetch.return_value = (True, "")
                m_ref.return_value = "c" * 40
                m_reset.return_value = (True, "")
                m_nr.return_value = 0
                m_restart.return_value = True
                ok = await svc._forward_heal_once()
            assert ok
            state_after = svc._read_state()
            assert state_after["BlocksScreen"]["fast_attempt"] == 0
            assert state_after["BlocksScreen"]["last_failed_remote"] == "c" * 40

        asyncio.run(run_test())

    def test_forward_heal_offline_skips(self, tmp_path):
        async def run_test():
            svc = UpdateService()
            svc._state_path = tmp_path / "state.json"
            svc._write_state({"BlocksScreen": {"prev_hash": "old", "fast_attempt": 3}})
            with (
                patch("updater.service.git_fetch") as m_fetch,
                patch("updater.service.git_reset_to_hash") as m_reset,
            ):
                m_fetch.return_value = (False, "network")
                ok = await svc._forward_heal_once()
            assert not ok
            m_reset.assert_not_called()

        asyncio.run(run_test())


class TestNRestartsReader:
    def test_get_service_nrestarts_parses_value(self):
        from types import SimpleNamespace

        with patch("updater.service.subprocess.run") as m_run:
            m_run.return_value = SimpleNamespace(stdout="7\n")
            assert updater_service.get_service_nrestarts("BlocksScreen.service") == 7

    def test_get_service_nrestarts_non_numeric_returns_zero(self):
        from types import SimpleNamespace

        with patch("updater.service.subprocess.run") as m_run:
            m_run.return_value = SimpleNamespace(stdout="[not set]\n")
            assert updater_service.get_service_nrestarts("BlocksScreen.service") == 0

    def test_get_service_nrestarts_subprocess_error_returns_zero(self):
        with patch("updater.service.subprocess.run", side_effect=OSError):
            assert updater_service.get_service_nrestarts("BlocksScreen.service") == 0
