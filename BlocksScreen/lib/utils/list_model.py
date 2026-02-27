import typing
from dataclasses import dataclass

from PyQt6 import QtCore, QtGui, QtWidgets  # pylint: disable=import-error


@dataclass(slots=True)
class ListItem:
    """List item data"""

    text: str
    right_text: str = ""
    right_icon: typing.Optional[QtGui.QPixmap] = None
    left_icon: typing.Optional[QtGui.QPixmap] = None
    callback: typing.Optional[typing.Callable] = None
    selected: bool = False
    allow_check: bool = True
    _lfontsize: int = 0
    _rfontsize: int = 0
    height: int = 60  # Change has needed
    notificate: bool = False  # render red dot
    not_clickable: bool = False


class EntryListModel(QtCore.QAbstractListModel):
    """List model Subclassed QAbstractListModel"""

    EnableRole = QtCore.Qt.ItemDataRole.UserRole + 1
    NotificateRole = QtCore.Qt.ItemDataRole.UserRole + 2

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
        # Prevent unbounded growth — 64 entries covers all wifi
        # bar variants × protected/open × left/right icons easily.
        if len(self._scaled_cache) > 64:
            # Drop oldest half
            keys = list(self._scaled_cache)
            for k in keys[:32]:
                del self._scaled_cache[k]
        return scaled

    def clear(self) -> None:
        """Clears delegate indexing"""
        self.prev_index = 0

    def sizeHint(
        self, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex
    ):
        """Returns base size for items, re-implemented method"""
        base = super().sizeHint(option, index)
        base.setHeight(self.height)
        return QtCore.QSize(base.width(), int(self.height + self.height * 0.20))

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget | None,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        """re-implemented method"""
        return super().updateEditorGeometry(editor, option, index)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        """Renders each item, re-implemented method"""
        super().paint(painter, option, index)
        item = index.data(QtCore.Qt.ItemDataRole.UserRole)
        painter.save()
        rect = option.rect
        rect.setHeight(item.height)
        button = QtWidgets.QStyleOptionButton()
        button.rect = rect
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
        radius = rect.height() / 5.0

        # Main rounded rectangle path (using the adjusted rect)
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(rect), radius, radius)

        if item.not_clickable:
            painter.restore()
            return

        pressed_color = QtGui.QColor("#1A8FBF")
        pressed_color.setAlpha(90 if item.selected else 20)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(pressed_color)
        painter.fillPath(path, pressed_color)

        # Ellipse ("hole") for the icon on the right
        ellipse_margin = rect.height() * 0.05
        ellipse_size = rect.height() * 0.90
        ellipse_rect = QtCore.QRectF(
            rect.right() - ellipse_margin - ellipse_size,
            rect.top() + ellipse_margin,
            ellipse_size,
            ellipse_size,
        )
        icon_margin = ellipse_size * 0.10
        # Draw icon inside the ellipse "hole" (on the right)
        if item.right_icon:
            icon_rect = QtCore.QRectF(
                ellipse_rect.left() + icon_margin / 2,
                ellipse_rect.top() + icon_margin / 2,
                ellipse_rect.width() - icon_margin,
                ellipse_rect.height() - icon_margin,
            )
            icon_scaled = self._get_scaled(item.right_icon, icon_rect.size().toSize())
            # Center the icon in the ellipse
            adjusted_x = (
                icon_rect.x() + (icon_rect.width() - icon_scaled.width()) // 2.0
            )
            adjusted_y = rect.y() + (rect.height() - icon_scaled.height()) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                adjusted_x,
                adjusted_y,
                icon_scaled.width(),
                icon_scaled.height(),
            )
            painter.drawPixmap(
                adjusted_icon_rect, icon_scaled, icon_scaled.rect().toRectF()
            )

        # Ellipse ("hole") for the icon on the left (only if present)
        left_icon_margin = rect.height() * 0.05
        left_icon_size = rect.height() * 0.70
        left_icon_rect = QtCore.QRectF(
            rect.left() + left_icon_margin,
            rect.top() + left_icon_margin,
            left_icon_size,
            left_icon_size,
        )
        left_margin = 10  # default left margin
        # Draw second icon (on the left, if present)
        if item.left_icon:
            left_icon_scaled = self._get_scaled(
                item.left_icon, left_icon_rect.size().toSize()
            )
            # Center the icon in the rect
            adjusted_x = (
                left_icon_rect.x()
                + (left_icon_rect.width() - left_icon_scaled.width()) // 2.0
            )
            adjusted_y = rect.y() + (rect.height() - left_icon_scaled.height()) // 2.0
            adjusted_left_icon_rect = QtCore.QRectF(
                adjusted_x,
                adjusted_y,
                left_icon_scaled.width(),
                left_icon_scaled.height(),
            )
            painter.drawPixmap(
                adjusted_left_icon_rect,
                left_icon_scaled,
                left_icon_scaled.rect().toRectF(),
            )
            left_margin = left_icon_margin + left_icon_size + 8  # 8px gap after icon

        # Draw text, area before the ellipse (adjusted for left icon)
        text_margin = int(
            rect.right() - ellipse_size - ellipse_margin - rect.height() * 0.10
        )
        text_rect = QtCore.QRectF(
            rect.left() + left_margin,
            rect.top(),
            text_margin - rect.left() - left_margin,
            rect.height(),
        )

        # Draw main text (left-aligned)
        painter.setPen(QtGui.QColor(255, 255, 255))
        _font = painter.font()
        _font.setPointSize(item._lfontsize)
        painter.setFont(_font)
        metrics = QtGui.QFontMetrics(_font)
        main_text_height = metrics.height()

        # Vertically center text
        text_y = rect.top() + (rect.height() + main_text_height) / 2 - metrics.descent()

        # Calculate where to start the right text: just left of the right icon ellipse
        gap = 10  # gap between right text and icon ellipse
        right_font = QtGui.QFont(_font)
        right_font.setPointSize(item._rfontsize)
        right_metrics = QtGui.QFontMetrics(right_font)
        right_text_width = right_metrics.horizontalAdvance(item.right_text)

        # The right text should end at ellipse_rect.left() - gap
        right_text_x = ellipse_rect.left() - gap - right_text_width

        # Draw main text (left-aligned, but don't overlap right text)
        max_main_text_width = (
            right_text_x - text_rect.left() - 10
        )  # 10px gap between main and right text
        elided_main_text = metrics.elidedText(
            item.text,
            QtCore.Qt.TextElideMode.ElideRight,
            int(max_main_text_width),
        )

        painter.setFont(_font)
        painter.drawText(
            int(text_rect.left()),
            int(text_y),
            elided_main_text,
        )

        # Draw right text (smaller, grey, just left of the icon)
        if item.right_text:
            painter.setFont(right_font)
            painter.setPen(QtGui.QColor(160, 160, 160))  # grey color
            right_text_height = right_metrics.height()
            right_text_y = (
                rect.top()
                + (rect.height() + right_text_height) / 2
                - right_metrics.descent()
            )
            painter.drawText(
                int(right_text_x),
                int(right_text_y),
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
        """Capture view model events, re-implemented method"""
        item = index.data(QtCore.Qt.ItemDataRole.UserRole)
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if item and item.not_clickable:
                return True
            if item.callback:
                if callable(item.callback):
                    item.callback()
            if self.prev_index is None:
                return False
            if self.prev_index != index.row():
                prev_index: QtCore.QModelIndex = model.index(self.prev_index)
                model.setData(prev_index, False, EntryListModel.EnableRole)
                self.prev_index = index.row()
            model.setData(index, True, EntryListModel.EnableRole)
            self.item_selected.emit(item)
            return True
        return False
