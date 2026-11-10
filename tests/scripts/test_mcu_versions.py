"""Tests for scripts/mcu_versions.py and the flash_mcus.sh helpers that wrap it."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
_spec = importlib.util.spec_from_file_location(
    "mcu_versions", _SCRIPTS / "mcu_versions.py"
)
assert _spec and _spec.loader
mv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mv)

SRC = "v0.13.0-225-g1a2b3c4d-dirty"


@pytest.mark.parametrize(
    ("running", "source", "expected"),
    [
        ("v0.13.0-225-g1a2b3c4d5", SRC, True),  # 9 vs 8 char abbreviation
        ("v0.13.0-225-g1a2b3c4d", "v0.13.0-225-g1a2b3c4d", True),
        ("v0.13.0-184-g5e6f7a8b", SRC, False),
        ("", SRC, False),
        ("Probe 2.1.0", SRC, False),
        ("v0.13.0", "v0.13.0-dirty", True),  # tag-only build, no hash
    ],
)
def test_versions_match(running: str, source: str, expected: bool) -> None:
    assert mv.versions_match(running, source) is expected


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (SRC, "1a2b3c4d"),
        ("v0.0.1-412-g36534d7", "36534d7"),  # fork with its own tags
        ("v0.12.0-rf50-5-g36534d7", "36534d7"),
        ("1a2b3c4d", "1a2b3c4d"),  # untagged checkout: --always gives the bare hash
        ("1a2b3c4d-dirty-20260101_120000-host", "1a2b3c4d"),
        ("v1.2.3", ""),  # third-party firmware; Klipper's --long never omits -N-g
        ("Probe 2.1.0", ""),
        ("?-20260101_120000-host", ""),  # built without git or klippy/.version
        ("", ""),
    ],
)
def test_klipper_version_shape(version: str, expected: str) -> None:
    assert mv.git_hash(version) == expected
    assert mv.is_klipper_version(version) is bool(expected)


@pytest.mark.parametrize("body", ["[]", '{"mcus": []}', "null"])
def test_malformed_state_is_ignored(tmp_path: Path, body: str) -> None:
    state_file = tmp_path / "s.json"
    state_file.write_text(body)
    assert mv.load_state(state_file) == {"schema": mv.SCHEMA, "mcus": {}}


def test_failed_save_leaves_no_temp_file(tmp_path: Path) -> None:
    state_file = tmp_path / "s.json"
    state_file.write_text("{}")
    assert mv.save_state(state_file, {"bad": object()}) is False
    assert [p.name for p in tmp_path.iterdir()] == ["s.json"]
    assert state_file.read_text() == "{}"


def test_merge_keeps_history_and_marks_gone_mcus() -> None:
    state = {"mcus": {"mcu old": {"connected": True}}}
    mv.record_flash(state, "mcu", SRC, "dfu", "ok")
    live = {
        "host_version": SRC,
        "klippy_state": "ready",
        "mcus": {
            "mcu": {"version": "v0.13.0-184-g5e6f7a8b", "chip": "stm32"},
            "probe": {"version": "Probe 2.1.0", "chip": "probe"},
        },
    }
    state = mv.merge_report(state, live, "")
    assert state["source_version"] == SRC  # falls back to the host version
    assert state["mcus"]["mcu"]["needs_flash"] is True
    assert state["mcus"]["mcu"]["last_flash"]["result"] == "ok"
    assert state["mcus"]["probe"]["needs_flash"] is None
    assert state["mcus"]["mcu old"]["connected"] is False


_ROUTES = {
    "/printer/info": {"state": "ready", "software_version": SRC},
    "/printer/objects/list": {"objects": ["mcu", "mcu pi", "toolhead"]},
}
_STATUS = {
    "mcu": {"mcu_version": "v0.13.0-225-g1a2b3c4d5"},
    "mcu pi": {"mcu_version": "v0.13.0-224-g9c8d7e6f"},
    "print_stats": {"state": "printing"},
}


class _Moonraker(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        body = _ROUTES.get(path, {"status": _STATUS})
        data = json.dumps({"result": body}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args: object) -> None:
        pass


@pytest.fixture
def moonraker_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Moonraker)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


def test_report_flags_outdated_and_writes_state(
    moonraker_url: str, tmp_path: Path
) -> None:
    state_file = tmp_path / "mcu_versions.json"
    rc = mv.main(
        ["report", "--url", moonraker_url, "--source", SRC]
        + ["--state-file", str(state_file), "--quiet"]
    )
    state = json.loads(state_file.read_text())
    assert rc == 2
    assert state["mcus"]["mcu"]["needs_flash"] is False
    assert state["mcus"]["mcu pi"]["needs_flash"] is True


def test_print_state_reports_active_print(moonraker_url: str) -> None:
    assert mv.query_print_state(moonraker_url) == "printing"


def test_shell_helpers(tmp_path: Path) -> None:
    script = (
        f'. "{_SCRIPTS / "flash_mcus.sh"}"; '
        f"versions_match v0.13.0-1-g1a2b3c4d5 {SRC} && echo match; "
        f'versions_match "" {SRC} || echo empty; '
        f'resolve_serial "{tmp_path}/usb-Klipper_mcu_*"'
    )
    (tmp_path / "usb-Klipper_mcu_ABC").touch()
    out = subprocess.run(
        ["bash", "-c", script],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    ).stdout.split()
    assert out == ["match", "empty", f"{tmp_path}/usb-Klipper_mcu_ABC"]


def _run_lock_script(tmp_path: Path, body: str) -> subprocess.CompletedProcess:
    # sudo stub: runs file ops for real, echoes systemctl calls
    script = (
        f'. "{_SCRIPTS / "flash_mcus.sh"}"; '
        f'KLIPPER_HOLD_DROPIN="{tmp_path}/hold.conf"; '
        'sudo() { if [ "$1" = systemctl ]; then echo "$*"; else "$@"; fi; }; ' + body
    )
    return subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        timeout=20,
        env={
            "PATH": "/usr/bin:/bin",
            "HOME": str(tmp_path),
            "FW_BUILD_ROOT": str(tmp_path),
        },
    )


def test_stale_hold_is_released_once_lock_is_free(tmp_path: Path) -> None:
    (tmp_path / "hold.conf").write_text("[Unit]\n")
    res = _run_lock_script(tmp_path, "take_flash_lock && recover_stale_hold")
    assert res.returncode == 0, res.stderr
    assert not (tmp_path / "hold.conf").exists()
    assert res.stdout.split("\n")[:2] == [
        "systemctl daemon-reload",
        "systemctl start klipper",
    ]


def test_hold_of_a_running_flash_is_kept(tmp_path: Path) -> None:
    (tmp_path / "hold.conf").write_text("[Unit]\n")
    holder = subprocess.Popen(["flock", str(tmp_path / "flash.lock"), "sleep", "30"])
    try:
        for _ in range(100):
            if (tmp_path / "flash.lock").exists():
                break
            threading.Event().wait(0.05)
        res = _run_lock_script(tmp_path, "take_flash_lock || echo busy")
    finally:
        holder.kill()
        holder.wait()
    assert res.stdout.strip() == "busy"
    assert (tmp_path / "hold.conf").exists()
