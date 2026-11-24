"""Guard: the D-Bus activation file must be one dbus-daemon will actually load."""

from __future__ import annotations

import configparser
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _ROOT / "scripts"
_ACTIVATION = _SCRIPTS / "com.blockscreen.Updater.service"


def _section(path: Path, section: str) -> configparser.SectionProxy:
    """Parse a systemd-style ini file, keeping key case."""
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.optionxform = str  # type: ignore[assignment,method-assign]
    cfg.read_string(path.read_text())
    return cfg[section]


def test_has_exec_line() -> None:
    # dbus-daemon activation.c skips any entry without Exec=; systemd units use /bin/false.
    assert _section(_ACTIVATION, "D-BUS Service").get("Exec") == "/bin/false"


def test_name_matches_filename_daemon_and_client() -> None:
    name = _section(_ACTIVATION, "D-BUS Service")["Name"]
    assert name == _ACTIVATION.stem
    daemon = (_ROOT / "updater" / "__main__.py").read_text()
    assert f'request_name_async("{name}"' in daemon
    client = (_ROOT / "BlocksScreen" / "lib" / "updater_worker.py").read_text()
    assert re.search(rf'^_DAEMON_BUS_NAME = "{re.escape(name)}"$', client, re.M)


def test_systemd_service_exists_and_user_matches() -> None:
    entry = _section(_ACTIVATION, "D-BUS Service")
    unit = _SCRIPTS / entry["SystemdService"]
    assert entry["User"] == _section(unit, "Service")["User"]


def test_install_triggers_agree_and_cover_bus_files() -> None:
    # Only install-updater.sh deploys these: a file missing from a trigger never ships.
    common = (_SCRIPTS / "bs-common.sh").read_text()
    array = re.search(r"BS_UPDATER_INSTALL_TRIGGERS=\(([^)]*)\)", common)
    assert array
    merge_set = {f"scripts/{name}" for name in array.group(1).split()}
    hook = (_ROOT / "updater" / "hooks" / "BlocksScreen.sh").read_text()
    block = hook[: hook.index("install files changed")].rsplit("diff --quiet", 1)[1]
    hook_set = set(re.findall(r"scripts/[\w.-]+", block))
    assert merge_set == hook_set
    for name in ("com.blockscreen.Updater.service", "com.blockscreen.Updater.conf"):
        assert f"scripts/{name}" in hook_set
