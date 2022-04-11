"""
Модуль, отвечающий за окно с настройками помощника.
Хоткеи, конфигфайл, масштабирование, быстрый доступ и даже всё цветные кнопочки - это всё тут.

p.s. Я сломал возможность изменять хоткеи поэтому надо подфиксить а пока закоментирую чтобы не тыкалось
"""

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTableWidget, QTableWidgetItem, \
    QMessageBox, QDesktopWidget, QWidget, QLabel, QPushButton, QTextEdit, QSlider
import sys
from configparser import ConfigParser
import pickle


class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigParser()
        self.config.read("Data/Config.ini")
        self.setupUi()
        self.setWindowIcon(QIcon("Image/Other/settings.png"))

    def setupUi(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(620, 520)
        self.setGeometry(50, 50, 620, 520)
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_size = (screen_geometry.width(), screen_geometry.height())
        win_size = (self.frameSize().width(), self.frameSize().height())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.setWindowTitle("Settings")

        self.Widget_1 = QWidget()
        self.Widget_1.setGeometry(QRect(0, 0, 620, 520))

        self.Widget_2 = QWidget()
        self.Widget_2.setGeometry(QRect(0, 0, 620, 520))

        self.Widget_3 = QWidget()
        self.Widget_3.setGeometry(QRect(0, 0, 620, 520))

        self.Widget_4 = QWidget()
        self.Widget_4.setGeometry(QRect(0, 0, 620, 520))

        pixmap = QPixmap("Image/Other/Main_bg.png")
        mini_pix = pixmap.scaled(620, 520, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.background_1 = QLabel(self.Widget_1)
        self.background_1.setGeometry(QRect(0, 0, 620, 520))
        self.background_1.setPixmap(mini_pix)

        self.background_2 = QLabel(self.Widget_2)
        self.background_2.setGeometry(QRect(0, 0, 620, 520))
        self.background_2.setPixmap(mini_pix)

        self.background_3 = QLabel(self.Widget_3)
        self.background_3.setGeometry(QRect(0, 0, 620, 520))
        self.background_3.setPixmap(mini_pix)

        self.background_4 = QLabel(self.Widget_4)
        self.background_4.setGeometry(QRect(0, 0, 620, 520))
        self.background_4.setPixmap(mini_pix)

        self.pushButton_5 = QPushButton(self.Widget_1)
        self.pushButton_5.setGeometry(QRect(250, 206, 120, 60))
        self.pushButton_5.setStyleSheet(
            '''  
            QPushButton:hover { background-color: rgba(255, 136, 255, 255);
            color: white;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(255, 100, 255, 100);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  20px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_2 = QPushButton(self.Widget_1)
        self.pushButton_2.setGeometry(QRect(20, 435, 111, 41))
        self.pushButton_2.setStyleSheet(
            '''  
            QPushButton:hover { background-color: red;
            color: white;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(255, 100, 255, 100);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  20px;
            color: #002756;
            padding: 1px;}
            '''
        )

        self.pushButton_3 = QPushButton(self.Widget_1)
        self.pushButton_3.setGeometry(QRect(550, 35, 40, 40))
        self.pushButton_3.setStyleSheet(
            '''  
            QPushButton:hover {background-color: rgba(87, 188, 255, 255);
            color: white;
            border-radius: 20px;}
            QPushButton:!hover { background-color: rgba(150, 200, 255, 200);
            border-width: 2px;
            border-style: solid;
            border-radius: 20px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_17 = QPushButton(self.Widget_1)
        self.pushButton_17.setGeometry(QRect(5, 210, 21, 51))
        self.pushButton_17.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover { background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_17.setText("<")
        self.pushButton_17.clicked.connect(self._on_back_tab)
        self.pushButton_18 = QPushButton(self.Widget_1)
        self.pushButton_18.setGeometry(QRect(594, 210, 21, 51))
        self.pushButton_18.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover { background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_18.setText(">")
        self.pushButton_18.clicked.connect(self._on_next_tab)

        self.label_2 = QLabel(self.Widget_2)
        self.label_2.setGeometry(QRect(50, 50, 171, 42))
        self.label_2.setStyleSheet(
            '''
            font:  16px;
            color: #002756;
            '''
        )

        self.label_3 = QLabel(self.Widget_2)
        self.label_3.setGeometry(QRect(50, 170, 151, 42))
        self.label_3.setStyleSheet(
            '''
            font:  16px;
            color: #002756;
            '''
        )

        self.label_4 = QLabel(self.Widget_2)
        self.label_4.setGeometry(QRect(50, 110, 111, 42))
        self.label_4.setStyleSheet(
            '''
            font:  16px;
            color: #002756;
            font-style: bold;
            '''
        )

        self.label_5 = QLabel(self.Widget_2)
        self.label_5.setGeometry(QRect(50, 230, 171, 42))
        self.label_5.setStyleSheet(
            '''
            font:  16px;
            color: #002756;
            '''
        )

        self.label_6 = QLabel(self.Widget_2)
        self.label_6.setGeometry(QRect(50, 290, 101, 42))
        self.label_6.setStyleSheet(
            '''
            font:  16px;
            color: #002756;
            '''
        )

        self.textEdit = QTextEdit(self.Widget_2)
        self.textEdit.setGeometry(QRect(210, 50, 161, 41))
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(f"{self.config['Hotkeys']['hotkey_1']}")
        self.textEdit.setStyleSheet(
            ''' 
            background-color: rgba(0, 0, 0, 00);
            font: bold 16px;
            color: #002756;
            border: 2px solid #002756;
            border-radius: 10px;
            '''
        )

        self.textEdit_2 = QTextEdit(self.Widget_2)
        self.textEdit_2.setGeometry(QRect(210, 110, 161, 41))
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setText(f"{self.config['Hotkeys']['hotkey_2']}")
        self.textEdit_2.setStyleSheet(
            ''' 
            background-color: rgba(0, 0, 0, 00);
            font: bold 16px;
            color: #002756;
            border: 2px solid #002756;
            border-radius: 10px;
            '''
        )

        self.textEdit_3 = QTextEdit(self.Widget_2)
        self.textEdit_3.setGeometry(QRect(210, 170, 161, 41))
        self.textEdit_3.setReadOnly(True)
        self.textEdit_3.setText(f"{self.config['Hotkeys']['hotkey_3']}")
        self.textEdit_3.setStyleSheet(
            ''' 
            background-color: rgba(0, 0, 0, 00);
            font: bold 16px;
            color: #002756;
            font-style: bold;
            border: 2px solid #002756;
            border-radius: 10px;
            '''
        )
        self.textEdit_4 = QTextEdit(self.Widget_2)
        self.textEdit_4.setGeometry(QRect(210, 230, 161, 41))
        self.textEdit_4.setReadOnly(True)
        self.textEdit_4.setText(f"{self.config['Hotkeys']['hotkey_4']}")
        self.textEdit_4.setStyleSheet(
            ''' 
            background-color: rgba(0, 0, 0, 00);
            font: bold 16px;
            color: #002756;
            border: 2px solid #002756;
            border-radius: 10px;
            '''
        )

        self.textEdit_5 = QTextEdit(self.Widget_2)
        self.textEdit_5.setGeometry(QRect(210, 290, 161, 41))
        self.textEdit_5.setReadOnly(True)
        self.textEdit_5.setText(f"{self.config['Hotkeys']['hotkey_5']}")
        self.textEdit_5.setStyleSheet(
            '''
            background-color: rgba(0, 0, 0, 00);
            font: bold 16px;
            color: #002756;
            border: 2px solid #002756;
            border-radius: 10px;
            '''
        )

        self.pushButton = QPushButton(self.Widget_2)
        self.pushButton.setGeometry(QRect(430, 50, 71, 33))
        self.pushButton.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_6 = QPushButton(self.Widget_2)
        self.pushButton_6.setGeometry(QRect(520, 50, 71, 33))
        self.pushButton_6.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: red;
            color: white;}
            QPushButton:!hover {background-color: rgba(255, 0, 0, 120);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_7 = QPushButton(self.Widget_2)
        self.pushButton_7.setGeometry(QRect(430, 110, 71, 33))
        self.pushButton_7.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_8 = QPushButton(self.Widget_2)
        self.pushButton_8.setGeometry(QRect(430, 170, 71, 33))
        self.pushButton_8.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_9 = QPushButton(self.Widget_2)
        self.pushButton_9.setGeometry(QRect(430, 290, 71, 33))
        self.pushButton_9.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_10 = QPushButton(self.Widget_2)
        self.pushButton_10.setGeometry(QRect(430, 230, 71, 33))
        self.pushButton_10.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )

        self.pushButton_12 = QPushButton(self.Widget_2)
        self.pushButton_12.setGeometry(QRect(520, 110, 71, 33))
        self.pushButton_12.setStyleSheet(
            '''  
            QPushButton:hover {background-color: red;
            color: white;}
            QPushButton:!hover {background-color: rgba(255, 0, 0, 120);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_13 = QPushButton(self.Widget_2)
        self.pushButton_13.setGeometry(QRect(520, 170, 71, 33))
        self.pushButton_13.setStyleSheet(
            '''  
            QPushButton:hover {background-color: red;
            color: white;}
            QPushButton:!hover {background-color: rgba(255, 0, 0, 120);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_14 = QPushButton(self.Widget_2)
        self.pushButton_14.setGeometry(QRect(520, 230, 71, 33))
        self.pushButton_14.setStyleSheet(
            '''
            QPushButton:hover {background-color: red;
            color: white;}
            QPushButton:!hover {background-color: rgba(255, 0, 0, 120);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_15 = QPushButton(self.Widget_2)
        self.pushButton_15.setGeometry(QRect(520, 290, 71, 33))
        self.pushButton_15.setStyleSheet(
            '''  
            QPushButton:hover {background-color: red;
            color: white;}
            QPushButton:!hover {background-color: rgba(255, 0, 0, 120);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )

        self.pushButton_19 = QPushButton(self.Widget_2)
        self.pushButton_19.setGeometry(QRect(5, 210, 21, 51))
        self.pushButton_19.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_19.setText("<")
        self.pushButton_19.clicked.connect(self._on_back_tab)
        self.pushButton_20 = QPushButton(self.Widget_2)
        self.pushButton_20.setGeometry(QRect(594, 210, 21, 51))
        self.pushButton_20.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_20.setText(">")
        self.pushButton_20.clicked.connect(self._on_next_tab)

        self.pB_del_account = QPushButton(self.Widget_1)
        self.pB_del_account.setGeometry(QRect(470, 435, 135, 41))
        self.pB_del_account.setStyleSheet(
            '''  
            QPushButton:hover {background-color: red;
            color: white;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(255, 100, 255, 100);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pB_del_account.setText("Delete account")
        self.pB_del_account.clicked.connect(self.del_account)
        self.pushButton_5.setText("Continue")
        self.pushButton_5.clicked.connect(self.save)
        self.pushButton_2.setText("Exit")
        self.pushButton_2.clicked.connect(self.exit_win)
        self.pushButton_3.setText("?")
        self.pushButton_3.clicked.connect(self.info)
        self.label_2.setText("Открыть/свернуть \nпомощника")
        self.label_3.setText("Закрыть окно \nуведомлений")
        self.label_4.setText("Голосовая \nкоманда")
        self.label_5.setText("Открыть/свернуть \nокно ввода")
        self.label_6.setText("Закрыть \nпомощника")

        self.pushButton.setText("Add key")
        # self.pushButton.clicked.connect(self.add_key_0)
        self.pushButton_7.setText("Add key")
        # self.pushButton_7.clicked.connect(self.add_key_1)
        self.pushButton_8.setText("Add key")
        # self.pushButton_8.clicked.connect(self.add_key_2)
        self.pushButton_9.setText("Add key")
        # self.pushButton_9.clicked.connect(self.add_key_3)
        self.pushButton_10.setText("Add key")
        # self.pushButton_10.clicked.connect(self.add_key_4)

        self.pushButton_6.setText("Del key")
        self.pushButton_6.clicked.connect(self.del_text)
        self.pushButton_12.setText("Del key")
        self.pushButton_12.clicked.connect(self.del_text_2)
        self.pushButton_13.setText("Del key")
        self.pushButton_13.clicked.connect(self.del_text_3)
        self.pushButton_14.setText("Del key")
        self.pushButton_14.clicked.connect(self.del_text_4)
        self.pushButton_15.setText("Del key")
        self.pushButton_15.clicked.connect(self.del_text_6)

        self.label_13 = QLabel(self.Widget_2)
        self.label_13.setGeometry(QRect(170, 400, 300, 60))
        self.label_13.setStyleSheet(
            '''
            font: bold 20px;
            color: #002756;
            '''
        )
        self.label_13.setText("     Нажмите клавишу,\n"
                              "которую хотите добавить")
        self.label_13.hide()

        self.label_8 = QLabel(self.Widget_3)
        self.label_8.setGeometry(QRect(230, 170, 80, 40))
        self.label_8.setStyleSheet(
            '''
            font:  20px;
            color: #002756;
            '''
        )
        self.label_8.setText("Размер:")
        self.value = int(self.config["Settings"]["window_scale"])
        self.line1 = QLabel(self.Widget_3)
        self.line1.setText(str(self.value) + "%")
        self.line1.setGeometry(QRect(310, 170, 80, 40))
        self.line1.setStyleSheet(
            '''
            font:  20px;
            color: #002756;
            '''
        )
        self.slider = QSlider(Qt.Horizontal, self.Widget_3)
        self.slider.setGeometry(QRect(212, 218, 200, 40))
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(25)
        self.slider.setSingleStep(5)
        self.slider.setRange(25, 200)
        self.slider.setValue(self.value)
        self.slider.valueChanged[int].connect(self.change_value)
        self.bt1 = QPushButton("OK", self.Widget_3)
        self.bt1.clicked.connect(self.on_click)
        self.bt1.setGeometry(QRect(200, 400, 70, 30))
        self.bt1.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  20px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.cbt = QPushButton("Cancel", self.Widget_3)
        self.cbt.setGeometry(QRect(350, 400, 70, 30))
        self.cbt.clicked.connect(self.cancel_size)
        self.cbt.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: red;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(255, 0, 0, 120);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  20px;
            color: #002756;
            padding: 1px;}
            '''
        )

        self.pushButton_21 = QPushButton(self.Widget_3)
        self.pushButton_21.setGeometry(QRect(5, 210, 21, 51))
        self.pushButton_21.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover { background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_21.setText("<")
        self.pushButton_21.clicked.connect(self._on_back_tab)
        self.pushButton_22 = QPushButton(self.Widget_3)
        self.pushButton_22.setGeometry(QRect(594, 210, 21, 51))
        self.pushButton_22.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover { background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_22.setText(">")
        self.pushButton_22.clicked.connect(self._on_next_tab)

        with open("Pickle/path_base_win.pickle", "rb") as f:
            self.path = pickle.load(f)

        self.table = QTableWidget(self.Widget_4)                                                # Тут создается таблица
        self.table.setGeometry(QRect(30, 40, 551, 350))
        self.table.setStyleSheet(
            '''
            QTableWidget { 
            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.65, y2: 0.5,
            stop: 0  #002756 stop: 1 #55aaff);background: transparent;
            font-size: 12pt; border: 2px outset #002756;color: #002756} 
            QWidget {background-color: transparent;color: #002756}
            QHeaderView::section {background-color: transparent; padding: 2px; 
            border: 2px solid #002756; font-size: 14pt}
            QTableWidget QTableCornerButton::section {
            background-color: transparent;
            border: 2px solid #002756}                 
            '''
        )

        """
        
        ТУТ НАДА ТАБЛИЦУ ДЕЛАТЬ!!!!!!!!1!!!!11!1!!
        
        """

        self.tab_pb_2 = QPushButton("Удалить", self.Widget_4)
        self.tab_pb_2.setGeometry(QRect(500, 400, 80, 32))
        self.tab_pb_2.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: red;
            color: white;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(255, 0, 0, 120);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )

        self.tab_pb_3 = QPushButton("Добавить файл", self.Widget_4)
        self.tab_pb_3.setGeometry(QRect(40, 400, 130, 32))
        self.tab_pb_3.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )

        self.tab_pb_4 = QPushButton("Добавить папку", self.Widget_4)
        self.tab_pb_4.setGeometry(QRect(185, 400, 130, 32))
        self.tab_pb_4.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )

        self.pushButton_23 = QPushButton(self.Widget_4)
        self.pushButton_23.setGeometry(QRect(5, 210, 21, 51))
        self.pushButton_23.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover { background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_23.setText("<")
        self.pushButton_23.clicked.connect(self._on_back_tab)
        self.pushButton_24 = QPushButton(self.Widget_4)
        self.pushButton_24.setGeometry(QRect(594, 210, 21, 51))
        self.pushButton_24.setStyleSheet(
            '''  
            QPushButton:hover {background-color: white;
            color: #002756;
            border-radius: 10px;}
            QPushButton:!hover { background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            font:  16px;
            color: #002756;
            padding: 1px;}
            '''
        )
        self.pushButton_24.setText(">")
        self.pushButton_24.clicked.connect(self._on_next_tab)

        self.num_page = 0
        self.tab = QTabWidget()
        self.tab.addTab(self.Widget_1, "Меню ")
        self.tab.addTab(self.Widget_2, "Горячие клавиши ")
        self.tab.addTab(self.Widget_3, "Размер ")
        self.tab.addTab(self.Widget_4, "Быстрый доступ ")
        self.tab.setStyleSheet(
            '''
            QTabWidget::pane {border:0} 
            QTabWidget::tab-bar {left: 5px;}
            QTabBar::tab {background: #ffaaff; padding: 10px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px; 
            color: #002756}
            QTabBar::tab:selected, QTabBar::tab:hover {
            background: #ff88ff;
            color: white}
            QTabBar::tab:selected {background: #ff66ff; color: white}
            QTabBar::tab:!selected {margin-top: 4px}    
            QTabBar::tab:selected {margin-left: -4px; margin-right: -4px}
            QTabBar::tab:first:selected {margin-left: 0}
            QTabBar::tab:last:selected {margin-right: 0}
           '''
        )
        self.setCentralWidget(self.tab)

        # self.thread = ThreadWin(main=self, config=self.config)
        # self.thread.change.connect(self.textEdit.setText)
        # self.thread.change_2.connect(self.textEdit_2.setText)
        # self.thread.change_3.connect(self.textEdit_3.setText)
        # self.thread.change_4.connect(self.textEdit_4.setText)
        # self.thread.change_5.connect(self.textEdit_5.setText)
        # self.choi = 0

    def _on_next_tab(self):
        if self.num_page == 3:
            self.num_page = 0
        else:
            self.num_page += 1
        self.tab.setCurrentIndex(self.num_page)

    def _on_back_tab(self):
        if self.num_page == 0:
            self.num_page = 3
        else:
            self.num_page -= 1
        self.tab.setCurrentIndex(self.num_page)

    def del_account(self):
        self.config["User"]["registered"] = "No"
        self.config["Hotkeys"]["hotkey_1"] = "<ctrl>+q"
        self.config["Hotkeys"]["hotkey_2"] = "<alt>"
        self.config["Hotkeys"]["hotkey_3"] = "`"
        self.config["Hotkeys"]["hotkey_4"] = "<ctrl>+<shift>"
        self.config["Hotkeys"]["hotkey_5"] = "<alt>+<f4>"
        self.config["Settings"]["window_scale"] = "100"
        self.config["Settings"]["window_pos_x"] = "1370"
        self.config["Settings"]["window_pos_y"] = "475"
        with open("Data/Config.ini", 'w') as configfile:
            self.config.write(configfile)

        self.path = {}
        with open("Pickle/path_base_win.pickle", "wb") as f:
            pickle.dump(self.path, f)

        self.close()

    def info(self):
        QMessageBox.about(self, 'О программе:',
                          '=)')

    def cancel_size(self):
        self.value = int(self.config["Settings"]["window_scale"])
        self.slider.setValue(self.value)

    def change_value(self, value):
        self.value = value
        self.line1.setText(str(self.value) + "%")

    def on_click(self):
        self.config["Settings"]["window_scale"] = str(self.value)

    def save(self):
        self.config["Exit"]["Answer_w2"] = "No"
        with open("Pickle/path_base_win.pickle", "wb") as f:
            pickle.dump(self.path, f)
        with open("Data/Config.ini", 'w') as configfile:
            self.config.write(configfile)
        self.close()

    def cancel(self):
        self.config["Exit"]["Answer_w2"] = "No"
        with open("Data/Config.ini", 'w') as configfile:
            self.config.write(configfile)
        self.close()

    def exit_win(self):
        self.close()

    def del_text(self):
        self.textEdit.setText("")
        text = self.textEdit.toPlainText()
        self.config['Hotkeys']['hotkey_1'] = text

    def del_text_2(self):
        self.textEdit_2.setText("")
        text = self.textEdit_2.toPlainText()
        self.config['Hotkeys']['hotkey_2'] = text

    def del_text_3(self):
        self.textEdit_3.setText("")
        text = self.textEdit_3.toPlainText()
        self.config['Hotkeys']['hotkey_3'] = text

    def del_text_4(self):
        self.textEdit_4.setText("")
        text = self.textEdit_4.toPlainText()
        self.config['Hotkeys']['hotkey_4'] = text

    def del_text_6(self):
        self.textEdit_5.setText("")
        text = self.textEdit_5.toPlainText()
        self.config['Hotkeys']['hotkey_5'] = text

    # def add_key_0(self):
    #     self.pushButton.hide()
    #     self.label_13.show()
    #     self.thread.start()
    #
    # def add_key_1(self):
    #     self.choi = 1
    #     self.pushButton_7.hide()
    #     self.label_13.show()
    #     self.thread.start()
    #
    # def add_key_2(self):
    #     self.choi = 2
    #     self.pushButton_8.hide()
    #     self.label_13.show()
    #     self.thread.start()
    #
    # def add_key_3(self):
    #     self.choi = 3
    #     self.pushButton_9.hide()
    #     self.label_13.show()
    #     self.thread.start()
    #
    # def add_key_4(self):
    #     self.choi = 4
    #     self.pushButton_10.hide()
    #     self.label_13.show()
    #     self.thread.start()


if __name__ == '__main__':
    app_1 = QApplication(sys.argv)
    w = Settings()
    w.show()
    app_1.exec_()
