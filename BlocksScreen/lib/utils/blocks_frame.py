from PyQt6 import QtCore, QtGui, QtWidgets
import typing

class BlocksCustomFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        # New properties replacing the old ones:
        self._left_line_width = 15  # Default fixed width for the left line
        self._is_centered = False   # Flag to control centering mode
        self.text = "" 

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)

    def setRadius(self, radius: int):
        self._radius = radius
        self.update()

    # Setter for the left line width
    def setLeftLineWidth(self, width: int):
        self._left_line_width = width
        self.update()

    # Setter to toggle the centering behavior
    def setCentered(self, centered: bool):
        self._is_centered = centered
        self.update()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, value)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Draw Frame Background (omitted for brevity)
        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            
            # FONT + METRICS (omitted for brevity)
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()        

            # LAYOUT CONFIGURATION
            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2
            
            # Use the new flag to determine mode
            if self._is_centered:
                # ---------------------------------------------
                # CENTERING MODE: Symmetrical layout
                # We use the fixed left line width for both lines
                # ---------------------------------------------
                
                left_line_width = self._left_line_width 
                right_line_width = self._left_line_width # Symmetric width
                
                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x) 

            else:
                # ---------------------------------------------
                # LEFT-ALIGNED MODE: Asymmetrical (Right line fills space)
                # ---------------------------------------------
                
                left_line_width = self._left_line_width # Use the defined fixed width
                x = margin
                right_line_width = 0 # Placeholder, calculated later
            
            
            # 1. DRAW LEFT LINE
            small_rect = QtCore.QRect(
                x,
                line_center_y - 1,
                left_line_width,
                3
            )
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            # 2. DRAW TEXT
            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            # 3. CALCULATE & DRAW RIGHT LINE
            
            if self._is_centered:
                # Centered mode: use the fixed, symmetric width
                big_rect_width = right_line_width 
            else:
                # Left-aligned mode: calculate remaining space
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width) 

            big_rect = QtCore.QRect(
                x,
                line_center_y - 1,
                big_rect_width,
                3
            )

            painter.fillRect(big_rect, QtGui.QColor("white"))