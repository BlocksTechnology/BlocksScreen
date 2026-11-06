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

SRC = "v0.13.0-bl.1-225-g14edee70-dirty"


@pytest.mark.parametrize(
    ("running", "source", "expected"),
    [
        ("v0.13.0-bl.1-225-g14edee706", SRC, True),  # 9 vs 8 char abbreviation
        ("v0.13.0-bl.1-225-g14edee70", "v0.13.0-bl.1-225-g14edee70", True),
        ("v0.13.0-184-g27ed6cf7", SRC, False),
        ("", SRC, False),
        ("Beacon 2.1.0", SRC, False),
        ("v0.13.0", "v0.13.0-dirty", True),  # tag-only build, no hash
    ],
)
def test_versions_match(running: str, source: str, expected: bool) -> None:
    assert mv.versions_match(running, source) is expected


def test_merge_keeps_history_and_marks_gone_mcus() -> None:
    state = {"mcus": {"mcu old": {"connected": True}}}
    mv.record_flash(state, "mcu", SRC, "dfu", "ok")
    live = {
        "host_version": SRC,
        "klippy_state": "ready",
        "mcus": {
            "mcu": {"version": "v0.13.0-184-g27ed6cf7", "chip": "stm32h723xx"},
            "beacon": {"version": "Beacon 2.1.0", "chip": "rp2040"},
        },
    }
    state = mv.merge_report(state, live, "")
    assert state["source_version"] == SRC  # falls back to the host version
    assert state["mcus"]["mcu"]["needs_flash"] is True
    assert state["mcus"]["mcu"]["last_flash"]["result"] == "ok"
    assert state["mcus"]["beacon"]["needs_flash"] is None
    assert state["mcus"]["mcu old"]["connected"] is False


_ROUTES = {
    "/printer/info": {"state": "ready", "software_version": SRC},
    "/printer/objects/list": {"objects": ["mcu", "mcu pi", "toolhead"]},
}
_STATUS = {
    "mcu": {"mcu_version": "v0.13.0-bl.1-225-g14edee706"},
    "mcu pi": {"mcu_version": "v0.13.0-bl.1-224-gd61bf239"},
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
        f"versions_match v0.13.0-1-g14edee706 {SRC} && echo match; "
        f'versions_match "" {SRC} || echo empty; '
        f'resolve_serial "{tmp_path}/usb-Klipper_rp2040_*"'
    )
    (tmp_path / "usb-Klipper_rp2040_ABC").touch()
    out = subprocess.run(
        ["bash", "-c", script],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    ).stdout.split()
    assert out == ["match", "empty", f"{tmp_path}/usb-Klipper_rp2040_ABC"]
