import sys
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QPainter, QPainterPath, QColor
from PyQt6.QtWidgets import QApplication, QWidget

class SubtractedRectanglesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 QPainterPath Subtraction")
        self.setGeometry(100, 100, 600, 400) # x, y, width, height

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Define the big rectangle
        big_rect = QRectF(50, 50, 500, 300) # x, y, width, height
        big_rect_path = QPainterPath()
        big_rect_path.addRect(big_rect)

        # 2. Define the small rectangle inside the big one
        small_rect = QRectF(150, 100, 300, 200) # x, y, width, height
        small_rect_path = QPainterPath()
        small_rect_path.addRect(small_rect)

        # 3. Calculate the subtracted path (the space between them)
        space_path = big_rect_path.subtracted(small_rect_path)

        # --- Drawing for demonstration ---

        # Draw the big rectangle (optional, for visualization)
        painter.setPen(QColor(0, 0, 255, 100)) # Blue, semi-transparent
        painter.setBrush(QColor(0, 0, 255, 50))
        
        
        painter.drawPath(big_rect_path)
        # painter.drawText(big_rect.topRight().x() + 5, big_rect.topRight().y() + 15, "Big Rect")

        # Draw the small rectangle (optional, for visualization)
        painter.setPen(QColor(255, 0, 0, 100)) # Red, semi-transparent
        painter.setBrush(QColor(255, 0, 0, 50))
        painter.drawPath(small_rect_path)
        # painter.drawText(small_rect.bottomRight().x() + 5, small_rect.bottomRight().y() + 15, "Small Rect")

        # Draw the resulting 'space_path'
        painter.setPen(QColor(0, 150, 0)) # Green
        painter.setBrush(QColor(0, 200, 0, 150)) # Green, semi-transparent
        painter.drawPath(space_path)
        painter.drawText(20, 20, "Space Path (Green)")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubtractedRectanglesWindow()
    window.show()
    sys.exit(app.exec())