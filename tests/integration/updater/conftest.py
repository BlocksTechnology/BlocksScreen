"""Updater integration harness: real git, state files, locking and D-Bus layer.

Only the root-owned edges are faked (systemctl, sudo, apt, dpkg, pip, klippy.sock).
Remotes are local bare repos reached through an https:// insteadOf rewrite, so
clone/fetch/ls-remote run for real against URLs that pass the https-only checks.
"""

import asyncio
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
REMOTE_BASE = "https://git.test/"


class _FakeDbusBase:
    """Real Python base class so inheritance does not raise TypeError."""

    def __init__(self, *a, **kw) -> None:
        pass

    def __init_subclass__(cls, **kw) -> None:
        super().__init_subclass__()


@pytest.fixture(scope="module", autouse=True)
def mock_sdbus():
    """Swap sdbus for a stub and force a fresh updater.dbus_service import."""
    mock = MagicMock()
    mock.DbusInterfaceCommonAsync = _FakeDbusBase
    mock.dbus_signal_async = lambda *a, **kw: lambda fn: fn
    mock.dbus_method_async = lambda *a, **kw: lambda fn: fn
    with pytest.MonkeyPatch.context() as mp:
        for key in ("sdbus", "updater", "updater.dbus_service"):
            mp.delitem(sys.modules, key, raising=False)
        mp.setitem(sys.modules, "sdbus", mock)
        yield mock


def _script(path: Path, body: str) -> Path:
    """Write an executable bash script."""
    path.write_text("#!/bin/bash\n" + body)
    path.chmod(0o755)
    return path


_SYSTEMCTL = """\
echo "systemctl $*" >>"{state}/calls.log"
unit="${{!#}}"
case "$1" in
  is-active) [ -e "{state}/inactive-$unit" ] && exit 3; exit 0 ;;
  show)
    if [ "$2" = "--property=LoadState" ]; then
      if [ -e "{state}/missing-$unit" ]; then echo not-found; else echo loaded; fi
    elif [[ " $* " == *" ActiveState "* ]]; then
      for u in "${{@:2}}"; do
        case "$u" in -*|ActiveState) continue ;; esac
        if [ -e "{state}/inactive-$u" ]; then echo inactive; else echo active; fi
        echo
      done
    else
      echo 0
    fi
    exit 0 ;;
  restart)
    if [ -e "{state}/fail-restart-$unit" ]; then
      echo "Job for $unit failed" >&2
      exit 1
    fi
    exit 0 ;;
  *) exit 0 ;;
esac
"""

# Only our fakes run as "root": a hook's bare `sudo cp` into /etc is denied, as on a box.
_SUDO = """\
echo "sudo $*" >>"{state}/calls.log"
case "$1" in
  "{bin}"/*) exec "$@" ;;
  *) echo "sudo: not allowed" >&2; exit 1 ;;
esac
"""

_APT = """\
echo "apt $*" >>"{state}/calls.log"
if [ "$1" = "list" ]; then
  echo "Listing..."
  [ -e "{state}/upgradable" ] && cat "{state}/upgradable"
fi
exit 0
"""

_LOGGED = 'echo "{name} $*" >>"{state}/calls.log"\nexit 0\n'


class Signal:
    """Stand-in for an sdbus signal: records every emit in a shared log."""

    def __init__(self, name: str, log: list) -> None:
        self._name = name
        self._log = log

    def emit(self, args: tuple) -> None:
        """Record (signal name, args)."""
        self._log.append((self._name, args))


class Recorder:
    """ProgressCallback that keeps every call, in order."""

    def __init__(self) -> None:
        self.events: list[tuple] = []

    def on_step(self, name: str, step: int, total: int) -> None:
        """Record a progress step."""
        self.events.append(("on_step", name, step, total))

    def on_component_done(self, name: str, success: bool) -> None:
        """Record a component outcome."""
        self.events.append(("on_component_done", name, success))

    def on_error(self, name: str, reason: str) -> None:
        """Record an error."""
        self.events.append(("on_error", name, reason))

    def on_rollback(self, name: str, success: bool) -> None:
        """Record a rollback."""
        self.events.append(("on_rollback", name, success))

    def on_recover(self, name: str, success: bool) -> None:
        """Record a recover."""
        self.events.append(("on_recover", name, success))

    def of(self, method: str) -> list[tuple]:
        """Arguments of every call to one callback method."""
        return [e[1:] for e in self.events if e[0] == method]


class Remote:
    """A bare origin plus a scratch worktree used to author upstream commits."""

    def __init__(self, harness: "Harness", name: str) -> None:
        self.name = name
        self.url = f"{REMOTE_BASE}{name}.git"
        self._h = harness
        self.bare = harness.remotes / f"{name}.git"
        self.work = harness.root / "authoring" / name
        harness.git("init", "-q", "--bare", "--initial-branch=master", str(self.bare))
        harness.git("init", "-q", "--initial-branch=master", str(self.work))
        harness.git("remote", "add", "origin", str(self.bare), cwd=self.work)

    def commit(
        self,
        files: Mapping[str, str | None],
        msg: str = "change",
        branch: str = "master",
    ) -> str:
        """Write (or delete, for None) files, commit on branch, push; return the sha."""
        h = self._h
        # symbolic-ref works on the unborn initial branch, where switch would fail.
        if h.git("symbolic-ref", "--short", "HEAD", cwd=self.work) != branch:
            known = h.git("branch", "--format=%(refname:short)", cwd=self.work)
            create = [] if branch in known.splitlines() else ["-c"]
            h.git("switch", "-q", *create, branch, cwd=self.work)
        for rel, content in files.items():
            target = self.work / rel
            if content is None:
                target.unlink()
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        h.git("add", "-A", cwd=self.work)
        h.git("commit", "-q", "-m", msg, cwd=self.work)
        h.git("push", "-q", "origin", f"HEAD:refs/heads/{branch}", cwd=self.work)
        return h.git("rev-parse", "HEAD", cwd=self.work)


class Harness:
    """One isolated device: tmp HOME, fake root tools, origins and components."""

    def __init__(self, root: Path, home: Path, mp: pytest.MonkeyPatch) -> None:
        self.root = root
        self.home = home
        self.remotes = root / "remotes"
        self.state = root / "fakeroot"
        self.bin = root / "bin"
        self.hooks = root / "hooks"
        self.run_dir = root / "run"
        self.etc = root / "etc"
        for d in (self.remotes, self.state, self.bin, self.hooks, self.etc):
            d.mkdir(parents=True)
        self.run_dir.mkdir(mode=0o700)
        self.components: list[dict] = []
        self.printing = AsyncMock(return_value=False)
        self.apt_upgrade = AsyncMock()
        self.dbus_g: dict = {}
        self.mp = mp

    # -- git -----------------------------------------------------------------

    def git(self, *args: str, cwd: Path | None = None) -> str:
        """Run git as the test author; return stripped stdout."""
        out = subprocess.run(
            ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
        )
        return out.stdout.strip()

    def remote(self, name: str, files: dict[str, str] | None = None) -> Remote:
        """Create an origin with one initial commit."""
        r = Remote(self, name)
        r.commit(files or {"README": f"{name}\n"}, msg="initial")
        return r

    def install(self, remote: Remote, branch: str = "master") -> Path:
        """Clone the origin into HOME over its https URL, as the installer does."""
        path = self.home / remote.name
        self.git("clone", "-q", "--branch", branch, remote.url, str(path))
        return path

    def head(self, name: str) -> str:
        """HEAD sha of the installed component."""
        return self.git("rev-parse", "HEAD", cwd=self.home / name)

    def branch(self, name: str) -> str:
        """Checked-out branch of the installed component."""
        return self.git("rev-parse", "--abbrev-ref", "HEAD", cwd=self.home / name)

    # -- components.yaml -----------------------------------------------------

    def component(self, name: str, **fields: object) -> dict:
        """Register a git component pointing at HOME/<name> and its origin."""
        entry = {
            "name": name,
            "type": "git",
            "path": str(self.home / name),
            "url": f"{REMOTE_BASE}{name}.git",
            "branch": "master",
            "reset_mode": "hard",
            "order": 10 + len(self.components),
        } | fields
        self.components.append(entry)
        return entry

    # -- hooks, fakes, observations ------------------------------------------

    def hook(self, name: str, body: str) -> None:
        """Install a post-update hook for a component."""
        _script(self.hooks / f"{name}.sh", body)

    def real_hook(self, name: str) -> None:
        """Install the shipped hook for a component."""
        dst = self.hooks / f"{name}.sh"
        shutil.copy(REPO_ROOT / "updater" / "hooks" / f"{name}.sh", dst)
        dst.chmod(0o755)

    def venv_pip(self, name: str, body: str = "exit 0\n") -> Path:
        """Give a component a logging venv pip (the sibling .<name>-env layout)."""
        pip_dir = self.home / f".{name}-env" / "bin"
        pip_dir.mkdir(parents=True)
        log = f'echo "venv-pip $*" >>"{self.state}/calls.log"\n'
        return _script(pip_dir / "pip", log + body)

    def fail_restart(self, unit: str) -> None:
        """Make `systemctl restart <unit>` fail."""
        (self.state / f"fail-restart-{unit}").touch()

    def calls(self) -> list[str]:
        """Every fake root-tool invocation, in order."""
        log = self.state / "calls.log"
        return log.read_text().splitlines() if log.exists() else []

    def history(self) -> list[dict]:
        """Parsed update_history.jsonl."""
        path = self.home / ".cache" / "blockscreen" / "update_history.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text().splitlines()]

    def events(self, component: str) -> list[str]:
        """History event names for one component."""
        return [e["event"] for e in self.history() if e["component"] == component]

    def state_file(self) -> dict:
        """Parsed updater_state.json."""
        return json.loads(
            (self.home / ".cache/blockscreen/updater_state.json").read_text()
        )

    @property
    def inflight(self) -> Path:
        """The in-flight batch marker."""
        return self.home / ".cache" / "blockscreen" / "updater_inflight.json"

    @property
    def deploy_flag(self) -> Path:
        """The flag BlocksScreen-deploy.path watches."""
        return self.home / ".config" / "blockscreen" / ".run-install-updater"

    @property
    def sentinel(self) -> Path:
        """The deferred-restart sentinel a self-update hook writes."""
        return self.run_dir / "updater-restart-needed"

    def service(self):
        """A fresh UpdateService over the registered components."""
        import updater.dbus_service as dbus_mod

        recorder = Recorder()
        svc = dbus_mod.UpdateService(callback=recorder)
        return svc, recorder


def _write_fakes(h: Harness) -> None:
    """Drop the fake root tools into h.bin."""
    fmt = {"state": h.state, "bin": h.bin}
    _script(h.bin / "systemctl", _SYSTEMCTL.format(**fmt))
    _script(h.bin / "sudo", _SUDO.format(**fmt))
    _script(h.bin / "apt", _APT.format(**fmt))
    for tool in ("apt-mark", "dpkg", "bs-apt-helper", "pip3"):
        _script(h.bin / tool, _LOGGED.format(name=tool, **fmt))
    # The shipped hook's daemon-reload fallback must not reach the host bus.
    _script(h.bin / "dbus-send", "exit 1\n")


def _patch(mp: pytest.MonkeyPatch, g: dict, **values: object) -> None:
    """Patch module globals, failing loudly if a name was renamed upstream."""
    for key, value in values.items():
        assert key in g, f"harness patches a missing global {key!r}"
        mp.setitem(g, key, value)


@pytest.fixture
def harness(tmp_path, monkeypatch, mock_sdbus) -> Harness:
    """Isolated device with every updater path and root tool redirected."""
    import updater.dbus_service as dbus_mod

    root = tmp_path.resolve()
    home = root / "home"
    home.mkdir()
    h = Harness(root, home, monkeypatch)
    _write_fakes(h)

    for var in ("XDG_CONFIG_HOME", "GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_GLOBAL"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("PATH", f"{h.bin}{os.pathsep}{os.environ['PATH']}")
    (home / ".gitconfig").write_text(
        "[user]\n\tname = Integration\n\temail = integration@example.invalid\n"
        "[commit]\n\tgpgsign = false\n"
        "[init]\n\tdefaultBranch = master\n"
        "[advice]\n\tdetachedHead = false\n"
        f'[url "file://{h.remotes}/"]\n\tinsteadOf = {REMOTE_BASE}\n'
    )

    # sdbus mock re-imports updater; resolve the live modules through the class.
    svc_g = dbus_mod.UpdateService.__init__.__globals__
    exec_g = svc_g["git_fetch"].__globals__
    lock_g = exec_g["restart_sentinel_path"].__globals__
    comp_g = svc_g["load_components"].__globals__
    cache = home / ".cache" / "blockscreen"
    deploy_unit = h.etc / "BlocksScreen-deploy.path"
    deploy_unit.touch()

    _patch(
        monkeypatch,
        svc_g,
        _STATE_PATH=cache / "updater_state.json",
        _INFLIGHT_PATH=cache / "updater_inflight.json",
        _FAULT_MARKER_PATH=cache / "selfheal_fault.json",
        _HISTORY_PATH=cache / "update_history.jsonl",
        _APT_STATUS_CACHE=cache / "apt_status_cache.json",
        _DEPLOY_FLAG=h.deploy_flag,
        _DEPLOY_PATH_UNIT=deploy_unit,
        PIP=str(h.bin / "pip3"),
        SYSTEMCTL=str(h.bin / "systemctl"),
        klipper_printing=h.printing,
        load_components=lambda: (comp_g["_build_configs"](h.components), 86_400.0),
    )

    async def _configured_origin(path: Path) -> str:
        # get-url expands insteadOf to file://; the raw config keeps the https URL.
        ok, out = await exec_g["_run"](
            [exec_g["GIT"], "config", "--get", "remote.origin.url"],
            cwd=path,
            timeout=10.0,
        )
        return out.strip() if ok else ""

    _patch(
        monkeypatch,
        exec_g,
        SUDO=str(h.bin / "sudo"),
        SYSTEMCTL=str(h.bin / "systemctl"),
        APT=str(h.bin / "apt"),
        APT_MARK=str(h.bin / "apt-mark"),
        DPKG=str(h.bin / "dpkg"),
        APT_HELPER=h.bin / "bs-apt-helper",
        PIP=str(h.bin / "pip3"),
        KLIPPY_SOCK=root / "no-klippy.sock",
        _HOOKS_DIR=h.hooks,
        git_remote_url=_configured_origin,
    )
    _patch(monkeypatch, lock_g, _runtime_dir=lambda: h.run_dir)
    h.dbus_g = dbus_mod.UpdaterDbusService.__init__.__globals__
    _patch(
        monkeypatch,
        h.dbus_g,
        _STATUS_PATH=h.run_dir / "updater_status.json",
        _BOOT_DELAY_S=0.0,
        _DEPLOY_POLL_S=0.05,
    )
    # Self-heal supervisors poll systemd on minute timers: out of scope here.
    for method in ("supervise_ui", "forward_heal_ui", "background_prime_nrestarts"):
        monkeypatch.setattr(dbus_mod.UpdateService, method, AsyncMock())
    # Recorded, not run: the daemon must skip it when its own restart is pending.
    monkeypatch.setattr(dbus_mod.UpdateService, "background_apt_upgrade", h.apt_upgrade)
    return h


class Daemon:
    """A live UpdaterDbusService plus its recorded signals."""

    def __init__(self, iface) -> None:
        self.iface = iface
        self.log: list[tuple[str, tuple]] = []
        for name in (
            "step_complete",
            "component_done",
            "error",
            "rollback",
            "recover_done",
            "status_ready",
            "busy_changed",
            "provisioning_changed",
        ):
            setattr(iface, name, Signal(name, self.log))

    def signals(self, name: str) -> list[tuple]:
        """Args of every emit of one signal."""
        return [args for sig, args in self.log if sig == name]

    def busy_trace(self) -> list[bool]:
        """Every busy_changed value, in order."""
        return [args[0] for args in self.signals("busy_changed")]

    def statuses(self) -> list[dict]:
        """Every status_ready payload, decoded."""
        return [json.loads(args[0]) for args in self.signals("status_ready")]


@pytest.fixture
async def daemon(harness):
    """Factory for live daemons; each is shut down at teardown."""
    import updater.dbus_service as dbus_mod

    started: list[Daemon] = []

    def start() -> Daemon:
        d = Daemon(dbus_mod.UpdaterDbusService())
        started.append(d)
        return d

    yield start
    for d in started:
        await d.iface.shutdown()


async def wait_for(predicate, timeout: float = 15.0, what: str = "condition") -> None:
    """Poll predicate until true; fail with `what` on timeout."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while not predicate():
        if loop.time() >= deadline:
            pytest.fail(f"timed out waiting for {what}")
        await asyncio.sleep(0.02)
