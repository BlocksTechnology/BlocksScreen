"""Fault-injection tests for scripts/bs-venv-heal.py, the power-cut venv repair."""

from __future__ import annotations

import importlib.util
import types
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "bs-venv-heal.py"
_CFG = "home = /usr/bin\ninclude-system-site-packages = false\nversion = 3.11.2\n"


@pytest.fixture
def heal(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> types.ModuleType:
    """Load the helper with sys.prefix pointed at an empty fake venv."""
    spec = importlib.util.spec_from_file_location("bs_venv_heal", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    venv = tmp_path / "venv"
    monkeypatch.setattr(mod.sys, "prefix", str(venv))
    mod._site_packages().mkdir(parents=True)
    (venv / "bin").mkdir()
    (venv / "pyvenv.cfg").write_text(_CFG)
    return mod


def _dist(site: Path, name: str, version: str, files: dict[str, bytes]) -> Path:
    """Install a fake dist the way pip lays it out, RECORD sizes included."""
    dist_info = site / f"{name}-{version}.dist-info"
    dist_info.mkdir()
    (dist_info / "METADATA").write_text(
        f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n"
    )
    (dist_info / "REQUESTED").write_bytes(b"")
    rows = []
    for rel, data in files.items():
        path = site / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        rows.append(f"{rel},sha256=x,{len(data)}")
    rows += [
        f"{dist_info.name}/METADATA,sha256=x,10",
        f"{dist_info.name}/REQUESTED,sha256=x,0",
        f"{dist_info.name}/RECORD,,",
        f"{name}/__pycache__/__init__.cpython-311.pyc,,",
    ]
    (dist_info / "RECORD").write_text("\n".join(rows) + "\n")
    return dist_info


def test_intact_venv_reports_nothing(heal: types.ModuleType) -> None:
    site = heal._site_packages()
    _dist(site, "foo", "1.0", {"foo/__init__.py": b"x = 1\n"})
    assert heal.broken_dists(site) == []


@pytest.mark.parametrize(
    "damage",
    [
        lambda d: (d.parent / "foo/__init__.py").write_bytes(b""),  # delalloc 0-byte
        lambda d: (d.parent / "foo/__init__.py").unlink(),
        lambda d: (d / "METADATA").write_bytes(b""),
        lambda d: (d / "METADATA").write_bytes(b"\0" * 64),
        lambda d: (d / "RECORD").write_bytes(b""),
        lambda d: (d / "RECORD").write_bytes(b"\0" * 64),
        lambda d: (d / "RECORD").unlink(),
    ],
)
def test_power_cut_damage_is_flagged(heal: types.ModuleType, damage) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "foo", "1.0", {"foo/__init__.py": b"x = 1\n"})
    _dist(site, "bar", "2.0", {"bar/__init__.py": b"y = 2\n"})
    damage(dist_info)
    assert heal.broken_dists(site) == [("foo==1.0", dist_info)]


def test_pip_rollback_stash_is_ignored(heal: types.ModuleType) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "foo", "1.0", {"foo/__init__.py": b"x = 1\n"})
    stash = site / "~oo-0.9.dist-info"  # left by a pip upgrade killed mid-way
    stash.mkdir()
    (stash / "RECORD").write_text("foo/__init__.py,sha256=x,999\n")
    assert heal.broken_dists(site) == []
    assert (site / "foo/__init__.py").read_bytes() == b"x = 1\n"
    assert dist_info.exists()


def test_uninstall_keeps_shared_dir_and_never_leaves_prefix(
    heal: types.ModuleType, tmp_path: Path
) -> None:
    site = heal._site_packages()
    outside = tmp_path / "outside.txt"
    outside.write_text("keep")
    dist_info = _dist(
        site, "foo", "1.0", {"foo/__init__.py": b"a", "shared/foo.py": b"b"}
    )
    _dist(site, "bar", "2.0", {"shared/bar.py": b"c"})
    (site / "foo/__pycache__").mkdir()
    (site / "foo/__pycache__/__init__.cpython-311.pyc").write_bytes(b"pyc")
    with (dist_info / "RECORD").open("a") as fh:
        fh.write(f"{Path('..', '..', '..', '..', 'outside.txt')},sha256=x,4\n")
    heal._uninstall(dist_info)
    assert not dist_info.exists()
    assert not (site / "foo").exists()  # a stale tree would shadow the reinstall
    assert not (site / "shared/foo.py").exists()
    assert (site / "shared/bar.py").read_bytes() == b"c"
    assert outside.read_text() == "keep"


def _fake_pip(monkeypatch: pytest.MonkeyPatch, heal: types.ModuleType, rc: int):
    """Stub `pip install`; returns the list of argv it was called with."""
    calls: list[list[str]] = []

    def run(argv, **_kw):
        calls.append(argv)
        return types.SimpleNamespace(returncode=rc)

    monkeypatch.setattr(heal, "subprocess", types.SimpleNamespace(run=run))
    monkeypatch.setattr(heal, "_pip_works", lambda: True)
    return calls


def test_offline_heal_keeps_pending_then_online_heal_clears_it(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "foo", "1.0", {"foo/__init__.py": b"x = 1\n"})
    (site / "foo/__init__.py").write_bytes(b"")

    calls = _fake_pip(monkeypatch, heal, rc=1)
    assert heal.heal() == 1  # damage found this run: caller reinstalls its set
    assert not dist_info.exists()
    assert heal._read_pending() == ["foo==1.0"]
    assert calls[-1][-1] == "foo==1.0"

    _fake_pip(monkeypatch, heal, rc=1)
    assert heal.heal() == 2  # still offline, nothing new: reinstall stays pending
    assert heal._read_pending() == ["foo==1.0"]

    calls = _fake_pip(monkeypatch, heal, rc=0)
    assert heal.heal() == 1
    assert "--force-reinstall" in calls[-1] and calls[-1][-1] == "foo==1.0"
    assert not heal._pending_file().exists()

    calls = _fake_pip(monkeypatch, heal, rc=0)
    assert heal.heal() == 0
    assert calls == []


def test_broken_pip_is_repaired_before_reinstall(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = _fake_pip(monkeypatch, heal, rc=0)
    monkeypatch.setattr(heal, "_pip_works", lambda: False)
    monkeypatch.setattr(heal, "_repair_pip", lambda _site: False)
    assert heal.heal() == 2
    assert calls == []
    monkeypatch.setattr(heal, "_repair_pip", lambda _site: True)
    assert heal.heal() == 1


@pytest.mark.parametrize(
    "damaged",
    [b"", b"\0" * 120, b"home = /usr/bin\n"],
    ids=["empty", "nul", "no-isolation"],
)
def test_damaged_pyvenv_cfg_is_rewritten(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch, damaged: bytes
) -> None:
    cfg = Path(heal.sys.prefix, "pyvenv.cfg")
    cfg.write_bytes(damaged)  # empty or no isolation line: system dist-packages leak in
    calls = _fake_pip(monkeypatch, heal, rc=0)
    assert heal.heal() == 2  # `venv --upgrade` did not fix it: nothing else runs
    assert calls[-1][1:] == [
        "-m",
        "venv",
        "--upgrade",
        "--without-pip",
        heal.sys.prefix,
    ]

    def run(_argv, **_kw):
        cfg.write_text(_CFG)
        return types.SimpleNamespace(returncode=0)

    monkeypatch.setattr(heal, "subprocess", types.SimpleNamespace(run=run))
    assert heal.heal() == 1
    assert heal.heal() == 0


def test_refuses_outside_a_venv(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = _fake_pip(monkeypatch, heal, rc=0)
    monkeypatch.setattr(heal.sys, "base_prefix", heal.sys.prefix)
    assert heal.heal() == 2
    assert calls == []


def test_pins_installed(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    have = {"requests": "2.34.2", "certifi": "2026.10.23"}

    def version(name: str) -> str:
        if name not in have:
            raise heal.importlib.metadata.PackageNotFoundError(name)
        return have[name]

    monkeypatch.setattr(heal.importlib.metadata, "version", version)
    reqs = tmp_path / "requirements.txt"
    reqs.write_text("# pins\nrequests==2.34.2\ncertifi==2026.10.23 ; python_version\n")
    assert heal.pins_installed(reqs) == 0
    have["requests"] = "2.32.0"  # pip exited 0 but the old version stayed
    assert heal.pins_installed(reqs) == 1
    del have["requests"]
    assert heal.pins_installed(reqs) == 1
