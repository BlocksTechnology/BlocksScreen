import typing
from collections import OrderedDict
from dataclasses import dataclass

from PyQt6 import QtCore, QtGui, QtWidgets  # pylint: disable=import-error


@dataclass(slots=True)
class ListItem:
    """List item data"""

    text: str
    right_text: str = ""
    _rfontsize: int = 0
    _lfontsize: int = 0

    callback: typing.Optional[typing.Callable] = None

    color: str = "#dfdfdf"
    color_left_icon: bool = False
    right_icon: typing.Optional[QtGui.QPixmap] = None
    left_icon: typing.Optional[QtGui.QPixmap] = None

    selected: bool = False
    allow_check: bool = True

    not_clickable: bool = False

    allow_expand: bool = False
    needs_expansion: bool = False
    is_expanded: bool = False

    height: int = 60
    notificate: bool = False


class EntryListModel(QtCore.QAbstractListModel):
    """List model Subclassed QAbstractListModel"""

    EnableRole = QtCore.Qt.ItemDataRole.UserRole + 1
    NotificateRole = QtCore.Qt.ItemDataRole.UserRole + 2
    ExpandRole = QtCore.Qt.ItemDataRole.UserRole + 3

    def __init__(self, entries=None) -> None:
        """Initialise the model with an optional pre-populated list of ``ListItem``s."""
        super().__init__()
        self.entries: list[ListItem] = entries or []

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        """Gets model row count"""
        return len(self.entries)

    def clear(self) -> None:
        """Clear model rows"""
        self.beginResetModel()
        self.entries.clear()
        self.endResetModel()

    def add_item(self, item: ListItem) -> None:
        """Adds one row item to the model"""
        row = len(self.entries)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.entries.append(item)
        self.endInsertRows()

    def remove_item(self, item: ListItem) -> None:
        """Remove one row item from the model by identity."""
        if item in self.entries:
            index = self.entries.index(item)
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.entries.pop(index)
            self.endRemoveRows()

    def delete_duplicates(self) -> None:
        """Drop entries sharing identical text, color, and last time value."""
        seen: set[tuple[str, str, typing.Any]] = set()
        unique: list[ListItem] = []
        for item in self.entries:
            key = (item.text, item.color, item._cache.get(-1))
            if key not in seen:
                unique.append(item)
                seen.add(key)
        self.beginResetModel()
        self.entries = unique
        self.endResetModel()

    def remove_item_by_text(self, text: str) -> bool:
        """Remove item by text value; True if found, False otherwise."""
        for i, item in enumerate(self.entries):
            if item.text == text:
                self.beginRemoveRows(QtCore.QModelIndex(), i, i)
                self.entries.pop(i)
                self.endRemoveRows()
                return True
        return False

    def insert_item(self, position: int, item: ListItem) -> None:
        """Insert item at a specific position in the model."""
        position = max(0, min(position, len(self.entries)))
        self.beginInsertRows(QtCore.QModelIndex(), position, position)
        self.entries.insert(position, item)
        self.endInsertRows()

    def remove_item_at(self, position: int) -> bool:
        """Remove item at position; True if removed, False if out of range."""
        if position < 0 or position >= len(self.entries):
            return False
        self.beginRemoveRows(QtCore.QModelIndex(), position, position)
        self.entries.pop(position)
        self.endRemoveRows()
        return True

    def get_selected_item(self) -> ListItem | None:
        """Return the currently selected item, or None."""
        for item in self.entries:
            if item.selected:
                return item
        return None

    def update_item_at(self, position: int, item: ListItem) -> bool:
        """Update item at position (left_icon, right_text, right_icon); emit dataChanged."""
        if position < 0 or position >= len(self.entries):
            return False
        existing = self.entries[position]
        existing.left_icon = item.left_icon
        existing.right_text = item.right_text
        existing.right_icon = item.right_icon
        idx = self.index(position)
        self.dataChanged.emit(idx, idx, [QtCore.Qt.ItemDataRole.UserRole])
        return True

    def reconcile(
        self,
        desired: list[ListItem],
        key_fn: typing.Callable[[ListItem], str],
    ) -> None:
        """Diff against desired entries and apply minimal mutations using key_fn."""
        desired_keys = {key_fn(d) for d in desired}
        self._remove_stale_entries(desired_keys, key_fn)

        current_map = self._current_key_map(key_fn)

        for target_idx, desired_item in enumerate(desired):
            if self._apply_desired_item(target_idx, desired_item, current_map, key_fn):
                current_map = self._current_key_map(key_fn)

    def _remove_stale_entries(
        self,
        desired_keys: set[str],
        key_fn: typing.Callable[[ListItem], str],
    ) -> None:
        """Remove entries whose key is not in *desired_keys*."""
        n_existing = len(self.entries)
        stale_count = sum(1 for e in self.entries if key_fn(e) not in desired_keys)
        if stale_count == 0:
            return

        if stale_count > n_existing // 2 and n_existing > 4:
            keep = [e for e in self.entries if key_fn(e) in desired_keys]
            self.beginResetModel()
            self.entries[:] = keep
            self.endResetModel()
        else:
            for i in range(n_existing - 1, -1, -1):
                if key_fn(self.entries[i]) not in desired_keys:
                    self.beginRemoveRows(QtCore.QModelIndex(), i, i)
                    self.entries.pop(i)
                    self.endRemoveRows()

    def _current_key_map(
        self, key_fn: typing.Callable[[ListItem], str]
    ) -> dict[str, int]:
        """Build a ``{key: index}`` map of current entries."""
        return {key_fn(entry): i for i, entry in enumerate(self.entries)}

    def _apply_desired_item(
        self,
        target_idx: int,
        desired_item: ListItem,
        current_map: dict[str, int],
        key_fn: typing.Callable[[ListItem], str],
    ) -> bool:
        """Insert, update, or reposition one item. Returns True if map is now stale."""
        key = key_fn(desired_item)
        current_idx = current_map.get(key)

        if current_idx is not None:
            if current_idx == target_idx:
                self.update_item_at(current_idx, desired_item)
                return False

            self.beginRemoveRows(QtCore.QModelIndex(), current_idx, current_idx)
            self.entries.pop(current_idx)
            self.endRemoveRows()

            self.beginInsertRows(QtCore.QModelIndex(), target_idx, target_idx)
            self.entries.insert(target_idx, desired_item)
            self.endInsertRows()
            return True

        self.beginInsertRows(QtCore.QModelIndex(), target_idx, target_idx)
        self.entries.insert(target_idx, desired_item)
        self.endInsertRows()
        return True

    def flags(self, index) -> QtCore.Qt.ItemFlag:
        """Models item flags, re-implemented method"""
        item = self.entries[index.row()]
        flags = QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
        if item.not_clickable:
            return QtCore.Qt.ItemFlag.NoItemFlags
        if item.allow_check:
            flags |= QtCore.Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def setData(self, index: QtCore.QModelIndex, value: typing.Any, role: int) -> bool:
        """Set data for items, re-implemented method"""
        if not index.isValid():
            return False
        if role == EntryListModel.EnableRole:
            item = self.entries[index.row()]
            item.selected = value
            self.dataChanged.emit(index, index, [EntryListModel.EnableRole])
            return True
        if role == EntryListModel.NotificateRole:
            item = self.entries[index.row()]
            item.notificate = value
            self.dataChanged.emit(index, index, [EntryListModel.NotificateRole])
            return True
        if role == EntryListModel.ExpandRole:
            item = self.entries[index.row()]
            item.is_expanded = value
            self.layoutChanged.emit()
            self.dataChanged.emit(index, index, [EntryListModel.ExpandRole])
        if role == QtCore.Qt.ItemDataRole.UserRole:
            self.dataChanged.emit(index, index, [QtCore.Qt.ItemDataRole.UserRole])
            return True
        return False

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        """Gets item data, re-implemented method"""
        if not index.isValid():
            return None
        item: ListItem = self.entries[index.row()]
        if role == EntryListModel.EnableRole:
            return item.selected
        if role == EntryListModel.NotificateRole:
            return item.notificate
        if role == EntryListModel.ExpandRole:
            return item.is_expanded
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return item
        return None


class EntryDelegate(QtWidgets.QStyledItemDelegate):
    """Renders each item in the view model, provides user interaction to the items"""

    item_selected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        ListItem, name="item-selected"
    )

    def __init__(self) -> None:
        """Initialise the delegate with a scaled-pixmap cache and default item height."""
        super().__init__()
        self.prev_index: int = 0
        self._press_pos: QtCore.QPointF | None = None
        self.height: int = 60
        self._scaled_cache: OrderedDict[tuple[int, int, int], QtGui.QPixmap] = (
            OrderedDict()
        )
        self._tinted_cache: OrderedDict[tuple[int, int, int, str], QtGui.QPixmap] = (
            OrderedDict()
        )
        self._arrow_cache: dict[bool, QtGui.QPixmap] = {}

    def _get_scaled(
        self,
        pixmap: QtGui.QPixmap,
        size: QtCore.QSize,
    ) -> QtGui.QPixmap:
        """Return scaled pixmap (cached by cacheKey, width, height)."""
        key = (pixmap.cacheKey(), size.width(), size.height())
        cached = self._scaled_cache.get(key)
        if cached is not None:
            self._scaled_cache.move_to_end(key)
            return cached
        scaled = pixmap.scaled(
            size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self._scaled_cache[key] = scaled
        # Bound growth: LRU-evict past 64 (covers all wifi/icon variants).
        if len(self._scaled_cache) > 64:
            self._scaled_cache.popitem(last=False)
        return scaled

    def _get_tinted(
        self,
        pixmap: QtGui.QPixmap,
        size: QtCore.QSize,
        color: str,
    ) -> QtGui.QPixmap:
        """Return *pixmap* scaled to *size* and tinted *color*, cached per paint."""
        key = (pixmap.cacheKey(), size.width(), size.height(), color)
        cached = self._tinted_cache.get(key)
        if cached is not None:
            self._tinted_cache.move_to_end(key)
            return cached
        scaled = self._get_scaled(pixmap, size)
        tinted = QtGui.QPixmap(scaled.size())
        tinted.fill(QtCore.Qt.GlobalColor.transparent)
        p = QtGui.QPainter(tinted)
        p.drawPixmap(0, 0, scaled)
        p.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceIn)
        p.fillRect(tinted.rect(), QtGui.QColor(color))
        p.end()
        self._tinted_cache[key] = tinted
        if len(self._tinted_cache) > 64:
            self._tinted_cache.popitem(last=False)
        return tinted

    def _expand_arrow(self, expanded: bool) -> QtGui.QPixmap:
        """Lazily load + cache the expand/collapse arrow pixmap (no per-paint decode)."""
        arrow = self._arrow_cache.get(expanded)
        if arrow is None:
            name = "arrow_down" if expanded else "arrow_right"
            arrow = QtGui.QPixmap(f":/arrow_icons/media/btn_icons/{name}.svg")
            self._arrow_cache[expanded] = arrow
        return arrow

    def clear(self) -> None:
        """Clears delegate indexing"""
        self.prev_index = 0

    def sizeHint(
        self, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex
    ):
        """Calculate size and determine expansion need."""
        item: ListItem = index.data(QtCore.Qt.ItemDataRole.UserRole)
        target_width = option.rect.width()

        base_h = item.height
        ellipse_size = base_h * 0.8

        right_reserved = base_h

        left_reserved = 10
        if item.left_icon:
            left_reserved = (base_h * 0.1) + ellipse_size + 8

        if item._lfontsize > 0 and item._lfontsize != option.font.pointSize():
            f = QtGui.QFont(option.font)
            f.setPointSize(item._lfontsize)
            fm = QtGui.QFontMetrics(f)
        else:
            fm = option.fontMetrics

        if item.right_text:
            if item._rfontsize > 0 and item._rfontsize != option.font.pointSize():
                fr = QtGui.QFont(option.font)
                fr.setPointSize(item._rfontsize)
                fmr = QtGui.QFontMetrics(fr)
            else:
                fmr = option.fontMetrics
            right_reserved += fmr.horizontalAdvance(item.right_text) + 10

        if item.right_icon:
            right_reserved += ellipse_size

        text_avail_width = target_width - left_reserved - right_reserved
        if text_avail_width < 50:
            text_avail_width = 50

        single_line_width = fm.horizontalAdvance(item.text)

        item.needs_expansion = single_line_width > text_avail_width

        if not item.is_expanded:
            return QtCore.QSize(target_width, int(item.height * 1.1))

        text_rect = fm.boundingRect(
            QtCore.QRect(0, 0, int(text_avail_width), 0),
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.TextFlag.TextWordWrap,
            item.text,
        )

        final_height = max(item.height, text_rect.height() - 1)
        return QtCore.QSize(target_width, int(final_height * 1.2))

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        """Renders each item"""
        painter.save()
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)

        item = index.data(QtCore.Qt.ItemDataRole.UserRole)
        rect = option.rect.adjusted(2, 2, -2, -2)

        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(rect), 12, 12)

        if item.not_clickable:
            painter.restore()
            return
        if item.allow_expand and item.needs_expansion:
            item.right_icon = self._expand_arrow(item.is_expanded)

        # Background Color
        pressed_color = QtGui.QColor("#1A8FBF")
        pressed_color.setAlpha(90 if item.selected else 20)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(pressed_color)
        painter.fillPath(path, pressed_color)

        # Geometry Calc

        # ICON SPACEEE
        ellipse_size = item.height * 0.8
        ellipse_margin = (item.height - ellipse_size) / 2
        ellipse_rect = QtCore.QRectF(
            rect.right() - ellipse_margin - ellipse_size,
            rect.top() + ellipse_margin,
            ellipse_size,
            ellipse_size,
        )

        if item.right_icon:
            icon_scaled = self._get_scaled(
                item.right_icon, ellipse_rect.size().toSize()
            )
            painter.drawPixmap(ellipse_rect.toRect(), icon_scaled)

        left_margin = 10
        left_icon_rect = QtCore.QRectF(
            rect.left() + ellipse_margin,
            rect.top() + ellipse_margin,
            ellipse_size,
            ellipse_size,
        )

        if item.left_icon:
            icon_size = QtCore.QSize(
                int(left_icon_rect.width()), int(left_icon_rect.height())
            )
            if item.color_left_icon:
                left_pixmap = self._get_tinted(item.left_icon, icon_size, item.color)
            else:
                left_pixmap = self._get_scaled(item.left_icon, icon_size)
            painter.drawPixmap(left_icon_rect.toRect(), left_pixmap)

        text_margin = int(
            rect.right() - ellipse_size - ellipse_margin - rect.height() * 0.10
        )

        text_rect = QtCore.QRectF(
            rect.left()
            + left_margin
            + (left_icon_rect.width() if item.left_icon else 0),
            rect.top(),
            text_margin
            - rect.left()
            - left_margin
            - (left_icon_rect.width() if item.left_icon else 0),
            rect.height(),
        )

        painter.setPen(QtGui.QColor(255, 255, 255))

        _font = painter.font()
        if item._lfontsize > 0:
            _font.setPointSize(item._lfontsize)
        painter.setFont(_font)

        metrics = QtGui.QFontMetrics(_font)

        right_font = QtGui.QFont(_font)
        if item._rfontsize > 0:
            right_font.setPointSize(item._rfontsize)

        right_metrics = QtGui.QFontMetrics(right_font)

        right_text_x = (
            ellipse_rect.right()
            - right_metrics.horizontalAdvance(item.right_text)
            - left_icon_rect.width()
            - left_margin
        )

        text = item.text.replace("\n", "")
        # Logic: If not expanded, OR if expansion is not needed, draw single line
        if not item.is_expanded:
            max_main_text_width = right_text_x - left_margin
            text = metrics.elidedText(
                text,
                QtCore.Qt.TextElideMode.ElideRight,
                int(max_main_text_width),
            )
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignVCenter,
                text,
            )
        else:
            # Expanded mode
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter
                | QtCore.Qt.TextFlag.TextWordWrap,
                text,
            )

        if item.right_text:
            painter.setFont(right_font)
            painter.setPen(QtGui.QColor(160, 160, 160))
            painter.drawText(
                int(right_text_x),
                int(
                    ellipse_rect.top()
                    + (ellipse_rect.height() + right_metrics.ascent()) / 2
                ),
                item.right_text,
            )

        if item.notificate:
            dot_diameter = rect.height() * 0.3
            dot_x = rect.width() - dot_diameter - 5
            notification_color = QtGui.QColor(226, 31, 31)
            painter.setBrush(notification_color)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            dot_rect = QtCore.QRectF(dot_x, rect.top(), dot_diameter, dot_diameter)
            painter.drawEllipse(dot_rect)

        painter.restore()

    def editorEvent(  # pylint: disable=invalid-name
        self,
        event: QtCore.QEvent,
        model: EntryListModel,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        """Capture view model events"""
        item = index.data(QtCore.Qt.ItemDataRole.UserRole)
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if item and item.not_clickable:
                return True
            # Record the press origin so a scroll drag is not mistaken for a tap.
            self._press_pos = event.position()
            return False

        if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            if item and item.not_clickable:
                return True

            # Ignore releases that drifted far enough to be a scroll gesture.
            press_pos = self._press_pos
            self._press_pos = None
            if press_pos is not None:
                # Fingers drift more than a mouse, so double the platform drag slop.
                threshold = QtWidgets.QApplication.startDragDistance() * 2
                delta = event.position() - press_pos
                if abs(delta.x()) + abs(delta.y()) > threshold:
                    return False

            if item.callback and callable(item.callback):
                item.callback()

            if self.prev_index is None:
                return False

            ellipse_size = item.height * 0.8
            ellipse_margin = (item.height - ellipse_size) / 2
            ellipse_rect = QtCore.QRectF(
                option.rect.right() - ellipse_margin - ellipse_size,
                option.rect.top() + ellipse_margin,
                ellipse_size,
                ellipse_size,
            )
            pos = event.position()

            # --- Logic Check ---
            # Only allow toggle if allow_expand AND text actually needs expansion
            if (
                ellipse_rect.contains(pos)
                and item.allow_expand
                and item.needs_expansion
            ):
                new_state = not item.is_expanded
                model.setData(index, new_state, EntryListModel.ExpandRole)
                return True

            if self.prev_index != index.row():
                prev_index: QtCore.QModelIndex = model.index(self.prev_index)
                if prev_index.isValid():
                    model.setData(prev_index, False, EntryListModel.EnableRole)
                self.prev_index = index.row()

            model.setData(index, True, EntryListModel.EnableRole)
            self.item_selected.emit(item)
            return True
        return False
