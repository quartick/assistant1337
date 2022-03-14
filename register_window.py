"""
Модуль, отвечающий за регистрационное окно
4 виджета, которые представляют "шаги" прохождения регистрации
Также здесь же они связываются воедино, и получается прикольное окно для регистрациии
"""


import sys
import configparser

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QStackedWidget, QPushButton, QHBoxLayout, QApplication, QFrame, \
    QGridLayout, QStackedLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon

import custom_buttons


class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QStackedLayout(self)
        lay.setStackingMode(1)
        hello_lbl = QLabel()
        hello_lbl.setText(
            """Добро пожаловать!\nСейчас мы настроим вашего помощника\nспециально для вас.\n\n\nОсталось всего несколько шагов.
            """)
        hello_lbl.setStyleSheet(
            '''
            font:  30px;
            color: #002756;
            '''
        )
        hello_lbl.setFont(QFont("Times"))
        hello_lbl.setAlignment(Qt.AlignCenter)

        lay.addWidget(hello_lbl)


class Widget2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        lbl = QLabel()
        lbl.setText("Как к вам обращаться?")
        lbl.setStyleSheet(
            '''
            font:  30px;
            color: #002756;
            '''
        )
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFont(QFont("Times"))
        lay.addWidget(lbl)
        self.lbl2 = QLabel()
        self.lbl2.setText("")
        self.lbl2.setStyleSheet(
            '''
            font:  20px;
            color: #002756;
            '''
        )
        self.lbl2.setFont(QFont("Times"))
        lay.addWidget(self.lbl2)
        self.enter = QLineEdit()
        self.enter.setFont(QFont("Times", 16))
        lay.addWidget(self.enter)


class Widget3(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.character = ""
        lay = QVBoxLayout(self)
        self.buttonframe = QFrame(self)
        self.picframe = QFrame(self)
        self.card1 = QFrame(self.buttonframe)
        self.card2 = QFrame(self.buttonframe)
        buttonslay = QGridLayout(self.buttonframe)

        piclay1 = QStackedLayout(self.card1)
        piclay2 = QStackedLayout(self.card2)
        piclay1.setStackingMode(1)
        piclay2.setStackingMode(1)

        bgpixmap = QPixmap("Image/Other/Button_bg.png")
        bgpixmap = bgpixmap.scaled(220, 220, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.bg_label1 = QLabel()
        self.bg_label1.setPixmap(bgpixmap)
        self.bg_label2 = QLabel()
        self.bg_label2.setPixmap(bgpixmap)
        self.bg_label1.hide()
        self.bg_label2.hide()
        pixmap = QPixmap("Image/Characters/Walle_set/Icon.png")
        # pixmap = pixmap.scaled(215, 215, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        pixmap_hover = pixmap
        pixmap_pressed = pixmap
        btn1 = custom_buttons.PicButton(pixmap, pixmap_hover, pixmap_pressed)
        btn1.clicked.connect(self.change_character1)
        pixmap = QPixmap("Image/Characters/Eve_set/Icon.png")
        pixmap_hover = pixmap
        pixmap_pressed = pixmap
        btn2 = custom_buttons.PicButton(pixmap, pixmap_hover, pixmap_pressed)
        btn2.clicked.connect(self.change_character2)
        piclay1.addWidget(btn1)
        piclay2.addWidget(btn2)
        piclay1.addWidget(self.bg_label1)
        piclay2.addWidget(self.bg_label2)

        lbl = QLabel()
        lbl.setText("""Выберите вашего помощника.\nВы всегда сможете сменить помощника,\nесли вам вдруг надоест.""")
        lbl.setStyleSheet(
            '''
            font:  22px;
            color: #002756;
            '''
        )
        lbl.setFont(QFont("Times"))
        lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl)

        buttonslay.setRowStretch(0, 1)
        buttonslay.setRowStretch(1, 1)
        buttonslay.setRowStretch(2, 1)

        buttonslay.setColumnStretch(0, 1)
        buttonslay.setColumnStretch(1, 1)
        buttonslay.setColumnStretch(2, 1)
        buttonslay.setColumnStretch(3, 1)
        buttonslay.setColumnStretch(4, 1)
        buttonslay.addWidget(self.card1, 1, 1)
        buttonslay.addWidget(self.card2, 1, 3)
        lay.addWidget(self.buttonframe)
        self.err_lbl = QLabel("")
        self.err_lbl.setStyleSheet(
            '''
            font:  20px;
            color: #002756;
            '''
        )
        lay.addWidget(self.err_lbl)
        lay.addWidget(self.picframe)

    def change_character1(self):
        self.character = "Walle"
        self.bg_label1.show()
        self.bg_label2.hide()

    def change_character2(self):
        self.character = "Eve"
        self.bg_label2.show()
        self.bg_label1.hide()


class Widget4(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        bye_lbl = QLabel()
        bye_lbl.setText("""Регистрация успешно завершена!\nПриятного время препровождения.""")
        bye_lbl.setStyleSheet(
            '''
            font:  30px;
            color: #002756;
            '''
        )
        bye_lbl.setAlignment(Qt.AlignCenter)
        bye_lbl.setFont(QFont("Times"))
        lay.addWidget(bye_lbl)


class Stacked(QWidget):
    def __init__(self, config, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setStyleSheet("background-image: ImageGif/Image/Main_bg.jpg;")
        self.setWindowTitle("Registration")
        self.setWindowIcon(QIcon("Image/Other/settings.png"))
        self.setFixedSize(700, 520)
        bg = QLabel()
        pixmap = QPixmap("Image/Other/Main_bg.png")
        mini_pix = pixmap.scaled(850, 580, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        bg.setPixmap(mini_pix)
        mlay = QStackedLayout(self)
        mlay.setStackingMode(1)
        self.config = config
        self.mframe = QFrame()
        lay = QVBoxLayout(self.mframe)
        self.W2 = Widget2()
        self.W3 = Widget3()
        self.Stack = QStackedWidget()
        self.Stack.addWidget(Widget1())
        self.Stack.addWidget(self.W2)
        self.Stack.addWidget(self.W3)
        self.Stack.addWidget(Widget4())
        self.btnNext = QPushButton("Next")
        self.btnNext.setStyleSheet(
            '''  
            QPushButton:hover { background-color: white;
            color: black;
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  25px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.btnNext.clicked.connect(self.onNext)
        self.btnNext.setFont(QFont("Times", 14))
        self.btnNext.setAutoDefault(True)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnNext)
        lay.addWidget(self.Stack)
        lay.addLayout(btnLayout)
        mlay.addWidget(self.mframe)
        mlay.addWidget(bg)

    def onNext(self):
        self.btnNext.show()
        if self.W2.enter.text() == "" and self.Stack.currentIndex() == 1:
            self.W2.lbl2.setText("\n\n\n\nКажется, вы забыли указать ваше имя")
            self.W2.enter.setFocus()
            return

        if self.W3.character == "" and self.Stack.currentIndex() == 2:
            self.W3.err_lbl.setText("Пожалуйста, выберите помощника")
            return

        if self.Stack.currentIndex() == 3:
            self.btnNext.setText("Finish")
            self.config["User"]["username"] = self.W2.enter.text()
            self.config["User"]["registered"] = "Yes"
            self.config["User"]["character"] = self.W3.character
            self.config["Exit"]["Answer_w1"] = "No"
            with open("Data/Config.ini", 'w') as configfile:
                self.config.write(configfile)
            self.close()

        if self.Stack.currentIndex() == 0:
            self.W2.enter.setFocus()
            self.W2.enter.returnPressed.connect(self.onNext)

        self.Stack.setCurrentIndex(self.Stack.currentIndex() + 1)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("Data/Config.ini", encoding='cp1251')
    config["User"]["registered"] = "No"
    with open("Data/Config.ini", 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    app = QApplication(sys.argv)
    w = Stacked(config)
    w.show()
    app.exec_()
