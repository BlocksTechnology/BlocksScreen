"""Tests for updater.executor — all subprocess calls use asyncio."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from updater.executor import (
    _make_clean_env,
    _remove_broken_loose_ref,
    _run,
    apt_update,
    apt_upgrade,
    check_apt_status,
    check_git_status,
    git_checkout,
    git_clone,
    git_commits_behind,
    git_describe,
    git_fetch,
    git_get_current_branch,
    git_get_hash,
    git_has_corruption,
    git_is_dirty,
    git_pull,
    git_remote_url,
    git_repair,
    git_reset_to_hash,
    git_prune_extra_remotes,
    enable_service,
    restart_service,
    restart_service_noblock,
    run_hook,
)


def _make_proc(
    returncode: int = 0, stdout: bytes = b"", stderr: bytes = b""
) -> MagicMock:
    """Return a fake asyncio.subprocess.Process."""
    proc = MagicMock()
    proc.returncode = returncode
    proc.communicate = AsyncMock(return_value=(stdout, stderr))
    proc.kill = MagicMock()
    proc.terminate = MagicMock()
    proc.wait = AsyncMock(return_value=returncode)
    return proc


class TestMakeCleanEnv:
    def test_verify_git_terminal_prompt(self):
        result = _make_clean_env()
        assert result["GIT_TERMINAL_PROMPT"] == "0"

    def test_no_dangerous_keys(self):
        result = _make_clean_env()
        assert "LD_PRELOAD" not in result
        assert "PYTHONPATH" not in result


class TestRun:
    @pytest.mark.asyncio
    async def test_success_returns_stdout(self, tmp_path):
        proc = _make_proc(0, b"hello\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, out = await _run(["/bin/echo", "hello"], timeout=5.0, cwd=tmp_path)
        assert ok is True
        assert "hello" in out

    @pytest.mark.asyncio
    async def test_failure_returns_stderr(self, tmp_path):
        proc = _make_proc(1, b"", b"not found\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, out = await _run(["/bin/false"], timeout=5.0, cwd=tmp_path)
        assert ok is False
        assert "not found" in out

    @pytest.mark.asyncio
    async def test_timeout_terminates_then_kills(self, tmp_path):
        proc = _make_proc(0)
        proc.returncode = None  # still running when timeout fires
        # communicate times out; wait() after SIGTERM also times out → SIGKILL
        proc.communicate = AsyncMock(side_effect=asyncio.TimeoutError)
        proc.wait = AsyncMock(side_effect=[asyncio.TimeoutError, None])
        proc.pid = 1234
        with (
            patch(
                "asyncio.create_subprocess_exec",
                new_callable=AsyncMock,
                return_value=proc,
            ),
            patch("os.killpg") as killpg_mock,
            patch("os.getpgid", return_value=1234),
        ):
            ok, msg = await _run(["/bin/sleep", "999"], timeout=0.01, cwd=tmp_path)
        assert ok is False
        assert "timed out" in msg
        # Should call killpg twice: once with SIGTERM, once with SIGKILL
        assert killpg_mock.call_count == 2

    @pytest.mark.asyncio
    async def test_timeout_terminate_succeeds_no_kill(self, tmp_path):
        proc = _make_proc(0)
        proc.returncode = None  # still running when timeout fires
        # communicate times out; wait() after SIGTERM succeeds → no SIGKILL
        proc.communicate = AsyncMock(side_effect=asyncio.TimeoutError)
        proc.pid = 1234
        with (
            patch(
                "asyncio.create_subprocess_exec",
                new_callable=AsyncMock,
                return_value=proc,
            ),
            patch("os.killpg") as killpg_mock,
            patch("os.getpgid", return_value=1234),
        ):
            ok, msg = await _run(["/bin/sleep", "999"], timeout=0.01, cwd=tmp_path)
        assert ok is False
        assert "timed out" in msg
        # Should call killpg once with SIGTERM (waits successfully, no SIGKILL needed)
        assert killpg_mock.call_count == 1

    @pytest.mark.asyncio
    async def test_cancel_kills_process_and_reraises(self, tmp_path):
        proc = _make_proc(0)
        proc.returncode = None  # still running
        proc.pid = 1234

        async def hang(*_a, **_kw):
            raise asyncio.CancelledError

        proc.communicate = hang
        with (
            patch(
                "asyncio.create_subprocess_exec",
                new_callable=AsyncMock,
                return_value=proc,
            ),
            patch("os.killpg") as killpg_mock,
            patch("os.getpgid", return_value=1234),
        ):
            with pytest.raises(asyncio.CancelledError):
                await _run(["/bin/sleep", "999"], timeout=5.0, cwd=tmp_path)
        # Should call killpg once with SIGKILL on cancel
        assert killpg_mock.call_count == 1


class TestGitClone:
    @pytest.mark.asyncio
    async def test_rejects_non_https_url(self, tmp_path):
        ok, msg = await git_clone("git@github.com:x/y", tmp_path / "y")
        assert ok is False
        assert "https" in msg

    @pytest.mark.asyncio
    async def test_rejects_none_path(self):
        ok, msg = await git_clone("https://github.com/x/y", None)
        assert ok is False

    @pytest.mark.asyncio
    async def test_rejects_bad_branch(self, tmp_path):
        ok, msg = await git_clone(
            "https://github.com/x/y", tmp_path / "y", branch="../evil"
        )
        assert ok is False
        assert "branch" in msg

    @pytest.mark.asyncio
    async def test_builds_clone_argv_with_branch(self, tmp_path):
        dest = tmp_path / "y"
        with patch(
            "updater.executor._run", new_callable=AsyncMock, return_value=(True, "")
        ) as mock_run:
            ok, _ = await git_clone("https://github.com/x/y", dest, branch="main")
        assert ok is True
        argv = mock_run.call_args[0][0]
        assert argv[:2] == ["/usr/bin/git", "clone"]
        assert "--branch" in argv and "main" in argv
        assert argv[-2:] == ["https://github.com/x/y", str(dest)]


class TestGitGetHash:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        proc = _make_proc(0, b"abc1234\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            result = await git_get_hash(tmp_path)
        assert result == "abc1234"

    @pytest.mark.asyncio
    async def test_none_path_returns_empty(self):
        assert await git_get_hash(None) == ""

    @pytest.mark.asyncio
    async def test_failure_returns_empty(self, tmp_path):
        proc = _make_proc(1, b"", b"fatal: not a repo\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            result = await git_get_hash(tmp_path)
        assert result == ""


class TestGitIsDirty:
    @pytest.mark.asyncio
    async def test_dirty(self, tmp_path):
        proc = _make_proc(0, b"M modified_file.py\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_is_dirty(tmp_path) is True

    @pytest.mark.asyncio
    async def test_clean(self, tmp_path):
        proc = _make_proc(0, b"", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_is_dirty(tmp_path) is False

    @pytest.mark.asyncio
    async def test_command_failure(self, tmp_path):
        proc = _make_proc(1, b"", b"error\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_is_dirty(tmp_path) is False


class TestGitCommitsBehind:
    @pytest.mark.asyncio
    async def test_returns_count(self, tmp_path):
        proc = _make_proc(0, b"3\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_commits_behind(tmp_path) == 3

    @pytest.mark.asyncio
    async def test_failure_returns_minus_one(self, tmp_path):
        proc = _make_proc(1, b"", b"error\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_commits_behind(tmp_path) == -1


class TestGitGetCurrentBranch:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        proc = _make_proc(0, b"main\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_get_current_branch(tmp_path) == "main"

    @pytest.mark.asyncio
    async def test_failure_returns_empty(self, tmp_path):
        proc = _make_proc(1, b"", b"error\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_get_current_branch(tmp_path) == ""


class TestGitRemoteUrl:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        proc = _make_proc(0, b"https://github.com/user/repo.git\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            result = await git_remote_url(tmp_path)
        assert result == "https://github.com/user/repo.git"

    @pytest.mark.asyncio
    async def test_failure_returns_empty(self, tmp_path):
        proc = _make_proc(1, b"", b"error\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_remote_url(tmp_path) == ""


class TestGitDescribe:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        proc = _make_proc(0, b"v1.0.0\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_describe(tmp_path) == "v1.0.0"

    @pytest.mark.asyncio
    async def test_failure_returns_empty(self, tmp_path):
        proc = _make_proc(1, b"", b"no tags\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_describe(tmp_path) == ""

    @pytest.mark.asyncio
    async def test_uses_custom_ref(self, tmp_path):
        proc = _make_proc(0, b"v2.0.0\n", b"")
        exec_mock = AsyncMock(return_value=proc)
        with patch("asyncio.create_subprocess_exec", exec_mock):
            await git_describe(tmp_path, ref="origin/main")
        cmd = exec_mock.call_args.args
        assert "origin/main" in cmd


class TestGitResetToHash:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        proc = _make_proc(0, b"HEAD is now at abc1234\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, _ = await git_reset_to_hash(tmp_path, "abc1234")
        assert ok is True

    @pytest.mark.asyncio
    async def test_none_path_returns_false(self):
        ok, msg = await git_reset_to_hash(None, "abc1234")
        assert ok is False
        assert "path" in msg

    @pytest.mark.asyncio
    async def test_empty_hash_returns_false(self, tmp_path):
        ok, msg = await git_reset_to_hash(tmp_path, "")
        assert ok is False
        assert "prev_hash" in msg

    @pytest.mark.asyncio
    async def test_invalid_ref_rejected(self, tmp_path):
        ok, msg = await git_reset_to_hash(tmp_path, "'; rm -rf /")
        assert ok is False
        assert "invalid git ref" in msg

    @pytest.mark.asyncio
    async def test_valid_sha_accepted(self, tmp_path):
        proc = _make_proc(0, b"HEAD is now at abc1234\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, _ = await git_reset_to_hash(tmp_path, "abc1234f")
        assert ok is True

    @pytest.mark.asyncio
    async def test_valid_origin_ref_accepted(self, tmp_path):
        proc = _make_proc(0, b"HEAD is now at deadbeef\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, _ = await git_reset_to_hash(tmp_path, "origin/main")
        assert ok is True

    @pytest.mark.asyncio
    async def test_valid_tag_accepted(self, tmp_path):
        proc = _make_proc(0, b"HEAD is now at deadbeef\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, _ = await git_reset_to_hash(tmp_path, "v1.2.3")
        assert ok is True


class TestGitResetToHashEnv:
    def test_make_clean_env_excludes_dbus(self):
        import os

        with patch.dict(
            os.environ, {"DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus"}
        ):
            env = _make_clean_env()
        assert "DBUS_SESSION_BUS_ADDRESS" not in env

    def test_make_clean_env_excludes_xdg_runtime(self):
        import os

        with patch.dict(os.environ, {"XDG_RUNTIME_DIR": "/run/user/1000"}):
            env = _make_clean_env()
        assert "XDG_RUNTIME_DIR" not in env


class TestGitPruneExtraRemotes:
    @pytest.mark.asyncio
    async def test_removes_extra_remote(self, tmp_path):
        list_proc = _make_proc(0, b"origin\neddy\n", b"")
        remove_proc = _make_proc(0, b"", b"")
        exec_mock = AsyncMock(side_effect=[list_proc, remove_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            await git_prune_extra_remotes(tmp_path)
        assert exec_mock.call_count == 2

    @pytest.mark.asyncio
    async def test_keeps_only_origin(self, tmp_path):
        list_proc = _make_proc(0, b"origin\n", b"")
        exec_mock = AsyncMock(return_value=list_proc)
        with patch("asyncio.create_subprocess_exec", exec_mock):
            await git_prune_extra_remotes(tmp_path)
        assert exec_mock.call_count == 1

    @pytest.mark.asyncio
    async def test_list_failure_is_noop(self, tmp_path):
        list_proc = _make_proc(1, b"", b"error\n")
        exec_mock = AsyncMock(return_value=list_proc)
        with patch("asyncio.create_subprocess_exec", exec_mock):
            await git_prune_extra_remotes(tmp_path)
        assert exec_mock.call_count == 1


class TestGitFetch:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        # git remote (for prune) returns only origin, then fetch succeeds
        prune_proc = _make_proc(0, b"origin\n", b"")
        fetch_proc = _make_proc(0, b"From https://github.com\n", b"")
        exec_mock = AsyncMock(side_effect=[prune_proc, fetch_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, _ = await git_fetch(tmp_path)
        assert ok is True

    @pytest.mark.asyncio
    async def test_none_path_returns_false(self):
        ok, _ = await git_fetch(None)
        assert ok is False

    @pytest.mark.asyncio
    async def test_fetch_failure(self, tmp_path):
        prune_proc = _make_proc(0, b"origin\n", b"")
        fail_proc = _make_proc(1, b"", b"network error\n")
        exec_mock = AsyncMock(side_effect=[prune_proc, fail_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, out = await git_fetch(tmp_path)
        assert ok is False
        assert "network error" in out

    @pytest.mark.asyncio
    async def test_repairs_broken_ref_then_retries(self, tmp_path):
        broken = (
            b"error: cannot lock ref 'refs/remotes/origin/fix/x': unable to "
            b"resolve reference 'refs/remotes/origin/fix/x': reference broken\n"
        )
        prune_proc = _make_proc(0, b"origin\n", b"")
        fail_proc = _make_proc(1, b"", broken)
        del_proc = _make_proc(0, b"", b"")
        retry_proc = _make_proc(0, b"From https://github.com\n", b"")
        exec_mock = AsyncMock(side_effect=[prune_proc, fail_proc, del_proc, retry_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, _ = await git_fetch(tmp_path)
        assert ok is True
        argvs = [call.args for call in exec_mock.call_args_list]
        assert any(
            "update-ref" in a and "refs/remotes/origin/fix/x" in a for a in argvs
        )

    @pytest.mark.asyncio
    async def test_broken_ref_unparseable_does_not_retry(self, tmp_path):
        prune_proc = _make_proc(0, b"origin\n", b"")
        fail_proc = _make_proc(1, b"", b"fatal: reference broken somewhere\n")
        exec_mock = AsyncMock(side_effect=[prune_proc, fail_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, _ = await git_fetch(tmp_path)
        assert ok is False
        assert exec_mock.call_count == 2

    def test_remove_broken_loose_ref_deletes_file_and_reflog(self, tmp_path):
        ref = "refs/remotes/origin/fix/x"
        (tmp_path / ".git" / ref).parent.mkdir(parents=True)
        (tmp_path / ".git" / ref).write_text("")
        (tmp_path / ".git" / "logs" / ref).parent.mkdir(parents=True)
        (tmp_path / ".git" / "logs" / ref).write_text("")
        _remove_broken_loose_ref(tmp_path, ref)
        assert not (tmp_path / ".git" / ref).exists()
        assert not (tmp_path / ".git" / "logs" / ref).exists()


class TestGitPull:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        proc = _make_proc(0, b"Already up to date.\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, _ = await git_pull(tmp_path)
        assert ok is True

    @pytest.mark.asyncio
    async def test_failure(self, tmp_path):
        proc = _make_proc(1, b"", b"conflict\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, out = await git_pull(tmp_path)
        assert ok is False
        assert "conflict" in out

    @pytest.mark.asyncio
    async def test_none_path_returns_false(self):
        ok, _ = await git_pull(None)
        assert ok is False


class TestGitCheckout:
    @pytest.mark.asyncio
    async def test_success(self, tmp_path):
        branch_proc = _make_proc(0, b"main\n", b"")
        checkout_proc = _make_proc(0, b"Switched to branch 'develop'\n", b"")
        exec_mock = AsyncMock(side_effect=[branch_proc, checkout_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, _ = await git_checkout(tmp_path, "develop")
        assert ok is True

    @pytest.mark.asyncio
    async def test_already_on_branch(self, tmp_path):
        branch_proc = _make_proc(0, b"develop\n", b"")
        exec_mock = AsyncMock(return_value=branch_proc)
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, msg = await git_checkout(tmp_path, "develop")
        assert ok is True
        assert "already" in msg
        assert exec_mock.call_count == 1

    @pytest.mark.asyncio
    async def test_invalid_branch_name_rejected(self, tmp_path):
        ok, msg = await git_checkout(tmp_path, "bad branch!")
        assert ok is False
        assert "invalid" in msg

    @pytest.mark.asyncio
    async def test_empty_branch_rejected(self, tmp_path):
        ok, _ = await git_checkout(tmp_path, "")
        assert ok is False

    @pytest.mark.asyncio
    async def test_failure(self, tmp_path):
        branch_proc = _make_proc(0, b"main\n", b"")
        checkout_proc = _make_proc(1, b"", b"branch not found\n")
        exec_mock = AsyncMock(side_effect=[branch_proc, checkout_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, out = await git_checkout(tmp_path, "missing-branch")
        assert ok is False
        assert "branch not found" in out


class TestAptUpdate:
    @pytest.mark.asyncio
    async def test_success(self):
        proc = _make_proc(0, b"Hit:1 http://archive\n", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, _ = await apt_update()
        assert ok is True

    @pytest.mark.asyncio
    async def test_failure(self):
        proc = _make_proc(1, b"", b"network error\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, out = await apt_update()
        assert ok is False
        assert "network error" in out


class TestAptUpgrade:
    @pytest.mark.asyncio
    async def test_success(self):
        proc = _make_proc(0, b"0 upgraded\n", b"")
        with patch(
            "updater.executor._list_upgradable_packages", return_value=(True, ["pkg1"])
        ):
            with patch(
                "asyncio.create_subprocess_exec",
                new_callable=AsyncMock,
                return_value=proc,
            ):
                ok, _ = await apt_upgrade()
        assert ok is True

    @pytest.mark.asyncio
    async def test_failure(self):
        proc = _make_proc(1, b"", b"dpkg error\n")
        with patch(
            "updater.executor._list_upgradable_packages", return_value=(True, ["pkg1"])
        ):
            with patch(
                "asyncio.create_subprocess_exec",
                new_callable=AsyncMock,
                return_value=proc,
            ):
                ok, out = await apt_upgrade()
        assert ok is False
        assert "dpkg error" in out

    @pytest.mark.asyncio
    async def test_unattended_hardening_options_present(self):
        proc = _make_proc(0, b"", b"")
        exec_mock = AsyncMock(return_value=proc)
        with (
            patch(
                "updater.executor._list_upgradable_packages",
                return_value=(True, ["pkg1"]),
            ),
            patch("asyncio.create_subprocess_exec", exec_mock),
        ):
            await apt_upgrade()
        argv = [str(a) for a in exec_mock.call_args[0]]
        assert "DPkg::Lock::Timeout=60" in argv  # wait for the lock, never fail fast
        assert "Dpkg::Options::=--force-confold" in argv  # no conffile prompt
        env = exec_mock.call_args[1]["env"]
        assert env["DEBIAN_FRONTEND"] == "noninteractive"
        assert env["NEEDRESTART_MODE"] == "a"

    @pytest.mark.asyncio
    async def test_list_failure(self):
        with patch(
            "updater.executor._list_upgradable_packages", return_value=(False, [])
        ):
            ok, out = await apt_upgrade()
        assert ok is False
        assert "list" in out

    @pytest.mark.asyncio
    async def test_no_packages(self):
        with patch(
            "updater.executor._list_upgradable_packages", return_value=(True, [])
        ):
            ok, out = await apt_upgrade()
        assert ok is True
        assert "no packages" in out


class TestRestartService:
    @pytest.mark.asyncio
    async def test_success(self):
        proc = _make_proc(0, b"", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, _ = await restart_service("klipper.service")
        assert ok is True

    @pytest.mark.asyncio
    async def test_invalid_name_rejected(self):
        ok, msg = await restart_service("Service.notservice")
        assert ok is False
        assert "invalid" in msg

    @pytest.mark.asyncio
    async def test_none_name_returns_false(self):
        ok, _ = await restart_service(None)
        assert ok is False

    @pytest.mark.asyncio
    async def test_restart_fail_then_reset_failed_and_retry_succeeds(self):
        # restart fails (e.g. start-limit), reset-failed runs, retry restart succeeds.
        fail = _make_proc(1, b"", b"start request repeated too quickly\n")
        reset = _make_proc(0, b"", b"")
        retry = _make_proc(0, b"", b"")
        exec_mock = AsyncMock(side_effect=[fail, reset, retry])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, msg = await restart_service("klipper.service")
        assert ok is True
        assert "reset-failed" in msg
        assert exec_mock.call_count == 3  # restart, reset-failed, restart

    @pytest.mark.asyncio
    async def test_restart_fail_then_retry_also_fails(self):
        fail = _make_proc(1, b"", b"boom\n")
        reset = _make_proc(0, b"", b"")
        retry_fail = _make_proc(1, b"", b"still failing\n")
        exec_mock = AsyncMock(side_effect=[fail, reset, retry_fail])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            ok, _ = await restart_service("klipper.service")
        assert ok is False

    @pytest.mark.asyncio
    async def test_no_systemctl_kill_used(self):
        # Regression: the systemctl-kill fallback must be gone (it needed a
        # password and did not clear a start-limit). reset-failed is used instead.
        procs = [
            _make_proc(1, b"", b"boom\n"),  # restart fails
            _make_proc(0, b"", b""),  # reset-failed
            _make_proc(0, b"", b""),  # retry restart
        ]
        calls: list[list[str]] = []

        async def _spawn(*args, **kwargs):
            calls.append([str(a) for a in args])
            return procs[len(calls) - 1]

        with patch("asyncio.create_subprocess_exec", side_effect=_spawn):
            await restart_service("klipper.service")
        flat = [tok for c in calls for tok in c]
        assert "kill" not in flat
        assert "reset-failed" in flat


class TestRestartServiceNoblock:
    @pytest.mark.asyncio
    async def test_uses_no_block_flag(self):
        calls: list[list[str]] = []

        async def _spawn(*args, **kwargs):
            calls.append([str(a) for a in args])
            return _make_proc(0, b"", b"")

        with patch("asyncio.create_subprocess_exec", side_effect=_spawn):
            ok, _ = await restart_service_noblock("BlocksScreen.service")
        assert ok is True
        flat = [tok for c in calls for tok in c]
        assert "--no-block" in flat and "restart" in flat
        assert "BlocksScreen.service" in flat

    @pytest.mark.asyncio
    async def test_invalid_name_rejected(self):
        ok, _ = await restart_service_noblock("bad name")
        assert ok is False


class TestCheckGitStatus:
    @pytest.mark.asyncio
    async def test_missing_path_returns_error(self, tmp_path):
        result = await check_git_status("klipper", None)
        assert result.error is not None

    @pytest.mark.asyncio
    async def test_nonexistent_path_returns_error(self, tmp_path):
        result = await check_git_status("klipper", tmp_path / "nonexistent")
        assert result.error is not None

    @pytest.mark.asyncio
    async def test_fetch_failure_returns_error(self, tmp_path):
        # git remote (prune) succeeds with origin only, then git fetch fails
        prune_proc = _make_proc(0, b"origin\n", b"")
        fetch_proc = _make_proc(1, b"", b"network error\n")
        exec_mock = AsyncMock(side_effect=[prune_proc, fetch_proc])
        with patch("asyncio.create_subprocess_exec", exec_mock):
            result = await check_git_status("klipper", tmp_path)
        assert result.error is not None

    @pytest.mark.asyncio
    async def test_success_skip_fetch(self, tmp_path):
        # skip_fetch=True: hash + current_branch + commits_behind + url + dirty + describe x2
        procs = [
            _make_proc(0, b"abc1234\n", b""),  # git_get_hash
            _make_proc(0, b"main\n", b""),  # git_get_current_branch
            _make_proc(0, b"2\n", b""),  # git_commits_behind
            _make_proc(0, b"https://github.com/x/y\n", b""),  # git_remote_url
            _make_proc(0, b"", b""),  # git_is_dirty (clean)
            _make_proc(0, b"v1.0\n", b""),  # git_describe current
            _make_proc(0, b"v1.2\n", b""),  # git_describe remote
        ]
        exec_mock = AsyncMock(side_effect=procs)
        with patch("asyncio.create_subprocess_exec", exec_mock):
            result = await check_git_status("klipper", tmp_path, skip_fetch=True)
        assert result.error is None
        assert result.current_hash == "abc1234"
        assert result.commits_behind == 2
        assert result.has_local_changes is False


class TestCheckAptStatus:
    @pytest.mark.asyncio
    async def test_success(self):
        proc = _make_proc(0, b"", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            result = await check_apt_status()
        assert result.name == "system"
        assert result.kind == "apt"

    @pytest.mark.asyncio
    async def test_failed_count_sets_error(self, tmp_path, monkeypatch):
        # A failed upgradable-package count (-1) must surface as an error so the
        # UI renders "status check failed" instead of a phantom update.
        monkeypatch.setenv("HOME", str(tmp_path))
        with patch(
            "updater.executor._count_apt_upgradable",
            new_callable=AsyncMock,
            return_value=-1,
        ):
            result = await check_apt_status()
        assert result.kind == "apt"
        assert result.packages_upgradable == -1
        assert result.error == "apt status check failed"


class TestCorruption:
    @pytest.mark.asyncio
    async def test_has_corruption_true_on_fsck_failure(self):
        proc = _make_proc(1, b"", b"error: object file ... is empty\n")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_has_corruption(Path("/x")) is True

    @pytest.mark.asyncio
    async def test_has_corruption_false_when_clean(self):
        proc = _make_proc(0, b"", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await git_has_corruption(Path("/x")) is False

    @pytest.mark.asyncio
    async def test_has_corruption_from_hint_skips_fsck(self):
        # The fetch error alone proves corruption even if fsck would miss it;
        # no subprocess should be spawned when the hint already matches.
        exec_mock = AsyncMock()
        with patch("asyncio.create_subprocess_exec", exec_mock):
            result = await git_has_corruption(
                Path("/x"), hint="error: object file ... is empty"
            )
        assert result is True
        exec_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_repair_deletes_empty_objects_then_fetches(self, tmp_path):
        objdir = tmp_path / ".git" / "objects" / "5d"
        objdir.mkdir(parents=True)
        (objdir / "deadbeef").write_bytes(b"")  # 0-byte = corrupt
        (objdir / "good").write_bytes(b"x")  # non-empty kept
        with (
            patch(
                "updater.executor.git_fetch",
                new_callable=AsyncMock,
                return_value=(True, ""),
            ),
            patch(
                "updater.executor.git_has_corruption",
                new_callable=AsyncMock,
                return_value=False,
            ),
        ):
            ok, _msg = await git_repair(tmp_path)
        assert ok is True
        assert not (objdir / "deadbeef").exists()
        assert (objdir / "good").exists()

    @pytest.mark.asyncio
    async def test_repair_fails_when_still_corrupt(self, tmp_path):
        # Empty-object prune + fetch left it corrupt and fsck found nothing to
        # quarantine: repair gives up rather than looping.
        (tmp_path / ".git" / "objects").mkdir(parents=True)
        with (
            patch(
                "updater.executor.git_fetch",
                new_callable=AsyncMock,
                return_value=(True, ""),
            ),
            patch(
                "updater.executor.git_has_corruption",
                new_callable=AsyncMock,
                return_value=True,
            ),
            patch(
                "updater.executor._quarantine_corrupt_objects",
                new_callable=AsyncMock,
                return_value=0,
            ),
        ):
            ok, msg = await git_repair(tmp_path)
        assert ok is False
        assert "still corrupt" in msg

    @pytest.mark.asyncio
    async def test_repair_quarantines_non_empty_corrupt_then_succeeds(self, tmp_path):
        # Non-empty corrupt loose object: first verify fails, quarantine moves it,
        # the re-fetch re-downloads it, and the second verify is clean.
        (tmp_path / ".git" / "objects").mkdir(parents=True)
        with (
            patch(
                "updater.executor.git_fetch",
                new_callable=AsyncMock,
                return_value=(True, ""),
            ),
            patch(
                "updater.executor.git_has_corruption",
                new_callable=AsyncMock,
                side_effect=[True, False],
            ),
            patch(
                "updater.executor._quarantine_corrupt_objects",
                new_callable=AsyncMock,
                return_value=1,
            ) as mock_quarantine,
        ):
            ok, msg = await git_repair(tmp_path)
        assert ok is True
        assert "1 corrupt" in msg
        mock_quarantine.assert_awaited_once_with(tmp_path)

    @pytest.mark.asyncio
    async def test_quarantine_moves_fsck_flagged_object(self, tmp_path):
        objdir = tmp_path / ".git" / "objects" / "ab"
        objdir.mkdir(parents=True)
        name = "a" * 38
        (objdir / name).write_bytes(b"garbage")  # non-empty but corrupt
        from updater.executor import _quarantine_corrupt_objects

        proc = _make_proc(
            1, b"", f"error: object file .git/objects/ab/{name} is corrupt\n".encode()
        )
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            moved = await _quarantine_corrupt_objects(tmp_path)
        assert moved == 1
        assert not (objdir / name).exists()
        assert (
            tmp_path / ".git" / "objects" / "objects-corrupt" / "ab" / name
        ).exists()

    @pytest.mark.asyncio
    async def test_quarantine_noop_when_fsck_clean(self, tmp_path):
        (tmp_path / ".git" / "objects").mkdir(parents=True)
        from updater.executor import _quarantine_corrupt_objects

        proc = _make_proc(0, b"", b"")
        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            assert await _quarantine_corrupt_objects(tmp_path) == 0


class TestSelfUpdateEnvStamp:
    def test_clean_env_marks_self_update(self):
        from updater.executor import _make_clean_env

        env = _make_clean_env()
        assert env["BS_UPDATER_SELF_UPDATE"] == "1"
        assert env["BS_UPDATER_RESTART_SENTINEL"].endswith("updater-restart-needed")


class TestVerifyUpdaterImportable:
    @pytest.mark.asyncio
    async def test_returns_false_for_missing_path(self):
        from updater.executor import verify_updater_importable

        assert await verify_updater_importable(Path("/no/such/path")) is False

    @pytest.mark.asyncio
    async def test_true_when_import_subprocess_succeeds(self, tmp_path):
        from updater.executor import verify_updater_importable

        with patch(
            "updater.executor._run", new=AsyncMock(return_value=(True, ""))
        ) as mock_run:
            assert await verify_updater_importable(tmp_path) is True
        assert mock_run.await_args.kwargs["cwd"] == tmp_path

    @pytest.mark.asyncio
    async def test_false_when_import_subprocess_fails(self, tmp_path):
        from updater.executor import verify_updater_importable

        with patch(
            "updater.executor._run",
            new=AsyncMock(return_value=(False, "ModuleNotFoundError: sdbus")),
        ):
            assert await verify_updater_importable(tmp_path) is False


class TestRunHook:
    """run_hook: resolve under hooks dir, pass timeout, reject traversal."""

    @pytest.mark.asyncio
    async def test_run_hook_passes_timeout(self, tmp_path, monkeypatch):
        import updater.executor as ex

        monkeypatch.setattr(ex, "_HOOKS_DIR", tmp_path)
        (tmp_path / "comp.sh").write_text("#!/bin/bash\nexit 0\n")
        with patch.object(ex, "_run", new=AsyncMock(return_value=(True, ""))) as run:
            await run_hook("comp", tmp_path, "newh", "prevh", timeout=600.0)
        assert run.await_args.kwargs["timeout"] == 600.0
        assert run.await_args.kwargs["env"]["NEW_HASH"] == "newh"

    @pytest.mark.asyncio
    async def test_run_hook_default_timeout(self, tmp_path, monkeypatch):
        import updater.executor as ex

        monkeypatch.setattr(ex, "_HOOKS_DIR", tmp_path)
        (tmp_path / "comp.sh").write_text("#!/bin/bash\nexit 0\n")
        with patch.object(ex, "_run", new=AsyncMock(return_value=(True, ""))) as run:
            await run_hook("comp", tmp_path, "n", "p")
        assert run.await_args.kwargs["timeout"] == 60.0

    @pytest.mark.asyncio
    async def test_hook_path_traversal_rejected(self, tmp_path, monkeypatch):
        import updater.executor as ex

        monkeypatch.setattr(ex, "_HOOKS_DIR", tmp_path)
        ok, msg = await run_hook("../../etc/passwd", tmp_path, "n", "p")
        assert ok is False
        assert "escapes" in msg


class TestEnableService:
    """enable_service: validate name, build the sudo systemctl enable argv."""

    @pytest.mark.asyncio
    async def test_enables_valid_service(self):
        with patch(
            "updater.executor._run", new=AsyncMock(return_value=(True, ""))
        ) as run:
            ok, _ = await enable_service("Spoolman.service")
        assert ok is True
        argv = run.await_args.args[0]
        assert argv[-2:] == ["enable", "Spoolman.service"]

    @pytest.mark.asyncio
    async def test_rejects_invalid_name(self):
        ok, msg = await enable_service("evil; rm -rf /")
        assert ok is False
        assert "invalid" in msg

    @pytest.mark.asyncio
    async def test_none_name(self):
        ok, _ = await enable_service(None)
        assert ok is False
