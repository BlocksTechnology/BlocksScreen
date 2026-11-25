"""Fault-injection tests for scripts/bs-venv-heal.py, the power-cut venv repair."""

from __future__ import annotations

import importlib.util
import shutil
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
    monkeypatch.setattr(mod, "_free_mb", lambda: 10**6)  # host disk must not decide
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
    assert dist_info.exists()  # nothing removed before the wheels are local
    assert heal._read_pending() == ["foo==1.0"]
    assert calls[-1][3] == "wheel" and calls[-1][-1] == "foo==1.0"

    _fake_pip(monkeypatch, heal, rc=1)
    assert heal.heal() == 2  # still offline, nothing new: reinstall stays pending
    assert heal._read_pending() == ["foo==1.0"]

    calls = _fake_pip(monkeypatch, heal, rc=0)
    assert heal.heal() == 1
    wheel, install = calls[-2:]
    assert wheel[wheel.index("--no-binary") + 1] == "sdbus,sdbus-networkmanager"
    assert wheel[wheel.index("--only-binary") + 1] == ":all:"
    assert "--force-reinstall" in install and "--no-index" in install
    assert install[-1] == "foo==1.0"
    assert not dist_info.exists()
    assert not heal._pending_file().exists()

    calls = _fake_pip(monkeypatch, heal, rc=0)
    assert heal.heal() == 0
    assert calls == []


def test_offline_heal_keeps_a_dist_whose_code_is_intact(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pip writes dist-info last, so a cut most often leaves only METADATA damaged."""
    site = heal._site_packages()
    dist_info = _dist(site, "foo", "1.0", {"foo/__init__.py": b"x = 1\n"})
    (dist_info / "METADATA").write_bytes(b"")
    _fake_pip(monkeypatch, heal, rc=1)
    assert heal.heal() == 1
    assert (site / "foo/__init__.py").read_bytes() == b"x = 1\n"
    assert heal._read_pending() == ["foo==1.0"]


def test_damaged_dist_is_removed_only_after_its_wheel_is_fetched(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "foo", "1.0", {"foo/__init__.py": b"x = 1\n"})
    (dist_info / "RECORD").write_bytes(b"")
    seen: list[tuple[str, bool]] = []
    monkeypatch.setattr(
        heal,
        "subprocess",
        types.SimpleNamespace(
            run=lambda argv, **_kw: (
                seen.append((argv[3], dist_info.exists()))
                or types.SimpleNamespace(returncode=0)
            )
        ),
    )
    monkeypatch.setattr(heal, "_pip_works", lambda: True)
    assert heal.heal() == 1
    assert seen == [("wheel", True), ("install", False)]
    assert not heal._wheel_dir().exists()


def test_low_disk_defers_the_reinstall_and_keeps_the_dist(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "foo", "1.0", {"foo/__init__.py": b"x" * (2 << 20)})
    (site / "foo/__init__.py").write_bytes(b"")
    calls = _fake_pip(monkeypatch, heal, rc=0)
    monkeypatch.setattr(heal, "_free_mb", lambda: heal._MIN_FREE_MB + 1)
    assert heal.heal() == 1
    assert calls == []  # 2 MB to reinstall on top of the margin: no download
    assert dist_info.exists()
    assert heal._read_pending() == ["foo==1.0"]

    monkeypatch.setattr(heal, "_free_mb", lambda: heal._MIN_FREE_MB + 2)
    assert heal.heal() == 1
    assert [c[3] for c in calls] == ["wheel", "install"]
    assert not heal._pending_file().exists()


def test_pip_repair_needs_ensurepip_before_deleting_pip(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "pip", "23.0.1", {"pip/__init__.py": b"v = 23\n"})
    monkeypatch.setattr(heal.importlib.util, "find_spec", lambda _name: None)
    calls = _fake_pip(monkeypatch, heal, rc=0)
    assert not heal._repair_pip(site)
    assert calls == []
    assert dist_info.exists() and (site / "pip/__init__.py").exists()


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


def test_pip_repair_drops_files_an_emptied_record_no_longer_lists(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "pip", "26.2.1", {"pip/__init__.py": b"v = 26\n"})
    (dist_info / "RECORD").write_bytes(b"")
    # pip 26 made build_env a package; left behind, it shadows the bundled 23.0.1 build_env.py.
    (site / "pip/_internal/build_env").mkdir(parents=True)
    (site / "pip/_internal/build_env/__init__.py").write_bytes(b"")
    stashes = [
        site / n for n in ("~ip", "~ip-23.0.1.dist-info", "~-p-23.0.1.dist-info")
    ]
    for stash in stashes:
        stash.mkdir()
    other = site / "~oo-0.9.dist-info"
    other.mkdir()
    calls = _fake_pip(monkeypatch, heal, rc=0)
    assert heal._repair_pip(site)
    assert calls[-1][1:3] == ["-m", "ensurepip"]
    assert not (site / "pip").exists()
    assert not dist_info.exists()
    # A stale pip stash makes pip's later self-upgrade keep the old dist-info beside the new one.
    assert not any(stash.exists() for stash in stashes)
    assert other.exists()


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


def test_crash_exits_3_not_healed(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Callers treat exit 1 as healed, so a crash must report a distinct code."""
    monkeypatch.setattr(heal, "heal", lambda: 1 // 0)
    monkeypatch.setattr(heal.sys, "argv", ["bs-venv-heal.py"])
    assert heal.main() == 3


def test_free_space_margin_matches_the_updater(heal: types.ModuleType) -> None:
    from updater.models import MIN_FREE_MB

    assert heal._MIN_FREE_MB == MIN_FREE_MB


def test_lost_record_is_sized_from_the_fetched_wheels(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = heal._site_packages()
    dist_info = _dist(site, "foo", "1.0", {"foo/__init__.py": b"x = 1\n"})
    (dist_info / "RECORD").write_bytes(b"")  # estimate before download: 0 MB
    calls = _fake_pip(monkeypatch, heal, rc=0)

    def run(argv, **_kw):
        calls.append(argv)
        if argv[3] == "wheel":
            wheels = Path(argv[argv.index("--wheel-dir") + 1])
            wheels.mkdir()
            with heal.zipfile.ZipFile(wheels / "foo-1.0-py3-none-any.whl", "w") as zf:
                zf.writestr("foo/big.bin", b"\0" * (3 << 20))
        return types.SimpleNamespace(returncode=0)

    monkeypatch.setattr(heal, "subprocess", types.SimpleNamespace(run=run))
    monkeypatch.setattr(heal, "_free_mb", lambda: heal._MIN_FREE_MB + 2)
    assert heal.heal() == 1
    assert [c[3] for c in calls] == ["wheel"]  # 3 MB unpacked: no install
    assert dist_info.exists()
    assert heal._read_pending() == ["foo==1.0"]


def test_pip_repair_queues_the_pip_it_replaced(
    heal: types.ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = heal._site_packages()
    # A cut kept only RECORD's first rows, so the emptied files look intact.
    _dist(site, "pip", "26.2.1", {"pip/__init__.py": b"v = 26\n"})
    calls = _fake_pip(monkeypatch, heal, rc=0)
    monkeypatch.setattr(heal, "_pip_works", lambda: False)

    def repair(site: Path) -> bool:
        shutil.rmtree(site / "pip-26.2.1.dist-info")
        (site / "pip-23.0.1.dist-info").mkdir()
        monkeypatch.setattr(heal, "_pip_works", lambda: True)
        return True

    monkeypatch.setattr(heal, "_repair_pip", repair)
    assert heal.heal() == 1
    assert calls[-1][3] == "install" and calls[-1][-1] == "pip==26.2.1"
    assert not heal._pending_file().exists()
