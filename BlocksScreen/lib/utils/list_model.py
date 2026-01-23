import typing
from dataclasses import dataclass, field

from PyQt6 import QtCore, QtGui, QtWidgets  # pylint: disable=import-error


@dataclass
class ListItem:
    """List item data"""

    text: str
    right_text: str = ""
    _rfontsize: int = 0
    _lfontsize: int = 0

    callback: typing.Optional[typing.Callable] = None

    color: str = "#dfdfdf"
    right_icon: typing.Optional[QtGui.QPixmap] = None
    left_icon: typing.Optional[QtGui.QPixmap] = None

    selected: bool = False
    allow_check: bool = True

    allow_expand: bool = False
    needs_expansion: bool = False
    is_expanded: bool = False

    height: int = 60
    notificate: bool = False

    # stores width and heitgh of the button so we dont need to recalculate it every time
    _cache: typing.Dict[int, int] = field(default_factory=dict)

    def clear_cache(self):
        """Call this if text or font size changes dynamically"""
        self._cache.clear()


class EntryListModel(QtCore.QAbstractListModel):
    """List model Subclassed QAbstractListModel"""

    EnableRole = QtCore.Qt.ItemDataRole.UserRole + 1
    NotificateRole = QtCore.Qt.ItemDataRole.UserRole + 2
    ExpandRole = QtCore.Qt.ItemDataRole.UserRole + 3

    def __init__(self, entries=None) -> None:
        super().__init__()
        self.entries = entries or []

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
        self.beginInsertRows(
            QtCore.QModelIndex(),
            self.rowCount(),
            self.rowCount(),
        )
        self.entries.append(item)
        self.endInsertRows()

    def flags(self, index) -> QtCore.Qt.ItemFlag:
        """Models item flags, re-implemented method"""
        item = self.entries[index.row()]
        flags = QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
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
        super().__init__()
        self.prev_index: int = 0

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
        # Cache it
        item._cache[target_width] = final_height + 20
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
        radius = 12
        path.addRoundedRect(QtCore.QRectF(rect), radius, radius)

        show_expand_arrow = item.allow_expand and item.needs_expansion

        if show_expand_arrow:
            item.right_icon = (
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/arrow_down.svg")
                if item.is_expanded
                else QtGui.QPixmap(":/arrow_icons/media/btn_icons/arrow_right.svg")
            )

        # Background Color
        pressed_color = QtGui.QColor("#1A8FBF")
        pressed_color.setAlpha(90 if item.selected else 20)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(pressed_color)
        painter.fillPath(path, pressed_color)

        # Geometry Calc
        ellipse_size = item.height * 0.8
        ellipse_margin = (item.height - ellipse_size) / 2
        ellipse_rect = QtCore.QRectF(
            rect.right() - ellipse_margin - ellipse_size,
            rect.top() + ellipse_margin,
            ellipse_size,
            ellipse_size,
        )

        if item.right_icon:
            icon_scaled = item.right_icon.scaled(
                ellipse_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(
                ellipse_rect.toRect(),
                icon_scaled,
            )

        left_margin = 10
        if item.left_icon:
            left_icon_rect = QtCore.QRectF(
                rect.left() + ellipse_margin,
                rect.top() + ellipse_margin,
                ellipse_size,
                ellipse_size,
            )
            l_icon_scaled = item.left_icon.scaled(
                int(left_icon_rect.width()),
                int(left_icon_rect.height()),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            tinted = QtGui.QPixmap(l_icon_scaled.size())
            tinted.fill(QtCore.Qt.GlobalColor.transparent)
            p2 = QtGui.QPainter(tinted)
            p2.drawPixmap(0, 0, l_icon_scaled)
            p2.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_SourceIn
            )
            p2.fillRect(tinted.rect(), QtGui.QColor(item.color))
            p2.end()
            painter.drawPixmap(
                left_icon_rect.toRect(),
                tinted,
            )
            left_margin = ellipse_margin + ellipse_size + 8

        text_margin = int(
            rect.right() - ellipse_size - ellipse_margin - rect.height() * 0.10
        )
        text_rect = QtCore.QRectF(
            rect.left() + left_margin,
            rect.top(),
            text_margin - rect.left() - left_margin,
            rect.height(),
        )

        painter.setPen(QtGui.QColor(255, 255, 255))
        _font = painter.font()
        if item._lfontsize > 0:
            _font.setPointSize(item._lfontsize)
        painter.setFont(_font)
        metrics = QtGui.QFontMetrics(_font)
        main_text_height = metrics.height()

        text_y = rect.top() + (rect.height() + main_text_height) / 2 - metrics.descent()

        right_font = QtGui.QFont(_font)
        if item._rfontsize > 0:
            right_font.setPointSize(item._rfontsize)
        right_metrics = QtGui.QFontMetrics(right_font)
        right_text_width = right_metrics.horizontalAdvance(item.right_text)
        right_text_x = ellipse_rect.right() - right_text_width - left_margin

        # Adjust main text width based on right text
        max_main_text_width = right_text_x - left_margin

        text = item.text

        # Logic: If not expanded, OR if expansion is not needed, draw single line
        if not item.is_expanded:
            text = metrics.elidedText(
                text,
                QtCore.Qt.TextElideMode.ElideRight,
                int(max_main_text_width),
            )
            painter.drawText(
                int(text_rect.left()),
                int(text_y),
                text,
            )
        else:
            # Expanded mode
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignTop
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

    def editorEvent(
        self,
        event: QtCore.QEvent,
        model: EntryListModel,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        """Capture view model events"""
        item = index.data(QtCore.Qt.ItemDataRole.UserRole)
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
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
