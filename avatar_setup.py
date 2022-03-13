import sys
import configparser
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QStackedWidget, QPushButton, QHBoxLayout, QApplication, QFrame
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QPixmap


class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.character = ""
        lay = QVBoxLayout(self)
        self.buttonframe = QFrame(self)
        self.picframe = QFrame(self)
        self.card1 = QFrame(self)
        self.card2 = QFrame(self)
        buttonlay = QHBoxLayout(self.buttonframe)

        piclay1 = QVBoxLayout(self.card1)
        piclay2 = QVBoxLayout(self.card2)

        btn1 = QPushButton("Ева")
        btn1.setFont(QFont("Times", 12))
        btn1.clicked.connect(self.change_character1)
        btn2 = QPushButton("Валли")
        btn2.setFont(QFont("Times", 12))
        btn2.clicked.connect(self.change_character2)
        piclay1.addWidget(btn1)
        piclay2.addWidget(btn2)
        piclay1.addSpacing(5)
        piclay2.addSpacing(5)

        self.pixmap = QPixmap("Image/Characters/Walle_set/Icon.png")
        self.mini_pix = self.pixmap.scaled(200, 200, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
        lbl1 = QLabel()
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setPixmap(self.mini_pix)
        piclay1.addWidget(lbl1)
        self.pixmap = QPixmap("Image/Characters/Eve_set/Icon.png")
        self.mini_pix = self.pixmap.scaled(200, 200, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
        lbl2 = QLabel()
        lbl2.setAlignment(QtCore.Qt.AlignCenter)
        lbl2.setPixmap(self.mini_pix)
        piclay2.addWidget(lbl2)
        buttonlay.addWidget(self.card1)
        buttonlay.addWidget(self.card2)
        lay.addWidget(self.buttonframe)
        self.err_lbl = QLabel("")
        lay.addWidget(self.err_lbl)

    def change_character1(self):
        self.character = "Walle"

    def change_character2(self):
        self.character = "Eve"


class Character_setup(QWidget):
    def __init__(self, config, parent=None):
        QWidget.__init__(self, parent=parent)
        self.config = config
        self.W = Widget()
        lay = QVBoxLayout(self)
        self.bframe = QFrame(self)
        blay = QHBoxLayout(self.bframe)
        btn1 = QPushButton("Save")
        btn1.setFont(QFont("Times", 14))
        btn1.clicked.connect(self.onNext)
        btn2 = QPushButton("Cancel")
        btn2.setFont(QFont("Times", 14))
        btn2.clicked.connect(self.Cancel)
        blay.addWidget(btn1)
        blay.addWidget(btn2)
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.W)
        lay.addWidget(self.Stack)
        lay.addWidget(self.bframe)
        self.setLayout(lay)

    def onNext(self):
        self.config["User"]["character"] = self.W.character
        with open("Data/Config.ini", 'w') as configfile:
            self.config.write(configfile)
        self.close()

    def Cancel(self):
        self.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("Data/Config.ini")
    with open("Data/Config.ini", 'w') as configfile:
        config.write(configfile)
    app = QApplication(sys.argv)
    w = Character_setup(config)
    w.show()
    app.exec_()

