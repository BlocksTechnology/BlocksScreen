import typing
from dataclasses import dataclass, field

from PyQt6 import QtCore, QtGui, QtWidgets  # pylint: disable=import-error


@dataclass(slots=True)
class ListItem:
    """List item data"""

    text: str
    right_text: str = ""
    _rfontsize: int = 0
    _lfontsize: int = 0

    callback: typing.Callable | None = None

    color: str = "#dfdfdf"
    color_left_icon: bool = False
    right_icon: QtGui.QPixmap | None = None
    left_icon: QtGui.QPixmap | None = None

    selected: bool = False
    allow_check: bool = True

    not_clickable: bool = False

    allow_expand: bool = False
    needs_expansion: bool = False
    is_expanded: bool = False

    height: int = 60
    notificate: bool = False

    _cache: dict[int, int] = field(default_factory=dict)

    def clear_cache(self):
        """Call this if text or font size changes dynamically"""
        self._cache.clear()


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

    def deleteLater(self) -> None:
        """subclass for deleting the object"""
        return super().deleteLater()

    def remove_item(self, item: ListItem) -> None:
        """Removes one row item from the model"""
        if item in self.entries:
            index = self.entries.index(item)
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.entries.pop(index)
            self.endRemoveRows()

    def delete_duplicates(self) -> None:
        """
        Removes items that have identical text, color, and
        last time entry (get(-1)).
        """
        seen_identifiers: set[tuple[str, str, str]] = set()
        unique_entries: list[ListItem] = []

        for item in self.entries:
            text_val = item.text
            color_val = item.color
            time_val = item._cache.get(-1)

            identifier = (text_val, color_val, time_val)

            if identifier not in seen_identifiers:
                unique_entries.append(item)
                seen_identifiers.add(identifier)

        self.beginResetModel()
        self.entries = unique_entries
        self.endResetModel()

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

    def remove_item_by_text(self, text: str) -> bool:
        """Remove item from model by its text value.

        Args:
            text: The text value of the item to remove.

        Returns:
            True if item was found and removed, False otherwise.
        """
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
        """Remove item at a specific position.

        Returns:
            True if item was removed, False if position is out of range.
        """
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
        """Update an existing item's display data in-place.

        Copies visual fields (left_icon, right_text, right_icon) from
        *item* into the entry at *position* and emits ``dataChanged``.

        Returns:
            True if updated, False if position is out of range.
        """
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
        """Diff current entries against *desired* and apply minimal mutations.

        Uses *key_fn* to derive a unique identity string for each item.
        """
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
        self.height: int = 60
        self._scaled_cache: dict[tuple[int, int, int], QtGui.QPixmap] = {}
        self._tinted_cache: dict[tuple[int, str], QtGui.QPixmap] = {}
        self._font_cache: dict[int, tuple[QtGui.QFont, QtGui.QFontMetrics]] = {}
        # Base the font cache was built from, a restyle must invalidate it
        self._font_base: QtGui.QFont | None = None
        self._path_cache: dict[tuple[int, int], QtGui.QPainterPath] = {}
        self._geometry_cache: dict[
            tuple[int, int], tuple[float, float, QtCore.QRectF, QtCore.QRectF]
        ] = {}
        # Pre-computed colors - avoids QColor allocation + setAlpha per paint frame
        self._color_pressed_sel = QtGui.QColor("#1A8FBF")
        self._color_pressed_sel.setAlpha(90)
        self._color_pressed_unsel = QtGui.QColor("#1A8FBF")
        self._color_pressed_unsel.setAlpha(20)
        self._color_text = QtGui.QColor(255, 255, 255)
        self._color_secondary = QtGui.QColor(160, 160, 160)
        self._color_notification = QtGui.QColor(226, 31, 31)
        # Arrow icons loaded once - avoids QPixmap(resource) parse per paint frame
        self._arrow_down = QtGui.QPixmap(":/arrow_icons/media/btn_icons/arrow_down.svg")
        self._arrow_right = QtGui.QPixmap(
            ":/arrow_icons/media/btn_icons/arrow_right.svg"
        )

    def _get_scaled(
        self,
        pixmap: QtGui.QPixmap,
        size: QtCore.QSize,
    ) -> QtGui.QPixmap:
        """Return *pixmap* scaled to *size*, using a cache to avoid
        re-scaling the same icon every paint frame.

        The cache key is (QPixmap.cacheKey(), width, height) which
        correctly invalidates when the source pixmap changes.
        """
        key = (pixmap.cacheKey(), size.width(), size.height())
        cached = self._scaled_cache.get(key)
        if cached is not None:
            return cached
        scaled = pixmap.scaled(
            size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self._scaled_cache[key] = scaled
        # Prevent unbounded growth - 64 entries covers all wifi
        # bar variants × protected/open × left/right icons easily.
        if len(self._scaled_cache) > 64:
            keys = list(self._scaled_cache)
            for k in keys[:32]:
                del self._scaled_cache[k]
        return scaled

    def _get_font_metrics(
        self, base_font: QtGui.QFont, point_size: int
    ) -> tuple[QtGui.QFont, QtGui.QFontMetrics]:
        """Return *base_font* at *point_size* with its metrics, cached per size.

        ``paint`` passes the painter font and ``sizeHint`` the option font, so the
        cache is keyed on size alone but dropped whenever the base font changes.
        """
        if self._font_base != base_font:
            self._font_cache.clear()
            self._font_base = QtGui.QFont(base_font)
        cached = self._font_cache.get(point_size)
        if cached is None:
            if point_size != base_font.pointSize():
                f = QtGui.QFont(base_font)
                f.setPointSize(point_size)
            else:
                f = base_font
            cached = (f, QtGui.QFontMetrics(f))
            self._font_cache[point_size] = cached
        return cached

    def _get_tinted(self, pixmap: QtGui.QPixmap, color: str) -> QtGui.QPixmap:
        key = (pixmap.cacheKey(), color)
        cached = self._tinted_cache.get(key)
        if cached is None:
            tinted = QtGui.QPixmap(pixmap.size())
            tinted.fill(QtCore.Qt.GlobalColor.transparent)
            p = QtGui.QPainter(tinted)
            p.drawPixmap(0, 0, pixmap)
            p.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_SourceIn
            )
            p.fillRect(tinted.rect(), QtGui.QColor(color))
            p.end()
            cached = tinted
            self._tinted_cache[key] = cached
            if len(self._tinted_cache) > 32:
                keys = list(self._tinted_cache)
                for k in keys[:16]:
                    del self._tinted_cache[k]
        return cached

    def clear(self) -> None:
        """Clears delegate indexing"""
        self.prev_index = 0

    def sizeHint(
        self, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex
    ):
        """
        Calculates size AND determines if expansion is needed.
        """
        item: ListItem = index.data(QtCore.Qt.ItemDataRole.UserRole)
        target_width = option.rect.width()

        base_h = item.height
        ellipse_size = base_h * 0.8

        right_reserved = base_h

        left_reserved = 10
        if item.left_icon:
            left_reserved = (base_h * 0.1) + ellipse_size + 8

        if item._lfontsize > 0 and item._lfontsize != option.font.pointSize():
            fm = self._get_font_metrics(option.font, item._lfontsize)[1]
        else:
            fm = option.fontMetrics

        if item.right_text:
            if item._rfontsize > 0 and item._rfontsize != option.font.pointSize():
                fmr = self._get_font_metrics(option.font, item._rfontsize)[1]
            else:
                fmr = option.fontMetrics
            right_reserved += fmr.horizontalAdvance(item.right_text) + 10

        if item.right_icon:
            right_reserved += ellipse_size

        text_avail_width = target_width - left_reserved - right_reserved
        text_avail_width = max(text_avail_width, 50)

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
        if item.not_clickable:
            painter.restore()
            return

        rect = option.rect.adjusted(2, 2, -2, -2)
        w, h = rect.width(), rect.height()
        # Translate so all geometry is relative to (0,0) - enables path cache hits
        # across items (all rows share the same w/h in a fixed-width list view).
        painter.translate(rect.x(), rect.y())

        path_key = (w, h)
        path = self._path_cache.get(path_key)
        if path is None:
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(0, 0, w, h), 12, 12)
            self._path_cache[path_key] = path
            # Expanded rows produce a new height each time, keep the dict bounded
            if len(self._path_cache) > 32:
                for k in list(self._path_cache)[:16]:
                    del self._path_cache[k]

        if item.allow_expand and item.needs_expansion:
            item.right_icon = (
                self._arrow_down if item.is_expanded else self._arrow_right
            )

        # fillPath takes its brush as an argument, the painter pen/brush are unused here
        painter.fillPath(
            path,
            self._color_pressed_sel if item.selected else self._color_pressed_unsel,
        )

        geom_key = (w, item.height)
        geometry = self._geometry_cache.get(geom_key)
        if geometry is None:
            ellipse_size = item.height * 0.8
            ellipse_margin = (item.height - ellipse_size) / 2
            geometry = (
                ellipse_size,
                ellipse_margin,
                QtCore.QRectF(
                    w - ellipse_margin - ellipse_size,
                    ellipse_margin,
                    ellipse_size,
                    ellipse_size,
                ),
                QtCore.QRectF(
                    ellipse_margin, ellipse_margin, ellipse_size, ellipse_size
                ),
            )
            self._geometry_cache[geom_key] = geometry
        ellipse_size, ellipse_margin, ellipse_rect, left_icon_rect = geometry

        if item.right_icon:
            icon_scaled = self._get_scaled(
                item.right_icon, ellipse_rect.size().toSize()
            )
            painter.drawPixmap(ellipse_rect.toRect(), icon_scaled)

        left_margin = 10

        if item.left_icon:
            l_icon_scaled = self._get_scaled(
                item.left_icon,
                QtCore.QSize(int(left_icon_rect.width()), int(left_icon_rect.height())),
            )
            if item.color_left_icon:
                painter.drawPixmap(
                    left_icon_rect.toRect(),
                    self._get_tinted(l_icon_scaled, item.color),
                )
            else:
                painter.drawPixmap(left_icon_rect.toRect(), l_icon_scaled)

        text_margin = int(w - ellipse_size - ellipse_margin - h * 0.10)

        icon_w = left_icon_rect.width() if item.left_icon else 0
        text_rect = QtCore.QRectF(
            left_margin + icon_w,
            0,
            text_margin - left_margin - icon_w,
            h,
        )

        painter.setPen(self._color_text)

        _font = painter.font()
        lps = item._lfontsize if item._lfontsize > 0 else _font.pointSize()
        rps = item._rfontsize if item._rfontsize > 0 else _font.pointSize()
        font, metrics = self._get_font_metrics(_font, lps)
        right_font, right_metrics = self._get_font_metrics(_font, rps)
        painter.setFont(font)

        right_text_x = (
            ellipse_rect.right()
            - right_metrics.horizontalAdvance(item.right_text)
            - left_icon_rect.width()
            - left_margin
        )

        text = item.text.replace("\n", "")
        if not item.is_expanded:
            max_main_text_width = right_text_x - left_margin
            text = metrics.elidedText(
                text,
                QtCore.Qt.TextElideMode.ElideRight,
                int(max_main_text_width),
            )
            painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignVCenter, text)
        else:
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter
                | QtCore.Qt.TextFlag.TextWordWrap,
                text,
            )

        if item.right_text:
            painter.setFont(right_font)
            painter.setPen(self._color_secondary)
            painter.drawText(
                int(right_text_x),
                int(
                    ellipse_rect.top()
                    + (ellipse_rect.height() + right_metrics.ascent()) / 2
                ),
                item.right_text,
            )

        if item.notificate:
            dot_diameter = h * 0.3
            dot_x = w - dot_diameter - 5
            painter.setBrush(self._color_notification)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawEllipse(QtCore.QRectF(dot_x, 0, dot_diameter, dot_diameter))

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
