"""Update page widget — displays component status from the D-Bus updater daemon."""

import json
import logging
import typing
from types import MappingProxyType

from PyQt6 import QtCore, QtGui, QtWidgets

from BlocksScreen.lib.panels.widgets.basePopup import BasePopup
from BlocksScreen.lib.panels.widgets.loadWidget import LoadingOverlayWidget
from BlocksScreen.lib.utils.blocks_button import BlocksCustomButton
from BlocksScreen.lib.utils.blocks_Scrollbar import CustomScrollBar
from BlocksScreen.lib.utils.icon_button import IconButton
from updater.models import ComponentStatus

_log = logging.getLogger(__name__)


class UpdatePage(QtWidgets.QWidget):
    request_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request-update"
    )
    request_status: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-status"
    )
    request_cancel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-cancel"
    )
    update_available: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="update-available"
    )
    call_load_panel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, str, name="call-load-panel"
    )
    disable_popups: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="disable-popups"
    )

    _STEP_LABELS: typing.ClassVar[MappingProxyType[int, str]] = MappingProxyType(
        {
            1: "fetching",
            2: "pulling",
            3: "installing deps",
            4: "restarting",
        }
    )

    _APT_STEP_LABELS: typing.ClassVar[MappingProxyType[int, str]] = MappingProxyType(
        {1: "updating packages", 2: "upgrading packages"}
    )

    def __init__(self) -> None:
        super().__init__()
        self._chevron_right: QtGui.QPixmap = QtGui.QPixmap()
        self._chevron_down: QtGui.QPixmap = QtGui.QPixmap()
        self._setupUI()
        self._statuses: dict[str, ComponentStatus] = {}
        self._font_cache: dict[int, QtGui.QFont] = {}
        self._chevron_btn: IconButton | None = None
        self._details_widget: QtWidgets.QWidget | None = None
        self.update_all_btn.clicked.connect(self.on_update_all_clicked)
        self.update_back_btn.clicked.connect(self._request_status_debounced)
        self._status_debounce: QtCore.QTimer = QtCore.QTimer(self)
        self._status_debounce.setSingleShot(True)
        self._status_debounce.timeout.connect(self.request_status.emit)
        self.reload_btn.clicked.connect(self._request_status_debounced)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self._busy: bool = False
        self._printing_state: str = ""
        self._heaters: dict[str, float] = {}
        self._update_avail: bool = False
        self._post_update_status_pending: bool = False
        self._overlay_shown: bool = False
        self._elapsed_time_seconds: int = 0
        self._elapsed_timer: QtCore.QTimer = QtCore.QTimer(self)
        self._elapsed_timer.setSingleShot(False)
        self._elapsed_timer.setInterval(1000)
        self._elapsed_timer.timeout.connect(self._update_elapsed_time)
        self._busy_timeout_timer: QtCore.QTimer = QtCore.QTimer(self)
        self._busy_timeout_timer.setSingleShot(True)
        self._busy_timeout_timer.setInterval(400_000)  # 400s > 360s watchdog
        self._busy_timeout_timer.timeout.connect(self._on_busy_timeout)
        self._update_confirm_popup: BasePopup | None = None
        self.show_loading(True)

    def _request_status_debounced(self) -> None:
        self._status_debounce.start(500)

    def set_printing_state(self, key: str, value: str) -> None:
        """Cache the printer state so update safety checks can block mid-print updates."""
        if key == "state":
            self._printing_state = value

    def set_heater_target(self, name: str, prop: str, value: float) -> None:
        """Track heater targets; update is blocked if any heater is above 40 °C."""
        if prop == "target":
            self._heaters[name] = value

    def _update_elapsed_time(self) -> None:
        """Update and display elapsed time counter."""
        self._elapsed_time_seconds += 1
        minutes = self._elapsed_time_seconds // 60
        seconds = self._elapsed_time_seconds % 60
        self._elapsed_time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def _on_busy_timeout(self) -> None:
        """Force-dismiss overlay if update takes longer than 400s (safety net)."""
        if self._busy:
            _log.warning("busy timeout: force-dismissing overlay after 400s")
            self._busy = False
            self._overlay_shown = False
            self.show_loading(False)
            self.call_load_panel.emit(False, "")

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        """Rebuild cards and request a fresh status poll each time the page becomes visible."""
        self.build_cards()
        self._post_update_status_pending = True
        self._request_status_debounced()
        return super().showEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Position elapsed time label and cancel button within the load widget area."""
        if self._loadwidget.isVisible():
            load_widget_height = self._loadwidget.height()
            load_widget_width = self._loadwidget.width()
            elapsed_y = int(load_widget_height * 0.65)
            elapsed_x = (load_widget_width - 200) // 2
            self._elapsed_time_label.setGeometry(elapsed_x, elapsed_y, 200, 40)
            progress_y = int(load_widget_height * 0.72)
            progress_x = (load_widget_width - 200) // 2
            self._progress_label.setGeometry(progress_x, progress_y, 200, 30)
            cancel_y = int(load_widget_height * 0.81)
            cancel_x = (load_widget_width - 280) // 2
            self._cancel_btn.setGeometry(cancel_x, cancel_y, 280, 60)
        return super().resizeEvent(a0)

    def _needs_update(self, status: ComponentStatus) -> bool:
        # Mirrors the daemon's dirty-set in _run_update_all: an errored git repo
        # (e.g. a corrupt repo) is included so the one "Update" button shows and
        # the update flow self-heals it. apt errors are not repairable this way.
        return bool(
            status.commits_behind
            or status.packages_upgradable > 0
            or status.has_local_changes
            or (status.error is not None and status.kind != "apt")
        )

    def _version_string(self, status: ComponentStatus) -> str:
        if status.error:
            return "status error"
        if status.kind in ("system", "apt"):
            return "updates available"
        current = status.current_version or status.current_hash[:8]
        return f"{current} → {status.remote_version or 'unknown'}"

    def _make_white_label(
        self,
        text: str,
        size: int,
        align: QtCore.Qt.AlignmentFlag = (
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft
        ),
    ) -> QtWidgets.QLabel:
        label = QtWidgets.QLabel(text, self)
        if size not in self._font_cache:
            self._font_cache[size] = QtGui.QFont(self._font_family, size)
        label.setFont(self._font_cache[size])
        label.setStyleSheet("color: #FFFFFF;")
        label.setAlignment(align)
        return label

    def _status_color(self, status: ComponentStatus) -> str:
        return "#ffd54f" if status.has_local_changes else "#ef5350"

    def build_cards(self) -> None:
        """Tear down and rebuild component cards from the current ``_statuses`` snapshot."""
        self._chevron_btn = None
        self._details_widget = None
        while self._cards_layout.count():
            item = self._cards_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        updatable = {n: s for n, s in self._statuses.items() if self._needs_update(s)}
        errored = {
            n: s
            for n, s in self._statuses.items()
            if s.error and not self._needs_update(s)
        }
        self._update_avail = bool(updatable)
        self.update_all_btn.setVisible(self._update_avail)

        if not updatable:
            if not self._statuses:
                text = "No update information available\nTap refresh to retry"
            elif errored:
                text = (
                    f"Status check failed for {len(errored)} "
                    f"component{'s' if len(errored) != 1 else ''}\nTap refresh to retry"
                )
            else:
                text = "All systems up to date"
            label = self._make_white_label(
                text,
                22,
                QtCore.Qt.AlignmentFlag.AlignCenter,
            )
            label.setStyleSheet("color: rgba(255, 255, 255, 160);")
            self._cards_layout.addStretch(1)
            self._cards_layout.addWidget(
                label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
            )
            self._cards_layout.addStretch(1)
            return

        self._cards_layout.addWidget(self._make_summary_row(updatable))
        self._details_widget = self._make_details_widget({**updatable, **errored})
        self._details_widget.setVisible(False)
        self._cards_layout.addWidget(self._details_widget)
        self._cards_layout.addStretch(1)

    def _make_summary_row(
        self, updatable: dict[str, ComponentStatus]
    ) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setFixedHeight(68)
        card.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        card.setObjectName("updateCard")
        card.setStyleSheet(
            "QFrame#updateCard {"
            " background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
            " stop:0 rgba(255,255,255,0.13), stop:1 rgba(255,255,255,0.04));"
            " border: 1px solid rgba(255,255,255,0.22); border-radius: 10px; }"
        )
        row = QtWidgets.QHBoxLayout(card)
        row.setContentsMargins(16, 0, 16, 0)
        row.setSpacing(12)
        row.addWidget(self._make_white_label("BlocksScreen", 22), 1)
        n = len(updatable)
        row.addWidget(
            self._make_white_label(
                f"{n} update{'s' if n != 1 else ''}",
                16,
                QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
            ),
            0,
        )
        self._chevron_btn = IconButton(card)
        self._chevron_btn.setFixedSize(50, 50)
        self._chevron_btn.setFlat(True)
        self._chevron_btn.setPixmap(self._chevron_right)
        self._chevron_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._chevron_btn.clicked.connect(self._toggle_details)
        row.addWidget(self._chevron_btn)
        return card

    def _make_details_widget(
        self, updatable: dict[str, ComponentStatus]
    ) -> QtWidgets.QWidget:
        container = QtWidgets.QWidget()
        container.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        container.setStyleSheet("background: transparent;")
        vbox = QtWidgets.QVBoxLayout(container)
        vbox.setContentsMargins(8, 4, 8, 4)
        vbox.setSpacing(4)
        for name, status in updatable.items():
            if status.kind == "system":
                continue
            row_w = QtWidgets.QWidget()
            row_w.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
            row_w.setFixedHeight(36)
            row = QtWidgets.QHBoxLayout(row_w)
            row.setContentsMargins(12, 0, 8, 0)
            row.setSpacing(10)
            dot = QtWidgets.QLabel(row_w)
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(
                f"background: {self._status_color(status)}; border-radius: 5px;"
            )
            row.addWidget(dot, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
            row.addWidget(self._make_white_label(name.title(), 13), 1)
            row.addWidget(
                self._make_white_label(
                    self._version_string(status),
                    11,
                    QtCore.Qt.AlignmentFlag.AlignRight
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                ),
                0,
            )
            vbox.addWidget(row_w)
        return container

    @QtCore.pyqtSlot(name="toggle-details")
    def _toggle_details(self) -> None:
        if self._details_widget is None or self._chevron_btn is None:
            return
        visible = not self._details_widget.isVisible()
        self._details_widget.setVisible(visible)
        self._chevron_btn.setPixmap(
            self._chevron_down if visible else self._chevron_right
        )

    def handle_status_ready(self, json_str: str) -> None:
        """Update component statuses from a JSON payload and refresh the list."""
        self.update_all_btn.setEnabled(True)
        _log.debug("handle_status_ready: busy=%s", self._busy)
        try:
            data: dict[str, dict] = json.loads(json_str)
            self._statuses = {
                name: ComponentStatus(**fields) for name, fields in data.items()
            }
        except (json.JSONDecodeError, TypeError) as exc:
            _log.error("handle_status_ready: bad payload '%s'", exc)
            _log.debug(json_str)
            return
        _update_avail = any(self._needs_update(s) for s in self._statuses.values())
        self._update_avail = _update_avail
        if not self._busy:
            self.show_loading(False)
            if self._post_update_status_pending:
                _log.debug("status_ready: emitting call_load_panel(False)")
                self.call_load_panel.emit(False, "")
                self._post_update_status_pending = False
        else:
            _log.debug("status_ready: skipping loadscreen dismiss (busy=True)")
        self.build_cards()
        self.update_available.emit(_update_avail)

    def handle_busy_changed(self, busy: bool) -> None:
        """Show loading overlay while an update is in progress; poll for fresh status when done."""
        _log.info("handle_busy_changed: %s", busy)
        self._busy = busy
        self.show_loading(busy)
        if busy:
            self._elapsed_time_seconds = 0
            self._elapsed_timer.start()
            self._busy_timeout_timer.start()
            self._elapsed_time_label.show()
            self._progress_label.setText("")
            self._progress_label.show()
            self._cancel_btn.show()
        else:
            self._elapsed_timer.stop()
            self._busy_timeout_timer.stop()
            self._elapsed_time_label.hide()
            self._progress_label.hide()
            self._cancel_btn.hide()
            self.update_all_btn.setEnabled(True)
            if self._overlay_shown:
                self._overlay_shown = False
                self.call_load_panel.emit(False, "")
            self._request_status_debounced()

    @QtCore.pyqtSlot(name="on-update-all-clicked")
    def on_update_all_clicked(self) -> None:
        """Guard against updates during a print or with hot heaters; otherwise show confirm dialog."""
        _SAFE_STATES = {"standby", "complete", "cancelled", "error", ""}
        if self._printing_state not in _SAFE_STATES:
            self._show_toast(f"Printer {self._printing_state} - update deferred")
            return
        hot = [n for n, t in self._heaters.items() if t > 40.0]
        if hot:
            self._show_toast(
                f"Heaters active ({', '.join(hot)}) - let it cool before updating"
            )
            return
        self._show_update_confirm()

    def _show_update_confirm(self) -> None:
        popup = BasePopup(self, floating=True)
        popup.set_message(
            "The printer will restart.\n"
            "Do not turn off the printer.\n"
            "The update may take a few minutes."
        )
        popup.confirm_button_text("Update")
        popup.cancel_button_text("Cancel")
        popup.accepted.connect(self._do_update)
        self._update_confirm_popup = popup
        popup.open()

    @QtCore.pyqtSlot(name="on-cancel-clicked")
    def _on_cancel_clicked(self) -> None:
        """Emit cancel signal when user clicks cancel button."""
        _log.info("Cancel button clicked")
        self.request_cancel.emit()

    @QtCore.pyqtSlot(name="do-update")
    def _do_update(self) -> None:
        self._overlay_shown = True
        self.request_update.emit("")
        self.call_load_panel.emit(True, "Updating all components ...")

    @QtCore.pyqtSlot(str, int, int, name="handle-step-complete")
    def handle_step_complete(self, name: str, step: int, total: int) -> None:
        """Forward step progress to the load panel overlay with a human-readable label."""
        status = self._statuses.get(name)
        if status and status.kind == "apt":
            label = self._APT_STEP_LABELS.get(step, "working")
        else:
            label = self._STEP_LABELS.get(step, "working")
        _log.info("step_complete: %s %d/%d (%s)", name, step, total, label)
        # Progress = daemon liveness; push the force-dismiss deadline out.
        if self._busy_timeout_timer.isActive():
            self._busy_timeout_timer.start()
        self._overlay_shown = True
        overlay_msg = f"{name}: {label}"
        self._progress_label.setText(f"Step {step}/{total}")
        self.call_load_panel.emit(True, overlay_msg)

    def _show_toast(self, message: str, *, success: bool = False) -> None:
        color = "#4caf50" if success else "#ef5350"
        self._toast.setStyleSheet(
            f"background: {color}; color: #fff; padding: 4px 12px; border-radius: 8px;"
        )
        self._toast.setText(message)
        self._toast.show()
        self._toast.raise_()
        self._toast_timer.start()

    def handle_error_occurred(self, name: str, reason: str) -> None:
        """Show a toast with the error reason and prompt the user to refresh."""
        error_msg = f"{name} update failed: {reason}. Tap refresh to retry."
        self._show_toast(error_msg)

    def handle_rollback_done(self, name: str, success: bool) -> None:
        """Show a success or failure toast after an automatic rollback completes."""
        self._show_toast(
            f"{name}: {'rolled back' if success else 'rollback failed'}",
            success=success,
        )

    def handle_recover_done(self, name: str, success: bool) -> None:
        """Show a success or failure toast after a manual recovery action completes."""
        self._show_toast(
            f"{name}: recovery {'complete' if success else 'failed'}", success=success
        )

    @QtCore.pyqtSlot(name="handle-daemon-unavailable")
    def handle_daemon_unavailable(self) -> None:
        """Show critical error when D-Bus daemon is unreachable."""
        self._busy = False
        self._busy_timeout_timer.stop()
        self._elapsed_timer.stop()
        self._elapsed_time_label.hide()
        self._progress_label.hide()
        self._cancel_btn.hide()
        self.show_loading(False)
        self._show_toast(
            "Updater unavailable. Check system logs or restart BlocksScreen.",
            success=False,
        )
        self.update_all_btn.setEnabled(False)
        self.reload_btn.setEnabled(True)

    def show_loading(self, loading: bool = False) -> None:
        """Toggle between the spinner overlay and the scrollable component list."""
        self.setUpdatesEnabled(False)
        self._loadwidget.setVisible(loading)
        self._scroll_area.setVisible(not loading)
        self.update_all_btn.setVisible(not loading and self._update_avail)
        self.setUpdatesEnabled(True)
        self.disable_popups.emit(loading)

    def _setupUI(self) -> None:
        bold_id = QtGui.QFontDatabase.addApplicationFont(
            ":/font/media/fonts for text/Momcake-Bold.ttf"
        )
        self._font_family = QtGui.QFontDatabase.applicationFontFamilies(bold_id)[0]
        thin_id = QtGui.QFontDatabase.addApplicationFont(
            ":/font/media/fonts for text/Momcake-Thin.ttf"
        )
        thin_families = QtGui.QFontDatabase.applicationFontFamilies(thin_id)
        _title_family = thin_families[0] if thin_families else ""

        self.setObjectName("updatePage")
        self.setStyleSheet(
            "#updatePage { background-image: url(:/background/media/1st_background.png); }"
        )
        self.setMinimumSize(QtCore.QSize(600, 360))
        sp = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sp.setHorizontalStretch(1)
        sp.setVerticalStretch(1)
        self.setSizePolicy(sp)

        content = QtWidgets.QVBoxLayout(self)
        content.setContentsMargins(15, 15, 15, 15)

        header = QtWidgets.QHBoxLayout()
        header.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.reload_btn = IconButton(self)
        # Touch target: 66×66 px (minimum 44×44 per WCAG, 60+ for kiosk)
        self.reload_btn.setFixedSize(QtCore.QSize(66, 66))
        self.reload_btn.setFlat(True)
        self.reload_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/refresh.svg"))
        header.addWidget(self.reload_btn)

        title = QtWidgets.QLabel("Update Manager", self)
        _title_font = QtGui.QFont(_title_family, 24)
        title.setFont(_title_font)
        title.setMinimumSize(QtCore.QSize(100, 60))
        title.setMaximumSize(QtCore.QSize(16777215, 60))
        title.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Preferred,
            )
        )
        pal = title.palette()
        pal.setColor(pal.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        title.setPalette(pal)
        title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header.addWidget(title)

        self.update_back_btn = IconButton(self)
        # Touch target: 66×66 px for consistency with reload button
        self.update_back_btn.setFixedSize(QtCore.QSize(66, 66))
        self.update_back_btn.setFlat(True)
        self.update_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        header.addWidget(self.update_back_btn)
        content.addLayout(header, 0)

        self._scroll_area = QtWidgets.QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setStyleSheet("background: transparent;")
        self._scroll_area.setVerticalScrollBar(CustomScrollBar())
        QtWidgets.QScroller.grabGesture(
            self._scroll_area.viewport(),
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )

        self._scroll_content = QtWidgets.QWidget()
        self._scroll_content.setStyleSheet("background: transparent;")
        self._cards_layout = QtWidgets.QVBoxLayout(self._scroll_content)
        self._cards_layout.setContentsMargins(8, 8, 8, 8)
        self._cards_layout.setSpacing(8)
        self._cards_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self._scroll_area.setWidget(self._scroll_content)
        content.addWidget(self._scroll_area, 1)

        self._loadwidget = LoadingOverlayWidget(
            self, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )
        content.addWidget(self._loadwidget, 1)

        self._elapsed_time_label = QtWidgets.QLabel("00:00", self._loadwidget)
        self._elapsed_time_label.setStyleSheet(
            "color: rgba(255, 255, 255, 200); background: transparent;"
        )
        self._elapsed_time_label.setFont(QtGui.QFont(self._font_family, 16))
        self._elapsed_time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._elapsed_time_label.setFixedWidth(100)
        self._elapsed_time_label.hide()

        self._progress_label = QtWidgets.QLabel("", self._loadwidget)
        self._progress_label.setStyleSheet(
            "color: rgba(255, 255, 255, 180); background: transparent;"
        )
        self._progress_label.setFont(QtGui.QFont(self._font_family, 12))
        self._progress_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._progress_label.setWordWrap(True)
        self._progress_label.hide()

        # Touch target size: minimum 44×44 px per WCAG; set to 60px tall for comfort
        self._cancel_btn = BlocksCustomButton(self._loadwidget)
        self._cancel_btn.setMinimumSize(QtCore.QSize(240, 60))
        self._cancel_btn.setMaximumSize(QtCore.QSize(320, 60))
        self._cancel_btn.setFont(QtGui.QFont(self._font_family, 18))
        self._cancel_btn.setText("Cancel")
        self._cancel_btn.clicked.connect(self._on_cancel_clicked)
        self._cancel_btn.hide()

        self.update_all_btn = BlocksCustomButton(self)
        self.update_all_btn.setMinimumSize(QtCore.QSize(240, 70))
        self.update_all_btn.setMaximumSize(QtCore.QSize(360, 70))
        self.update_all_btn.setFont(QtGui.QFont(self._font_family, 22))
        self.update_all_btn.setText("Update")
        self.update_all_btn.setPixmap(
            QtGui.QPixmap(":/system/media/btn_icons/update-software-icon.svg")
        )
        content.addWidget(self.update_all_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_all_btn.hide()

        self._toast = QtWidgets.QLabel(self)
        self._toast.setWordWrap(True)
        self._toast.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._toast.setFont(QtGui.QFont(self._font_family, 13))
        self._toast.setFixedHeight(46)
        self._toast.hide()
        content.addWidget(self._toast, 0)
        self._toast_timer = QtCore.QTimer(self)
        self._toast_timer.setSingleShot(True)
        self._toast_timer.setInterval(12000)
        self._toast_timer.timeout.connect(self._toast.hide)

        _arrow = QtGui.QPixmap(":/arrow_icons/media/btn_icons/arrow_right.svg")
        self._chevron_right: QtGui.QPixmap = _arrow
        self._chevron_down: QtGui.QPixmap = _arrow.transformed(
            QtGui.QTransform().rotate(90),
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
