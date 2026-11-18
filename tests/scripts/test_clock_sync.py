"""Tests for scripts/bs-clock-sync.sh against a local TLS server and the real openssl."""

from __future__ import annotations

import datetime as dt
import socket
import os
import shutil
import ssl
import subprocess
import threading
import time
from collections.abc import Sequence
from email.utils import formatdate
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

pytestmark = pytest.mark.skipif(
    shutil.which("openssl") is None, reason="needs the openssl CLI"
)

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "bs-clock-sync.sh"
_DAY = 86400
_NAMES = [f"m{i}.test" for i in range(4)]
# Host -> Date header to send ("" = none, _CLOSE = hang up).
_DATES: dict[str, str] = {}
_SLOW: set[str] = set()
# Hosts whose HEAD reached a server.
_SEEN: set[str] = set()
_CLOSE = "close"
_TIMEOUT_S = 3


class _DateHandler(BaseHTTPRequestHandler):
    """Answers HEAD with the Date header registered for the requested Host."""

    def do_HEAD(self) -> None:  # noqa: N802
        """Send only a status line and the configured Date header."""
        host = self.headers.get("Host", "")
        _SEEN.add(host)
        if host in _SLOW:
            time.sleep(_TIMEOUT_S / 2)
        hdr = _DATES.get(host, "")
        if hdr == _CLOSE:
            return
        self.send_response_only(200)
        if hdr:
            self.send_header("date", hdr)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Keep test output quiet."""


def _cert(
    subject: str,
    key: ec.EllipticCurvePrivateKey,
    issuer: tuple[str, ec.EllipticCurvePrivateKey] | None = None,
    *,
    days: tuple[int, int] = (-1, 1),
) -> x509.Certificate:
    """Build a CA cert (no issuer) or a leaf for _NAMES valid between now+days."""
    now = dt.datetime.now(dt.timezone.utc)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject)])
    issuer_name, signer = (subject, key) if issuer is None else issuer
    builder = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, issuer_name)]))
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now + dt.timedelta(days=days[0]))
        .not_valid_after(now + dt.timedelta(days=days[1]))
        .add_extension(x509.BasicConstraints(ca=issuer is None, path_length=None), True)
    )
    if issuer is not None:
        sans = [x509.DNSName(n) for n in _NAMES]
        builder = builder.add_extension(x509.SubjectAlternativeName(sans), False)
    return builder.sign(signer, hashes.SHA256())


def _serve(tmp: Path, tag: str, cert: x509.Certificate, key) -> int:
    """Start a TLS server for one cert in a daemon thread; return its port."""
    pem = tmp / f"{tag}.pem"
    pem.write_bytes(
        cert.public_bytes(serialization.Encoding.PEM)
        + key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(pem)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _DateHandler)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1]


@pytest.fixture(scope="module")
def tls(tmp_path_factory) -> dict[str, object]:
    """CA file plus one server per cert kind: ok, expired, notyet (clock behind), rogue CA."""
    tmp = tmp_path_factory.mktemp("tls")
    ca_key, rogue_key = (
        ec.generate_private_key(ec.SECP256R1()),
        ec.generate_private_key(ec.SECP256R1()),
    )
    ca = _cert("Test CA", ca_key, days=(-3000, 3000))
    (tmp / "ca.pem").write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    ports = {}
    for kind, issuer, days in (
        ("ok", ("Test CA", ca_key), (-1000, 1000)),
        ("expired", ("Test CA", ca_key), (-30, -1)),
        ("notyet", ("Test CA", ca_key), (1, 30)),
        ("rogue", ("Rogue CA", rogue_key), (-1000, 1000)),
    ):
        key = ec.generate_private_key(ec.SECP256R1())
        ports[kind] = _serve(tmp, kind, _cert(_NAMES[0], key, issuer, days=days), key)
    # Accepts TCP, never answers the TLS hello.
    stall = socket.create_server(("127.0.0.1", 0))
    ports["stall"] = stall.getsockname()[1]
    return {"cafile": str(tmp / "ca.pem"), "ports": ports, "_keep": stall}


def _http_date(offset_s: int) -> str:
    return formatdate(time.time() + offset_s, usegmt=True)


def _run(
    tmp_path: Path,
    tls: dict,
    sources: Sequence[tuple[str, str | None]],
    *,
    synced: bool = False,
    floor: int = 0,
    print_state: str | None = "standby",
    verified: bool = False,
    disabled: bool = False,
) -> tuple[str, str, bool, bool]:
    """Run the script; return (stdout, date -s args, marker, touched)."""
    shim = tmp_path / "bin"
    shim.mkdir()
    log, marker, clock = tmp_path / "set.log", tmp_path / "verified", tmp_path / "clock"
    if verified:
        marker.touch()
    if disabled:
        (tmp_path / "disabled").touch()
    clock.touch()
    os.utime(clock, (0, 0))
    entries = []
    _DATES.clear()
    _SLOW.clear()
    _SEEN.clear()
    for name, (kind, hdr) in zip(_NAMES, sources, strict=False):
        if kind == "dns":
            entries.append("nx.invalid")
            continue
        if kind == "wronghost":
            name, kind = "evil.test", "ok"
        if kind == "slow":
            _SLOW.add(name)
        if kind in ("slow", "close", "nohdr"):
            hdr = _CLOSE if kind == "close" else hdr
            kind = "ok"
        port = 1 if kind == "down" else tls["ports"][kind]
        _DATES[name] = hdr or ""
        entries.append(f"{name}=127.0.0.1:{port}")
    # None = Moonraker unreachable.
    (shim / "curl").write_text(
        "#!/bin/sh\nexit 7\n"
        if print_state is None
        else '#!/bin/sh\nprintf \'{"result":{"status":{"print_stats":'
        f'{{"state":"{print_state}"}}}}}}}}\'\n'
    )
    (shim / "date").write_text(
        "#!/bin/bash\n"
        f'for a in "$@"; do [[ $a == -s ]] && {{ echo "$*" >>"{log}"; exit 0; }}; done\n'
        'exec /bin/date "$@"\n'
    )
    (shim / "timedatectl").write_text(f"#!/bin/sh\necho {'yes' if synced else 'no'}\n")
    (shim / "fake-hwclock").write_text("#!/bin/sh\nexit 0\n")
    for f in shim.iterdir():
        f.chmod(0o755)
    env = {
        **os.environ,
        "PATH": f"{shim}:{os.environ.get('PATH', '')}",
        "BS_CLOCK_MARKER": str(marker),
        "BS_CLOCK_DISABLE_FILE": str(tmp_path / "disabled"),
        "BS_CLOCK_SOURCES": " ".join(entries),
        "BS_CLOCK_CAFILE": tls["cafile"],
        "BS_CLOCK_TIMESYNC_FILE": str(clock),
        "BS_MOONRAKER_URL": "http://mr.invalid",
        "BS_CLOCK_FLOOR": str(floor),
        "BS_CLOCK_TIMEOUT": str(_TIMEOUT_S),
    }
    res = subprocess.run(
        ["bash", str(_SCRIPT)], capture_output=True, text=True, env=env, timeout=60
    )
    assert res.returncode == 0, res.stderr
    set_args = log.read_text() if log.exists() else ""
    return res.stdout, set_args, marker.exists(), clock.stat().st_mtime > 0


_AHEAD = ("ok", _http_date(_DAY))


@pytest.mark.parametrize(
    ("sources", "kwargs"),
    [
        ([_AHEAD] * 2, {"synced": True}),
        ([_AHEAD] * 2, {"verified": True}),
        ([_AHEAD] * 2, {"disabled": True}),
        ([("down", None)] * 2, {}),
        ([_AHEAD, ("down", None), ("down", None)], {}),
        ([_AHEAD, ("ok", _http_date(2 * _DAY)), ("ok", _http_date(3 * _DAY))], {}),
        ([("ok", "garbage")] * 2, {}),
        ([("ok", _http_date(-_DAY))] * 2, {"floor": int(time.time())}),
        ([_AHEAD] * 2, {"print_state": "printing"}),
        ([_AHEAD] * 2, {"print_state": "paused"}),
        # Only the chain and name checks stand between a forged Date and the clock.
        ([_AHEAD, ("rogue", _http_date(_DAY))], {}),
        ([_AHEAD, ("wronghost", _http_date(_DAY))], {}),
        # A key whose cert expired cannot vouch for a date past its validity.
        ([("expired", _http_date(10 * _DAY))] * 2, {}),
        ([("stall", None)] * 4, {}),
        ([("dns", None)] * 2, {}),
        ([_AHEAD, ("close", None), ("nohdr", None)], {}),
    ],
    ids=[
        "synced",
        "verified",
        "disabled",
        "offline",
        "one-source",
        "disagree",
        "garbage",
        "floor",
        "printing",
        "paused",
        "rogue-ca",
        "wrong-host",
        "date-outside-cert-validity",
        "internet-hangs",
        "dns-fails",
        "hangup-and-no-date",
    ],
)
def test_clock_left_alone(tmp_path: Path, tls, sources, kwargs) -> None:
    _, set_args, marker, touched = _run(tmp_path, tls, sources, **kwargs)
    assert set_args == ""
    assert not touched
    assert marker is kwargs.get("verified", False)


def test_clock_close_enough_is_verified(tmp_path: Path, tls) -> None:
    sources = [("ok", _http_date(30)), ("ok", _http_date(31))]
    _, set_args, marker, touched = _run(tmp_path, tls, sources)
    assert set_args == ""
    assert marker and not touched


@pytest.mark.parametrize(
    ("offset", "sources"),
    [
        (30 * _DAY, [("ok", 0), ("down", None), ("ok", 0)]),
        (-3600, [("ok", 0), ("ok", 400 * _DAY), ("ok", 0)]),  # one source lying
        (-2 * 365 * _DAY, [("ok", 0), ("ok", 0)]),  # clock years ahead
        # Box clock ahead: certs look expired. Box clock behind: certs look not yet valid.
        (-10 * _DAY, [("expired", 0), ("expired", 0)]),
        (10 * _DAY, [("notyet", 0), ("notyet", 0)]),
        (-_DAY, [("down", None), ("ok", 0), ("ok", 0)]),  # github.com is source 1
        (5 * _DAY, [("stall", None), ("close", None), ("ok", 0), ("slow", 0)]),
        (7 * _DAY, [("dns", None), ("nohdr", None), ("ok", 0), ("ok", 0)]),
    ],
    ids=[
        "one-down",
        "one-lying",
        "years-ahead",
        "clock-ahead-certs-expired",
        "clock-behind-certs-notyet",
        "github-down",
        "messy-stall-hangup-slow",
        "messy-dns-no-date",
    ],
)
def test_clock_stepped_when_two_agree(
    tmp_path: Path, tls, offset: int, sources
) -> None:
    start = time.time()
    resolved = [
        (k, None if extra is None else _http_date(offset + extra))
        for k, extra in sources
    ]
    out, set_args, marker, touched = _run(tmp_path, tls, resolved)
    assert "@" in set_args, out
    # Dates are fixed at setup, so the target lands between run start and end.
    target = int(set_args.split("@")[1]) - offset
    assert start - 2 <= target <= time.time() + 2
    assert "clock stepped" in out
    assert marker and touched


def test_unverified_peer_never_gets_the_request(tmp_path: Path, tls) -> None:
    """A rogue or wrong-host TLS peer is dropped at the handshake, before the HEAD is sent."""
    _run(tmp_path, tls, [("rogue", _http_date(_DAY)), ("wronghost", _http_date(_DAY))])
    assert _SEEN == set()


def test_moonraker_down_does_not_block_the_step(tmp_path: Path, tls) -> None:
    """No print state means no job to protect: the step goes ahead."""
    out, set_args, marker, _ = _run(tmp_path, tls, [_AHEAD] * 2, print_state=None)
    assert "@" in set_args, out
    assert marker


def test_stops_at_first_agreeing_pair(tmp_path: Path, tls) -> None:
    """Two agreeing sources end the run: later sources are never contacted."""
    _run(tmp_path, tls, [_AHEAD] * 4)
    assert _SEEN == {_NAMES[0], _NAMES[1]}


def test_dead_network_run_is_bounded(tmp_path: Path, tls) -> None:
    """Every source stalling costs at most one timeout each, then the run gives up."""
    start = time.monotonic()
    _, set_args, marker, _ = _run(tmp_path, tls, [("stall", None)] * 4)
    assert time.monotonic() - start < 4 * _TIMEOUT_S + 5
    assert set_args == "" and not marker


def test_clock_units_are_wired() -> None:
    """Service runs the script, timer is enabled, and deploy reinstalls both units."""
    scripts = _ROOT / "scripts"
    assert "bs-clock-sync.sh" in (scripts / "BlocksScreen-clock.service").read_text()
    assert (
        "WantedBy=timers.target" in (scripts / "BlocksScreen-clock.timer").read_text()
    )
    assert (
        "enable --now --no-reload BlocksScreen-clock.timer"
        in (scripts / "install-updater.sh").read_text()
    )
    post_merge = (scripts / "post-merge").read_text()
    hook = (_ROOT / "updater" / "hooks" / "BlocksScreen.sh").read_text()
    for unit in ("BlocksScreen-clock.service", "BlocksScreen-clock.timer"):
        assert f"scripts/{unit}" in hook
        assert "scripts/" + unit.replace(".", "\\.") in post_merge
