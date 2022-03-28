"""
Модуль, отвечающий за поле для ввода письменных команд помощнику
поля для помощников оформляются по разному, в плане визуала
"""

import sys
import configparser
from PyQt5.QtWidgets import QWidget, QCompleter, QApplication, QFrame, QStackedLayout, QGridLayout, \
    QLineEdit, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import QMetaObject, Qt


class EnterField(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 110
        self.config = configparser.ConfigParser()
        self.config.read("Data/Config.ini")
        self.size_win = int(self.config["Settings"]["window_scale"])
        self.scale = int(int(self.config["Settings"]["window_scale"]) / 100 * 18)
        self.character = self.config["User"]["character"]
        if self.character == "Eve":
            self.bg_color = "rgba(222, 246, 255, 100)"
            self.border_color = "rgba(0, 138, 230, 255)"
            self.font_color = "rgba(0, 138, 230, 255)"
        elif self.character == "Walle":
            self.bg_color = "rgba(196, 135, 79, 100)"
            self.border_color = "rgba(27, 27, 27, 255)"
            self.font_color = "rgba(27, 27, 27, 255)"
        self.setupUi()

    def setupUi(self):
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(1)
        mlay = QStackedLayout(self.frame)
        mlay.setStackingMode(1)

        self.bgFrame = QFrame(self.frame)
        self.UIFrame = QFrame(self.frame)
        add_lay = QGridLayout(self.bgFrame)

        width = round(445 * self.size_win / 100)
        height = round(100 * self.size_win / 100)
        self.back = QFrame(self.bgFrame)
        self.back.setStyleSheet(
            '''
            background-color: %s;
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            border-color: %s;
            min-width: 10em;
            min-height: 5em;
            font: %s;
            ''' % (self.bg_color,
                   self.border_color,
                   str(self.scale) + 'px'))
        self.back.setObjectName("background")

        add_lay.addWidget(self.back)

        lay = QVBoxLayout(self.UIFrame)
        self.config = configparser.ConfigParser()
        self.config.read("Data/Config.ini")

        self.hframe = QFrame()
        hlay = QHBoxLayout(self.hframe)
        self.label = QLabel(self.hframe)
        self.label.setText("Вы ввели:")
        self.label.setObjectName("UserName")
        self.label.setStyleSheet(
            '''
            font:  %s;
            color: %s;
            padding: 6px;
            ''' % (str(self.scale) + 'px',
                   self.font_color))

        self.say = QLabel(self.hframe)
        self.say.setText("")
        self.say.setObjectName("UserSaid")
        self.say.setStyleSheet(
            '''
            font:  %s;
            color: %s;
            padding: 6px;
            ''' % (str(self.scale) + 'px',
                   self.font_color))

        hlay.addWidget(self.label)
        hlay.addWidget(self.say)

        self.edit_line = QLineEdit(self.UIFrame)
        self.edit_line.setStyleSheet(
            '''
            background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            border-color: %s;
            font:  %s;
            color: %s;
            min-width: 10em;
            padding: 6px;
            ''' % (self.border_color,
                   str(self.scale) + 'px',
                   self.font_color))

        self.edit_line.setObjectName("TextLine")
        self.edit_line.setPlaceholderText("Введите команду...")

        key = ["открой браузер", "открой сайт", "изменить браузер", "открой папку", "открой файл",
               "погода", "время", "система", "что ты умеешь?", "местоположение", "новости", "пока"]
        self.completer = QCompleter(key, self.edit_line)
        self.completer.setCaseSensitivity(0)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.popup().setStyleSheet(
            '''
            background-color: white;
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            border-color: blue;
            font:  16px;
            color: blue;
            font-style: italic;
            ''')
        self.edit_line.text()
        self.edit_line.setCompleter(self.completer)

        lay.addWidget(self.hframe)
        lay.addWidget(self.edit_line)
        mlay.addWidget(self.bgFrame)
        mlay.addWidget(self.UIFrame)
        self.setLayout(mlay)

        QMetaObject.connectSlotsByName(self.frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = EnterField()
    w.show()
    app.exec_()
