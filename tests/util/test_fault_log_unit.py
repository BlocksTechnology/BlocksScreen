"""CrashHandler fault log: a SEGV after shutdown still lands in the fault log."""

import subprocess
import sys
import textwrap
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]

_CHILD = textwrap.dedent(
    """
    import faulthandler, sys
    from BlocksScreen.logger import CrashHandler
    fault, other = sys.argv[1], sys.argv[2]
    CrashHandler.install(crash_log_path=fault + ".crash", fault_log_path=fault)
    CrashHandler._instance.uninstall()
    with open(other, "w") as f:
        f.write("unrelated\\n")
        f.flush()
        faulthandler._sigsegv()
    """
)


def _crash_after_uninstall(tmp_path: Path) -> tuple[str, str]:
    fault, other = tmp_path / "fault.log", tmp_path / "other.log"
    fault.write_text("previous run\n")
    proc = subprocess.run(
        [sys.executable, "-c", _CHILD, str(fault), str(other)],
        cwd=_REPO,
        capture_output=True,
        timeout=20,
        check=False,
    )
    assert proc.returncode != 0
    return fault.read_text(), other.read_text()


def test_segv_after_uninstall_goes_to_fault_log(tmp_path):
    fault, other = _crash_after_uninstall(tmp_path)
    assert "Segmentation fault" in fault
    assert "Segmentation fault" not in other


def test_fault_log_keeps_previous_runs_and_marks_each_start(tmp_path):
    fault, _ = _crash_after_uninstall(tmp_path)
    assert fault.startswith("previous run\n--- run started ")
