"""
Модуль содержащий класс для функции погоды, то есть визуалки на разную погоду.
"""

import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QStackedLayout, QApplication
from PyQt5.QtCore import pyqtSlot, Qt, QMetaObject
import configparser


class WeatherForm(QWidget):

    def __init__(self, setup_size_win):
        super().__init__()
        self.setup_size_win = setup_size_win
        self.setup_size_win.size_weather.connect(self.size_change)
        self.config = configparser.ConfigParser()
        self.config.read("Data/Config.ini")
        self.size_win = int(self.config["Settings"]["window_scale"])
        self.setupUi()

    @pyqtSlot(int)
    def size_change(self, size):
        pixmap = QPixmap("Image/Other/Sun.png")
        mini_pix = pixmap.scaled(150 * size / 100,
                                 150 * size / 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.sun.setPixmap(mini_pix)

        pixmap = QPixmap("Image/Other/Rain.png")
        mini_pix = pixmap.scaled(150 * size / 100,
                                 150 * size / 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.rain.setPixmap(mini_pix)

    def setupUi(self):
        self.frame = QFrame()
        self.mlay = QStackedLayout(self.frame)

        self.empty = QLabel(self.frame)
        # self.empty.setPixmap(mini_pix)
        self.empty.setObjectName("Empty")

        pixmap = QPixmap("Image/Other/Sun.png")
        mini_pix = pixmap.scaled(150 * self.size_win / 100,
                                 150 * self.size_win / 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.sun = QLabel(self.frame)
        self.sun.setPixmap(mini_pix)
        self.sun.setObjectName("Sun")

        pixmap = QPixmap("Image/Other/Rain.png")
        mini_pix = pixmap.scaled(150 * self.size_win / 100,
                                 150 * self.size_win / 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.rain = QLabel(self.frame)
        self.rain.setPixmap(mini_pix)
        self.rain.setObjectName("Rain")

        pixmap = QPixmap("Image/Other/Cloud.png")
        mini_pix = pixmap.scaled(150 * self.size_win / 100,
                                 150 * self.size_win / 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.cloud = QLabel(self.frame)
        self.cloud.setPixmap(mini_pix)
        self.cloud.setObjectName("Cloud")

        pixmap = QPixmap("Image/Other/Sun_cloud.png")
        mini_pix = pixmap.scaled(150 * self.size_win / 100,
                                 150 * self.size_win / 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.sun_cloud = QLabel(self.frame)
        self.sun_cloud.setPixmap(mini_pix)
        self.sun_cloud.setObjectName("Sun_Cloud")

        self.mlay.addWidget(self.empty)
        self.mlay.addWidget(self.sun)
        self.mlay.addWidget(self.rain)
        self.mlay.addWidget(self.cloud)
        self.mlay.addWidget(self.sun_cloud)
        self.setLayout(self.mlay)

        QMetaObject.connectSlotsByName(self.frame)

    def change_icon(self, weather):
        if weather == "ясно":
            self.mlay.setCurrentIndex(1)
        if weather == "пасмурно" or weather == "гроза с небольшим дождём":
            self.mlay.setCurrentIndex(2)

        if weather == "облачно с прояснениями":
            self.mlay.setCurrentIndex(4)

        if weather == "переменная облачность":
            self.mlay.setCurrentIndex(3)

        if weather == "небольшая облачность":
            self.mlay.setCurrentIndex(3)

        if weather == "небольшой дождь":
            self.mlay.setCurrentIndex(2)

        if weather == "небольшой проливной дождь":
            self.mlay.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WeatherForm()
    w.show()
    app.exec_()
