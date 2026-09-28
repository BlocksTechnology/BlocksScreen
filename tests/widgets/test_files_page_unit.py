"""FilesPage list build, sorting and selection."""

import importlib.util
import sys
from pathlib import Path

import pytest

# tests/network conftest stubs list_model globally; force the real one.
_lm_path = Path(__file__).resolve().parents[2] / "BlocksScreen/lib/utils/list_model.py"
_spec = importlib.util.spec_from_file_location("lib.utils.list_model", _lm_path)
_lm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lm)
sys.modules["lib.utils.list_model"] = _lm

# Its BlocksComboBox stub lacks set_options; force the real one too.
_bc_path = (
    Path(__file__).resolve().parents[2] / "BlocksScreen/lib/utils/blocks_combobox.py"
)
_bc_spec = importlib.util.spec_from_file_location("lib.utils.blocks_combobox", _bc_path)
_bc = importlib.util.module_from_spec(_bc_spec)
_bc_spec.loader.exec_module(_bc)
sys.modules["lib.utils.blocks_combobox"] = _bc

from lib.panels.widgets.filesPage import FilesPage  # noqa: E402
from lib.utils.list_model import ListItem  # noqa: E402


@pytest.fixture()
def page(qtbot):
    """FilesPage with a live model, no backend."""
    w = FilesPage()
    qtbot.addWidget(w)
    return w


def _texts(page):
    """Row display texts in model order."""
    return [e.text for e in page._model.entries]


class TestBuildFileList:
    def test_root_sorts_dirs_alpha_then_files_by_last_print_desc(self, page):
        page._curr_dir = ""
        page._directories = [{"dirname": "beta"}, {"dirname": "alpha"}]
        page._file_list = [
            {"filename": "old.gcode", "modified": 1},
            {"filename": "new.gcode", "modified": 9},
        ]
        page._files_data["old.gcode"] = {"print_start_time": 1}
        page._files_data["new.gcode"] = {"print_start_time": 9}
        page._build_file_list()
        assert _texts(page) == ["alpha", "beta", "new", "old"]

    def test_never_printed_files_are_newest_upload_first(self, page):
        page._curr_dir = ""
        page._file_list = [
            {"filename": "old.gcode", "modified": 1},
            {"filename": "new.gcode", "modified": 9},
            {"filename": "done.gcode", "modified": 5},
        ]
        page._files_data["done.gcode"] = {"print_start_time": 3}
        page._build_file_list()
        assert _texts(page) == ["done", "new", "old"]

    def test_subdirectory_prepends_go_back(self, page):
        page._curr_dir = "sub"
        page._directories = []
        page._file_list = [{"filename": "sub/a.gcode", "modified": 1}]
        page._build_file_list()
        assert _texts(page)[0] == "Go Back"

    def test_hidden_dotdirs_excluded(self, page):
        page._curr_dir = ""
        page._directories = [{"dirname": ".thumbs"}, {"dirname": "visible"}]
        page._file_list = []
        page._build_file_list()
        assert _texts(page) == ["visible"]

    def test_empty_root_shows_placeholder(self, page):
        page._curr_dir = ""
        page._directories = []
        page._file_list = []
        page._build_file_list()
        assert page._model.rowCount() == 0
        assert page._label.isVisible() or not page._list_widget.isVisibleTo(page)

    def test_uncached_file_shows_unknown_right_text(self, page):
        page._curr_dir = ""
        page._file_list = [{"filename": "cube.gcode", "modified": 5}]
        page._build_file_list()
        assert page._model.entries[0].right_text == "Unknown Filament - Unknown time"

    def test_cached_file_renders_filament_and_time(self, page):
        page._curr_dir = ""
        page._file_list = [{"filename": "cube.gcode", "modified": 5}]
        page._files_data["cube.gcode"] = {
            "filename": "cube.gcode",
            "estimated_time": 3600,
            "filament_type": "PLA",
            "modified": 5,
        }
        page._build_file_list()
        assert page._model.entries[0].right_text == "PLA - 1h 0m"


class TestItemKey:
    def test_namespaces_dirs_and_files(self, page):
        d = ListItem(text="folder", left_icon=object())
        f = ListItem(text="folder", left_icon=None)
        assert page._item_key(d) == "d:folder"
        assert page._item_key(f) == "f:folder"


class TestSelection:
    def test_file_selection_emits_file_selected(self, page, qtbot):
        """file_selected carries the full path."""
        page._curr_dir = ""
        page._file_list = [{"filename": "cube.gcode", "modified": 5}]
        page._build_file_list()
        item = page._model.entries[0]
        with qtbot.waitSignal(page.file_selected, timeout=500) as sig:
            page._on_item_selected(item)
        assert sig.args[0] == "cube.gcode"

    def test_directory_selection_navigates(self, page, qtbot):
        page._curr_dir = ""
        page._directories = [{"dirname": "alpha"}]
        page._file_list = []
        page._build_file_list()
        item = page._model.entries[0]
        with qtbot.waitSignal(page.request_dir_info[str], timeout=500):
            page._on_item_selected(item)
        assert page._curr_dir == "/alpha"


class TestIncrementalHandlers:
    def test_on_file_added_appends_to_backing_and_lists(self, page):
        page._curr_dir = ""
        page.on_file_added({"filename": "a.gcode", "modified": 3})
        page._build_file_list()
        assert "a" in _texts(page)

    def test_on_file_removed_drops_row(self, page):
        page._curr_dir = ""
        page._file_list = [{"filename": "a.gcode", "modified": 3}]
        page._build_file_list()
        page.on_file_removed("a.gcode")
        page._build_file_list()
        assert "a" not in _texts(page)

    def test_on_dir_added_appends_dir(self, page):
        page._curr_dir = ""
        page.on_dir_added({"dirname": "newdir"})
        page._build_file_list()
        assert "newdir" in _texts(page)

    def test_on_dir_removed_drops_dir(self, page):
        page._curr_dir = ""
        page._directories = [{"dirname": "d1"}]
        page._build_file_list()
        page.on_dir_removed("d1")
        page._build_file_list()
        assert "d1" not in _texts(page)

    def test_on_dir_removed_nested_keeps_same_named_root_dir(self, page):
        page._curr_dir = ""
        page._directories = [{"dirname": "d1"}]
        page.on_dir_removed("sub/d1")
        page._build_file_list()
        assert "d1" in _texts(page)

    def test_on_dir_removed_drops_child_of_current_dir(self, page):
        page._curr_dir = "/sub"
        page._directories = [{"dirname": "d1"}]
        page.on_dir_removed("sub/d1")
        page._build_file_list()
        assert "d1" not in _texts(page)

    def test_on_dir_removed_ancestor_of_current_returns_to_root(self, page, qtbot):
        page._curr_dir = "/sub/d1"
        with qtbot.waitSignal(page.request_dir_info[str], timeout=500) as sig:
            page.on_dir_removed("sub")
        assert sig.args == [""]
        assert page._curr_dir == ""

    def test_on_dir_added_without_dirname_uses_basename(self, page):
        """Moonraker dir notifications carry only a path."""
        page._curr_dir = "/sub"
        page.on_dir_added({"path": "sub/newdir"})
        page._build_file_list()
        assert "newdir" in _texts(page)

    def test_on_usb_removed_inside_unlabelled_stick_returns_to_root(self, page, qtbot):
        """Unlabelled sticks link as 'USB DRIVE'."""
        page._curr_dir = "/USB DRIVE/sub"
        with qtbot.waitSignal(page.request_dir_info[str], timeout=500) as sig:
            page.on_usb_removed()
        assert sig.args == [""]
        assert page._curr_dir == ""

    def test_on_usb_removed_other_drive_stays_put(self, page, qtbot):
        """Pulling USB-B must not eject a user browsing USB-A."""
        page._curr_dir = "/USB-A/sub"
        with qtbot.waitSignal(page.request_dir_info[str], timeout=500) as sig:
            page.on_usb_removed("/home/pi/printer_data/gcodes/USB-B")
        assert sig.args == ["/USB-A/sub"]
        assert page._curr_dir == "/USB-A/sub"

    def test_on_usb_removed_own_drive_returns_to_root(self, page, qtbot):
        page._curr_dir = "/USB-A/sub"
        with qtbot.waitSignal(page.request_dir_info[str], timeout=500) as sig:
            page.on_usb_removed("/home/pi/printer_data/gcodes/USB-A")
        assert sig.args == [""]

    def test_delete_in_other_dir_keeps_same_named_file(self, page):
        """_file_list holds bare names; only the current dir's may go."""
        page._file_list = [{"filename": "a.gcode"}]
        page.on_file_removed("sub/a.gcode")
        assert page._file_list == [{"filename": "a.gcode"}]
        page.on_file_removed("a.gcode")
        assert page._file_list == []

    def test_on_file_added_in_subdir_renders_metadata(self, page):
        """Stored as a bare name so metadata still resolves."""
        page._curr_dir = "/sub"
        page.on_file_added({"path": "sub/a.gcode", "modified": 3})
        page.on_fileinfo(
            {"filename": "sub/a.gcode", "estimated_time": 3600, "filament_type": "PLA"}
        )
        page._build_file_list()
        assert page._model.entries[-1].right_text == "PLA - 1h 0m"

    def test_on_file_removed_in_subdir_drops_row(self, page):
        """A full-path notify still drops the bare-named row."""
        page._curr_dir = "/sub"
        page._file_list = [{"filename": "a.gcode", "modified": 3}]
        page._build_file_list()
        page.on_file_removed("sub/a.gcode")
        page._build_file_list()
        assert "a" not in _texts(page)

    def test_on_fileinfo_caches_then_renders_metadata(self, page):
        page._curr_dir = ""
        page._file_list = [{"filename": "cube.gcode", "modified": 5}]
        page._build_file_list()
        page.on_fileinfo(
            {"filename": "cube.gcode", "estimated_time": 3600, "filament_type": "PLA"}
        )
        page._build_file_list()
        assert page._model.entries[0].right_text == "PLA - 1h 0m"

    def test_on_directories_keeps_metadata(self, page):
        """Files emits metadata once, so a relisting must not drop it."""
        page.on_fileinfo({"filename": "a.gcode", "estimated_time": 60})
        page.on_directories([])
        assert "a.gcode" in page._files_data

    def test_on_dir_removed_forgets_only_its_metadata(self, page):
        for name in ("sub/x.gcode", "subway/y.gcode", "z.gcode"):
            page.on_fileinfo({"filename": name})
        page.on_dir_removed("sub")
        assert set(page._files_data) == {"subway/y.gcode", "z.gcode"}


class TestSorting:
    def test_combobox_lists_all_sorting_types(self, page):
        options = [
            page._sort_combo.itemText(i) for i in range(page._sort_combo.count())
        ]
        assert options == list(FilesPage.SORTING_TYPES)

    def test_sort_by_name_ascending(self, page):
        page._curr_dir = ""
        page._file_list = [
            {"filename": "banana.gcode", "modified": 9},
            {"filename": "apple.gcode", "modified": 1},
        ]
        page._sort_descending = False
        page._sort_combo.setCurrentText("Name")
        assert _texts(page) == ["apple", "banana"]

    def test_last_print_descending_is_most_recent_first(self, page):
        page._curr_dir = ""
        page._file_list = [
            {"filename": "old.gcode", "modified": 1},
            {"filename": "new.gcode", "modified": 9},
        ]
        page._files_data["old.gcode"] = {"print_start_time": 1}
        page._files_data["new.gcode"] = {"print_start_time": 9}
        assert page._sort_key == "Last Print"
        page._build_file_list()
        assert _texts(page) == ["new", "old"]

    def test_order_toggle_reverses_list(self, page):
        page._curr_dir = ""
        page._file_list = [
            {"filename": "apple.gcode", "modified": 1},
            {"filename": "banana.gcode", "modified": 9},
        ]
        page._sort_combo.setCurrentText("Name")  # descending default -> Z..A
        assert _texts(page) == ["banana", "apple"]
        page._on_sort_order_toggled()
        assert page._sort_descending is False
        assert _texts(page) == ["apple", "banana"]

    def test_sort_import_order_is_newest_upload_first(self, page):
        """Moonraker's listing order is arbitrary; mtime is the upload time."""
        page._curr_dir = ""
        page._file_list = [
            {"filename": "zeta.gcode", "modified": 1},
            {"filename": "alpha.gcode", "modified": 9},
        ]
        page._sort_combo.setCurrentText("Import Order")
        assert _texts(page) == ["alpha", "zeta"]
        page._on_sort_order_toggled()
        assert _texts(page) == ["zeta", "alpha"]

    def test_sort_by_nozzle_size(self, page):
        page._curr_dir = ""
        page._file_list = [
            {"filename": "big.gcode", "modified": 1},
            {"filename": "small.gcode", "modified": 2},
        ]
        page._files_data["big.gcode"] = {"nozzle_diameter": 0.8}
        page._files_data["small.gcode"] = {"nozzle_diameter": 0.4}
        page._sort_descending = False
        page._sort_combo.setCurrentText("Nozzle Size")
        assert _texts(page) == ["small", "big"]
