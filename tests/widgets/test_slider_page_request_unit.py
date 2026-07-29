"""on_slidePage_request must set the slider's range before its position.

Regression coverage for: pressing a control (e.g. Fan, range 0-100) right
after adjusting Speed (range 10-300) during printing showed the wrong
value, because the position was applied while the slider still held the
previous control's range and got clamped.

Uses the real ``SliderPage``/``QSlider`` (this is a Qt range-clamping bug,
not something a stub could reproduce) with the tab classes' unbound
``on_slidePage_request`` called against a minimal stand-in ``self`` --
constructing a full ``PrintTab``/``ControlTab`` pulls in unrelated heavy
UI dependencies (fonts, generated Ui_* files) that this test doesn't need.
"""

import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

# printTab/controlTab import configfile, lib.files, lib.printer purely for
# type hints and passthrough attribute assignment -- stub them so importing
# the tab classes doesn't require the real config/websocket/printer stack.
for _name in ("configfile", "lib.files", "lib.printer"):
    sys.modules.setdefault(_name, types.ModuleType(_name))
sys.modules["configfile"].BlocksScreenConfig = MagicMock
sys.modules["configfile"].get_configparser = MagicMock(return_value=MagicMock())
sys.modules["lib.files"].Files = MagicMock
sys.modules["lib.printer"].Printer = MagicMock

# SliderPage needs the real IconButton (has setPixmap); undo the
# QPushButton stand-in the widgets conftest installs for other tests.
sys.modules.pop("lib.utils.icon_button", None)

# tests/panels/conftest.py permanently stubs these as MagicMock/empty-package
# stand-ins in sys.modules at collection time; when that directory collects
# first, the stubs outlive it for the rest of the session. Evict them so the
# real classes resolve here instead of hitting the empty stub package.
sys.modules.pop("lib.panels.printTab", None)
sys.modules.pop("lib.panels.controlTab", None)
sys.modules.pop("lib.ui", None)
for _stubbed in [_m for _m in sys.modules if _m.startswith("lib.panels.widgets")]:
    sys.modules.pop(_stubbed, None)

from lib.panels.controlTab import ControlTab  # noqa: E402
from lib.panels.printTab import PrintTab  # noqa: E402
from lib.panels.widgets.slider_selector_page import SliderPage  # noqa: E402


@pytest.fixture
def slider_stub(qtbot):
    slider_page = SliderPage(None)
    qtbot.addWidget(slider_page)
    return SimpleNamespace(
        sliderPage=slider_page,
        indexOf=lambda widget: 0,
        change_page=lambda index: None,
    )


class TestOnSlidePageRequestRangeOrdering:
    @pytest.mark.parametrize("tab_class", [PrintTab, ControlTab])
    def test_position_not_clamped_by_stale_range(self, slider_stub, tab_class):
        # Fan slider opened first: range 0-100.
        tab_class.on_slidePage_request(slider_stub, "Fan", 100, lambda v: None, 0, 100)
        # Speed slider opened next: range 10-300, value 150 (outside the
        # stale 0-100 range that must no longer be in effect).
        tab_class.on_slidePage_request(
            slider_stub, "Speed", 150, lambda v: None, 10, 300
        )
        assert slider_stub.sliderPage.slider.value() == 150
