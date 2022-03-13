from PyQt5.QtWidgets import QWidget, QFrame, QStackedLayout, QLabel, QTextEdit, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, QSize, Qt, QMetaObject
import configparser


class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read("Data/Config.ini")
        self.size_win = int(self.config["Settings"]["window_scale"])
        self.setupUi()

    def setupUi(self):
        self.frame = QFrame()
        self.frame.resize(100, 250)

        grid = QStackedLayout(self.frame)
        grid.setStackingMode(1)

        self.bgFrame = QFrame(self.frame)
        self.UIFrame = QFrame(self.frame)
        self.EditFrame = QFrame(self.UIFrame)

        self.label = QLabel(self.frame)
        self.label.setGeometry(QRect(0, 0, round(260 * self.size_win/ 100),
                                            round(300 * self.size_win / 100)))
        self.label.setMinimumSize(QSize(110, 110))
        self.label.setText("")
        self.pixmap = QPixmap("Image/Other/dialog_l.png")
        self.mini_pix = self.pixmap.scaled(round(260 * self.size_win / 100),
                                 round(300 * self.size_win / 100),
                                 Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.setPixmap(self.mini_pix)
        self.label.setObjectName("label")

        # Поле вывода
        self.textEdit = QTextEdit(self.EditFrame)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.textEdit.setWindowOpacity(0.5)
        self.textEdit.setStyleSheet(
            '''
            QTextEdit{
            background: rgba(0, 0, 0, 00);
            font:  15px;
            color: #002756;
            border: None;
            font-style: italic};
            '''
        )
        EditLay = QVBoxLayout(self.EditFrame)
        EditLay.addWidget(self.textEdit)

        UILay = QGridLayout(self.UIFrame)
        UILay.setRowStretch(0, 2)
        UILay.setRowStretch(1, 10)
        UILay.setRowStretch(2, 8)
        UILay.setColumnStretch(0, 2)
        UILay.setColumnStretch(1, 10)
        UILay.setColumnStretch(2, 2)

        grid.addWidget(self.label)
        UILay.addWidget(self.EditFrame, 1, 1)
        grid.addWidget(self.UIFrame)
        self.setLayout(grid)

        QMetaObject.connectSlotsByName(self.frame)
