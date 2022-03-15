import threading
from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QMessageBox, QMainWindow, QLabel, \
    QDialog, QApplication, QGridLayout, QSlider, QPushButton, QStackedLayout, QFrame
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, QObject, Qt, QTimer, QSize, QRect
from PyQt5.QtGui import QPixmap, QIcon, QMovie

from dialog_window import Ui_Form
from enter_window import EnterField
import avatar_setup

class CustomWindow(QMainWindow):
    """
    Так-ссс, этот класс основное окно, которое связывает все, принимает только размеры.
    """
    def __init__(self, config, flow, parent=None):
        super(CustomWindow, self).__init__(parent)
        self.config = config
        character = config["User"]["character"]
        self.flow = flow

        # Натройка визуала самого окна, прозрачноть и т д и т п
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Helper")
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowIcon(QIcon("Image/Characters/%s_set/Icon.png" % (character)))

        self.path = config["Path"]["%s" % (character)]
        self.size_win = int(config["Settings"]["window_scale"])
        self.config = config
        self.child = None
        self.initUI()

        self.setWindowFlag(Qt.WindowStaysOnTopHint)                    # Флаг для того, чтобы дп весел поверх всех окон

    @pyqtSlot(int)
    def size_pic_change(self, size):
        self.l.m.stop()
        self.l.size_win = size
        self.l.setMovie(self.l.m)
        self.l.m.start()
        self.l.adjustSize()

    @pyqtSlot(int)
    def size_change(self, size):
        self.win_size = [round((int(self.config["Settings"]["Window_size_w"]) *
                          size / 100) * 1.1),
                         round((int(self.config["Settings"]["Window_size_h"]) *
                          size / 100) * 1.1)]
        self.setGeometry(50, 50, self.win_size[0], self.win_size[1])
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_size = (screen_geometry.width(), screen_geometry.height())
        win_size = (self.frameSize().width(), self.frameSize().height())
        x = screen_size[0] - win_size[0]
        y = screen_size[1] - win_size[1]
        if x != int(self.config["Settings"]["window_pos_x"]) and y != int(self.config["Settings"]["window_pos_y"]):
            x = int(self.config["Settings"]["window_pos_x"])
            y = int(self.config["Settings"]["window_pos_y"])
        self.move(x, y)

    def initUI(self):
        self.size_change(self.size_win)
        self.child = Setup_size_window(config=self.config, win_CW=self)
        self.child.size_CW.connect(self.size_change)
        self.child.size_pic.connect(self.size_pic_change)
        self.pic_display()
        self.enterWindow = EnterWindow(win_size=self.child)
        self.quoteWindow = DialogWindow(self, win_size=self.child)
        self.quoteWindow.start_manual.connect(self.manual)

        self.flow.start_image.connect(self.change_pic)
        self.flow.change_text.connect(self.quoteWindow.textEdit.setText)

        self.tab1 = QWidget()
        quoteLayout = QStackedLayout()
        quoteLayout.setStackingMode(1)
        mframe = QFrame(self.tab1)
        hframe = QFrame(self.tab1)
        wframe = QFrame(self.tab1)
        lay = QGridLayout(mframe)
        lay.setRowStretch(0, 1)
        lay.setRowStretch(1, 1)
        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 1)
        lay.addWidget(self.quoteWindow, 0, 0)
        mframe.setLayout(lay)

        lay2 = QGridLayout(hframe)
        lay2.setRowStretch(0, 5)
        lay2.setRowStretch(1, 1)
        lay2.setColumnStretch(0, 5)
        lay2.setColumnStretch(1, 1)
        lay2.addWidget(self.enterWindow, 1, 0)

        lay3 = QGridLayout(wframe)
        lay3.setRowStretch(0, 1)
        lay3.setRowStretch(1, 1)
        lay3.setRowStretch(2, 1)
        lay3.setColumnStretch(0, 1)
        lay3.setColumnStretch(1, 1)
        lay3.setColumnStretch(2, 1)
        quoteLayout.addWidget(hframe)
        quoteLayout.addWidget(mframe)  #
        quoteLayout.addWidget(wframe)
        self.tab1.setLayout(quoteLayout)
        self.setCentralWidget(self.tab1)
        self.enterWindow.hide()
        self.quoteWindow.hide()
        self.choi_size_settin = 0

    @pyqtSlot(str)
    def change_pic(self, path):
        self.l.m.stop()
        self.l.m.setFileName(path)
        self.l.m.start()

    # Изменение размеров
    def show_size_setup(self):
        if self.choi_size_settin == 0:
            self.choi_size_settin = 1
            self.child.show()

    # вызывается при нажатии кнопки мыши
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    # вызывается при отпускании кнопки мыши
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
            self.config["Settings"]["window_pos_x"] = str(self.x())
            self.config["Settings"]["window_pos_y"] = str(self.y())
            with open("Data/Config.ini", 'w') as configfile:
                self.config.write(configfile)

    # вызывается всякий раз, когда мышь перемещается
    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)


    # Изменение аватара
    def change_character(self):
        self.CHS = avatar_setup.Character_setup(self.config)
        self.CHS.show()

    def pic_display(self):
        self.l = QMovieLabel(self.path, self.config, self)
        self.l.adjustSize()
        self.l.show()

    def exit(self):
        self.flow.timer_exit.emit(2000)
        self.show()
        self.flow.start_image.emit(self.flow.speak_gif)
        self.flow.change_text.emit("До встречи :(")
        self.quoteWindow.show()
        self.flow.listener.stop()

    @pyqtSlot()
    def manual(self):
        QMessageBox.about(self, 'О программе:',
                          '=)')


class QMovieLabel(QLabel):
    def __init__(self, filename, config, parent=None):
        super(QMovieLabel, self).__init__(parent)
        self.m = QMovie(filename)
        self.config = config
        self.size_win = int(self.config["Settings"]["window_scale"])
        self.setMovie(self.m)
        self.m.start()

    def setMovie(self, movie):
        super(QMovieLabel, self).setMovie(movie)

        s = movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()
        movie = self.movie()

        x = round(int(self.config["Settings"]["Window_size_w"]) *
             self.size_win / 100)
        y = round(int(self.config["Settings"]["Window_size_h"]) *
             self.size_win / 100)
        movie.setScaledSize(QSize(x, y))
        self.adjustSize()
        self.move(90 *
                  round(self.size_win / 100), 55 *
                  round(self.size_win / 100))


class Setup_size_window(QDialog):
    size_pic = pyqtSignal(int)
    size_ent = pyqtSignal(int)
    size_CW = pyqtSignal(int)
    size_dialog = pyqtSignal(int)

    def __init__(self, config, win_CW):
        super(Setup_size_window, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("Image/Other/settings.png"))
        self.win_CW = win_CW
        self.size = []
        self.value = int(config["Settings"]["window_scale"])
        self.config = config
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 200, 150)

        screen_geometry = QApplication.desktop().availableGeometry()
        screen_size = (screen_geometry.width(), screen_geometry.height())
        x = screen_size[0] - int(self.config["Settings"]["Window_size_w"])
        y = screen_size[1] - int(self.config["Settings"]["Window_size_h"])
        self.move(x, y)

        Glayout = QGridLayout(self)
        self.label_1 = QLabel(self)
        self.label_1.setGeometry(QRect(0, 0, 200, 150))
        self.pixmap = QPixmap("Image/Other/Tray1.png")
        self.mini_pix = self.pixmap.scaled(200, 150, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.label_1.setPixmap(self.mini_pix)
        self.line1 = QLabel(self)
        self.line1.setText(str(self.value) + "%")
        self.line1.setStyleSheet(
            '''
            font:  16px;
            color: white;
            font-style: italic;
            '''
        )
        Glayout.addWidget(self.line1, 1, 2)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(25)
        self.slider.setSingleStep(5)
        self.slider.setRange(25, 200)
        self.slider.setValue(self.value)
        self.slider.valueChanged[int].connect(self.change_value)
        Glayout.addWidget(self.slider, 1, 1)

        self.bt1 = QPushButton("OK", self)
        self.bt1.clicked.connect(self.on_click)
        self.bt1.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: white;
            font-style: italic;
            padding: 1px;}
            '''
        )
        Glayout.addWidget(self.bt1, 3, 2)

        self.cbt = QPushButton("Cancel", self)
        self.cbt.clicked.connect(self.cancel)
        self.cbt.setStyleSheet(
            ''' 
            QPushButton:hover {background-color: white;
            color: #002756;}
            QPushButton:!hover {background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            font:  16px;
            color: white;
            font-style: italic;
            padding: 1px;}
            '''
        )
        Glayout.addWidget(self.cbt, 3, 1)
        self.setLayout(Glayout)

    def cancel(self):
        self.win_CW.choi_size_settin = 0
        self.close()

    def change_value(self, value):
        self.value = value
        self.line1.setText(str(self.value) + "%")

    def on_click(self):
        width = int(self.config["Settings"]["Window_size_w"])
        height = int(self.config["Settings"]["Window_size_h"])
        width = width * self.value / 100
        height = height * self.value / 100
        self.size_CW.emit(int(self.value))
        self.size_pic.emit(int(self.value))
        self.size_dialog.emit(int(self.value))
        self.size_ent.emit(int(self.value))
        self.size_weather.emit(int(self.value))
        self.config["Settings"]["window_scale"] = str(self.value)

        with open("Data/Config.ini", 'w') as configfile:
            self.config.write(configfile)
        self.win_CW.choi_size_settin = 0
        self.close()


class EnterWindow(EnterField):
    def __init__(self, win_size):
        super().__init__()
        self.win_size = win_size
        self.win_size.size_ent.connect(self.size_change)
        self.win2 = 0
        self.edit_line.returnPressed.connect(self.input_comm)

    @pyqtSlot(int)
    def size_change(self, size):
        width = 445 * size / 100
        height = 100 * size / 100
        self.scale = int(size / 100 * 18)
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
        self.edit_line.setStyleSheet(
            '''
            background-color: rgba(0, 0, 0, 00);
            border-width: 2px;
            border-style: solid;
            border-radius: 10px;
            border-color: %s;
            font:  %s;
            color: %s;
            font-style: italic;
            min-width: 10em;
            padding: 6px;
            ''' % (self.border_color,
                   self.font_color,
                   str(self.scale) + 'px'))
        self.label.setStyleSheet(
            '''
            font:  %s;
            color: %s;
            font-style: italic;
            padding: 6px;
            ''' % (str(self.scale) + 'px',
                   self.font_color))

    def input_comm(self):
        comm = f'{self.edit_line.text()} '
        if len(comm) > 1:
            self.edit_line.clear()
        else:
            self.win2.textEdit.setText("Вы ничего не ввели.")


class DialogWindow(Ui_Form):
    """
    А тут будет почти всё, что связано с взаимодействием с пользователем
    """
    start_manual = pyqtSignal()

    def __init__(self, CW, win_size):
        super().__init__()
        self.win_size = win_size
        self.win_size.size_dialog.connect(self.size_change)

    @pyqtSlot(int)
    def size_change(self, size):
        self.label.setGeometry(QRect(0, 0, 260 * size / 100,
                                     300 * size / 1.00))

        self.mini_pix = self.pixmap.scaled(260 * size / 100,
                                           300 * size / 100,
                                           Qt.KeepAspectRatio, Qt.FastTransformation)

        self.label.setPixmap(self.mini_pix)
