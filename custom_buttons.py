"""
Модуль, создающий виджет кнопок,
нужных для регистрационного окна выбора аватара (см. register_window.py)
"""


import sys
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractButton, QApplication, QWidget, QHBoxLayout
from PyQt5.QtCore import QSize


class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(200, 200)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QHBoxLayout(window)
    sys.exit(app.exec_())


