"""Tests for scripts/bs-clock-sync.sh against a local TLS server and the real openssl."""

from __future__ import annotations

import datetime as dt
import socket
import os
import re
import shutil
import ssl
import subprocess
import threading
import time
from collections.abc import Iterator, Sequence
from email.utils import formatdate
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    shutil.which("openssl") is None, reason="needs the openssl CLI"
)

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "bs-clock-sync.sh"
_DAY = 86400
_NAMES = [f"m{i}.test" for i in range(4)]
# Host -> Date offset in s rendered per request, or raw header ("" = none, _CLOSE = hang up).
_DATES: dict[str, int | str] = {}
_SLOW: set[str] = set()
# Hosts whose HEAD reached a server.
_SEEN: set[str] = set()
_CLOSE = "close"
_TIMEOUT_S = 3


class _DateHandler(BaseHTTPRequestHandler):
    """Answers HEAD with the Date header registered for the requested Host."""

    def do_HEAD(self) -> None:  # noqa: N802
        host = self.headers.get("Host", "")
        _SEEN.add(host)
        if host in _SLOW:
            time.sleep(_TIMEOUT_S / 2)
        hdr = _DATES.get(host, "")
        if isinstance(hdr, int):
            hdr = formatdate(time.time() + hdr, usegmt=True)
        if hdr == _CLOSE:
            return
        self.send_response_only(200)
        if hdr:
            self.send_header("date", hdr)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Keep test output quiet."""


_CA_CONF = """\
[ca]
default_ca = d
[d]
database = {tmp}/index.txt
serial = {tmp}/serial
new_certs_dir = {tmp}
default_md = sha256
policy = p
unique_subject = no
[p]
commonName = supplied
[v3_ca]
basicConstraints = critical,CA:TRUE
keyUsage = critical,keyCertSign
[leaf]
basicConstraints = critical,CA:FALSE
subjectAltName = {sans}
"""


def _openssl(*args: str | Path) -> None:
    subprocess.run(["openssl", *map(str, args)], check=True, capture_output=True)


def _asn1_time(days: int) -> str:
    """UTCTime now+days, the -startdate/-enddate form OpenSSL 3.0 accepts."""
    when = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=days)
    return when.strftime("%y%m%d%H%M%SZ")


def _cert(
    tmp: Path, tag: str, subject: str, issuer: str | None, days: tuple[int, int]
) -> None:
    """Write tag.key and tag.pem: a self-signed CA (issuer None) or a leaf signed by issuer."""
    conf = tmp / "ca.cnf"
    if not conf.exists():
        sans = ",".join(f"DNS:{n}" for n in _NAMES)
        conf.write_text(_CA_CONF.format(tmp=tmp, sans=sans))
        (tmp / "index.txt").touch()
        (tmp / "serial").write_text("01\n")
    key, csr = tmp / f"{tag}.key", tmp / f"{tag}.csr"
    _openssl(
        "genpkey",
        "-algorithm",
        "EC",
        "-pkeyopt",
        "ec_paramgen_curve:P-256",
        "-out",
        key,
    )
    _openssl("req", "-new", "-key", key, "-subj", f"/CN={subject}", "-out", csr)
    sign = (
        ["-selfsign", "-keyfile", key, "-extensions", "v3_ca"]
        if issuer is None
        else [
            "-cert",
            tmp / f"{issuer}.pem",
            "-keyfile",
            tmp / f"{issuer}.key",
            "-extensions",
            "leaf",
        ]
    )
    _openssl(
        "ca", "-batch", "-notext", "-config", conf, "-in", csr,
        "-out", tmp / f"{tag}.pem", "-startdate", _asn1_time(days[0]),
        "-enddate", _asn1_time(days[1]), *sign,
    )  # fmt: skip


def _serve(tmp: Path, tag: str) -> ThreadingHTTPServer:
    """Start a TLS server for one cert in a daemon thread."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(tmp / f"{tag}.pem", tmp / f"{tag}.key")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _DateHandler)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


@pytest.fixture(scope="module")
def tls(tmp_path_factory) -> Iterator[dict[str, object]]:
    """CA file plus one server per cert kind: ok, expired, notyet (clock behind), rogue CA."""
    tmp = tmp_path_factory.mktemp("tls")
    _cert(tmp, "ca", "Test CA", None, (-3000, 3000))
    _cert(tmp, "rogueca", "Rogue CA", None, (-3000, 3000))
    ports = {}
    servers = []
    for kind, issuer, days in (
        ("ok", "ca", (-1000, 1000)),
        ("expired", "ca", (-30, -1)),
        ("notyet", "ca", (1, 30)),
        ("rogue", "rogueca", (-1000, 1000)),
    ):
        _cert(tmp, kind, _NAMES[0], issuer, days)
        servers.append(_serve(tmp, kind))
        ports[kind] = servers[-1].server_address[1]
    # Accepts TCP, never answers the TLS hello.
    stall = socket.create_server(("127.0.0.1", 0))
    ports["stall"] = stall.getsockname()[1]
    yield {"cafile": str(tmp / "ca.pem"), "ports": ports}
    # Left running, the server threads outlive the module into the Qt tests.
    for httpd in servers:
        httpd.shutdown()
        httpd.server_close()
    stall.close()


def _marker(jump: int = 0) -> str:
    """Marker as the script writes it; jump = wall-clock jump since then."""
    return f"{int(time.time()) - jump} {int(time.clock_gettime(time.CLOCK_BOOTTIME))}\n"


def _run(
    tmp_path: Path,
    tls: dict,
    sources: Sequence[tuple[str, int | str | None]],
    *,
    synced: bool = False,
    floor: int = 0,
    print_state: str | None = "standby",
    verified: bool = False,
    disabled: bool = False,
    syncs_mid_run: bool = False,
) -> tuple[str, str, bool, bool]:
    """Run the script; return (stdout, date -s args, marker, touched)."""
    shim = tmp_path / "bin"
    shim.mkdir(exist_ok=True)
    log, marker, clock = tmp_path / "set.log", tmp_path / "verified", tmp_path / "clock"
    if verified:
        marker.write_text(_marker())
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
        _DATES[name] = "" if hdr is None else hdr
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
    ntp = (
        f'#!/bin/sh\n[ -e "{tmp_path}/ntp.calls" ] && echo yes && exit 0\n'
        f'touch "{tmp_path}/ntp.calls"; echo no\n'
        if syncs_mid_run
        else f"#!/bin/sh\necho {'yes' if synced else 'no'}\n"
    )
    (shim / "timedatectl").write_text(ntp)
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


_AHEAD = ("ok", _DAY)


@pytest.mark.parametrize(
    ("sources", "kwargs"),
    [
        ([_AHEAD] * 2, {"synced": True}),
        ([_AHEAD] * 2, {"verified": True}),
        ([_AHEAD] * 2, {"disabled": True}),
        ([("down", None)] * 2, {}),
        ([_AHEAD, ("down", None), ("down", None)], {}),
        ([_AHEAD, ("ok", 2 * _DAY), ("ok", 3 * _DAY)], {}),
        ([("ok", "garbage")] * 2, {}),
        ([("ok", -_DAY)] * 2, {"floor": int(time.time())}),
        ([_AHEAD] * 2, {"print_state": "printing"}),
        ([_AHEAD] * 2, {"print_state": "paused"}),
        # Only the chain and name checks stop a forged Date.
        ([_AHEAD, ("rogue", _DAY)], {}),
        ([_AHEAD, ("wronghost", _DAY)], {}),
        # An expired cert cannot vouch for a date past its validity.
        ([("expired", 10 * _DAY)] * 2, {}),
        ([("stall", None)] * 4, {}),
        ([("dns", None)] * 2, {}),
        ([_AHEAD, ("close", None), ("nohdr", None)], {}),
        ([_AHEAD] * 2, {"syncs_mid_run": True}),
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
        "ntp-synced-mid-run",
    ],
)
def test_clock_left_alone(tmp_path: Path, tls, sources, kwargs) -> None:
    _, set_args, marker, touched = _run(tmp_path, tls, sources, **kwargs)
    assert set_args == ""
    assert not touched
    assert marker is kwargs.get("verified", False)


def test_clock_close_enough_is_verified(tmp_path: Path, tls) -> None:
    sources = [("ok", 30), ("ok", 31)]
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
        (-_DAY, [("down", None), ("ok", 0), ("ok", 0)]),
        (5 * _DAY, [("stall", None), ("close", None), ("ok", 0), ("slow", 0)]),
        (7 * _DAY, [("dns", None), ("nohdr", None), ("ok", 0), ("ok", 0)]),
    ],
    ids=[
        "one-down",
        "one-lying",
        "years-ahead",
        "clock-ahead-certs-expired",
        "clock-behind-certs-notyet",
        "first-down",
        "messy-stall-hangup-slow",
        "messy-dns-no-date",
    ],
)
def test_clock_stepped_when_two_agree(
    tmp_path: Path, tls, offset: int, sources
) -> None:
    start = time.time()
    resolved = [(k, None if extra is None else offset + extra) for k, extra in sources]
    out, set_args, marker, touched = _run(tmp_path, tls, resolved)
    assert "@" in set_args, out
    target = int(set_args.split("@")[1]) - offset
    assert start - 2 <= target <= time.time() + 2
    assert "clock stepped" in out
    assert marker and touched


@pytest.mark.parametrize(
    "stale",
    [_marker(30 * _DAY), _marker(-3600), "1700000000\n", ""],
    ids=["clock-fell-back", "clock-jumped-ahead", "old-format", "empty"],
)
def test_stale_marker_does_not_block_a_heal(tmp_path: Path, tls, stale: str) -> None:
    """A clock that jumped after verification is healed again and re-marked."""
    (tmp_path / "verified").write_text(stale)
    out, set_args, _, _ = _run(tmp_path, tls, [_AHEAD] * 2)
    assert "@" in set_args, out
    wall, boot = map(int, (tmp_path / "verified").read_text().split())
    assert abs(wall - time.time()) < 5
    assert abs(boot - time.clock_gettime(time.CLOCK_BOOTTIME)) < 5


def test_step_is_the_mean_of_the_agreeing_pair(tmp_path: Path, tls) -> None:
    """Neither source of the pair is preferred: the step lands between them."""
    out, *_ = _run(tmp_path, tls, [("ok", _DAY), ("ok", _DAY + 4)])
    step = int(re.search(r"clock stepped by (-?\d+) s", out)[1])
    assert _DAY + 1 <= step <= _DAY + 3, out


def test_unverified_peer_never_gets_the_request(tmp_path: Path, tls) -> None:
    """A rogue or wrong-host TLS peer is dropped at the handshake, before the HEAD is sent."""
    _run(tmp_path, tls, [("rogue", _DAY), ("wronghost", _DAY)])
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


def test_timeouts_nest() -> None:
    """Script worst case fits the unit timeout, which fits the updater's wait."""
    from updater.executor import CLOCK_HEAL_WAIT_S

    script = _SCRIPT.read_text()
    per_conn = int(re.search(r"TIMEOUT_S=\$\{BS_CLOCK_TIMEOUT:-(\d+)\}", script)[1])
    sources = re.search(r'BS_CLOCK_SOURCES:-([^}"]+)\}', script)[1].split()
    unit = (_ROOT / "scripts" / "BlocksScreen-clock.service").read_text()
    unit_s = int(re.search(r"^TimeoutStartSec=(\d+)$", unit, re.M)[1])
    worst_s = 2 * len(sources) * per_conn + 5
    assert worst_s < unit_s < CLOCK_HEAL_WAIT_S


def test_step_threshold_matches_marker_jump() -> None:
    """The script's step threshold is the jump the updater treats as voiding the marker."""
    from updater.executor import _CLOCK_MARKER_JUMP_S

    script = _SCRIPT.read_text()
    assert (
        int(re.search(r"^MIN_STEP_S=(\d+)$", script, re.M)[1]) == _CLOCK_MARKER_JUMP_S
    )
