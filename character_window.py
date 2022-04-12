import json
import operator
import pickle
import threading
import webbrowser
import datetime
import easygui
import os
import platform
import re

from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QMessageBox, QMainWindow, QLabel, \
    QDialog, QApplication, QGridLayout, QSlider, QPushButton, QStackedLayout, QFrame
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot, QObject, Qt, QTimer, QSize, QRect
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from pip._vendor import requests

from dialog_window import Ui_Form
from enter_window import EnterField
from weather_widget import WeatherForm
import avatar_setup

import wordskey


class CustomWindow(QMainWindow):
    """
    Это класс основного окна, который связывает все, принимает только размеры.
    """
    change_textt = pyqtSignal(str)

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

    @pyqtSlot(str)
    def temp(self, text):
        self.change_textt.emit(text)

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
        # if x != int(self.config["Settings"]["window_pos_x"]) and y != int(self.config["Settings"]["window_pos_y"]):
        #     x = int(self.config["Settings"]["window_pos_x"])
        #     y = int(self.config["Settings"]["window_pos_y"])
        self.move(x, y)

    def initUI(self):
        self.size_change(self.size_win)
        self.child = Setup_size_window(config=self.config, win_CW=self)
        self.child.size_CW.connect(self.size_change)
        self.child.size_pic.connect(self.size_pic_change)
        self.pic_display()
        self.weatherWindow = WeatherForm(self.child)
        self.enterWindow = EnterWindow(win_size=self.child)
        self.quoteWindow = DialogWindow(self, win_size=self.child)
        self.flow.change_text_enter.connect(self.enterWindow.say.setText)
        self.quoteWindow.start_manual.connect(self.manual)

        self.flow.start_image.connect(self.change_pic)
        self.change_textt.connect(self.quoteWindow.input_comm)
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
        lay3.addWidget(self.weatherWindow, 0, 2)

        quoteLayout.addWidget(hframe)
        quoteLayout.addWidget(mframe)  #
        quoteLayout.addWidget(wframe)
        self.tab1.setLayout(quoteLayout)
        self.setCentralWidget(self.tab1)
        self.enterWindow.hide()
        self.quoteWindow.hide()
        self.choi_size_settin = 0

        self.timer_weather = QTimer(self)
        self.timer_weather.timeout.connect(self.changes_weat_time)

        self.timer_exit = QTimer(self)
        self.timer_exit.timeout.connect(self.changes_exit_time)
        self.flow.timer_exit.connect(self.timer_exit.start)

    def changes_weat_time(self):
        self.weatherWindow.hide()
        self.timer_weather.stop()

    def changes_exit_time(self):
        self.close()
        self.timer_exit.stop()


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
        self.flow.change_text.emit("Пока :(")
        self.quoteWindow.show()
        self.flow.listener.stop()

    def change_weather(self, weather):
        self.weatherWindow.show()
        self.timer_weather.start(3000)
        if weather == "ясно":
            self.weatherWindow.change_icon(weather)

        if weather == "пасмурно" or weather == "гроза с небольшим дождём":
            self.weatherWindow.change_icon(weather)
            # self.weatherWindow.show()

        if weather == "облачно с прояснениями":
            self.weatherWindow.change_icon(weather)
            # self.weatherWindow.show()

        if weather == "переменная облачность":
            self.weatherWindow.change_icon(weather)
            # self.weatherWindow.show()

        if weather == "небольшая облачность":
            self.weatherWindow.change_icon(weather)
            # self.weatherWindow.show()

        if weather == "небольшой дождь":
            self.weatherWindow.change_icon(weather)

        if weather == "небольшой проливной дождь":
            self.weatherWindow.change_icon(weather)

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
    size_weather = pyqtSignal(int)

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
            self.win2.input_comm(f'{comm}')
            self.say.setText(comm)
            self.edit_line.clear()
        else:
            self.say.clear()
            self.win2.textEdit.setText("Вы ничего не ввели.")


def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


@thread
def city_and_weather(signal, choi):
    try:
        send_url = "http://api.ipstack.com/check?access_key=c024957c288f813bf6f290a7182aa3d7"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        if choi == 0:
            signal.emit(geo_json)
            return 0

        elif choi == 1:
            city_id = geo_json["location"]["geoname_id"]
            appid = "3afeacd4d791d087699e1eef4315c1ec"
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                   params={'id': city_id, 'units': 'metric', 'lang': 'ru',
                                           'APPID': appid})
                data = res.json()
                signal.emit(data)
                return 0

            except:
                signal.emit({0: "К сожалению сервер не отвечает.\n"
                                "Попробуйте позже."})
                return 0
    except:
        signal.emit({0: "Похоже нет доступа к сети.\n"
                        "Попробуйте позже."})
        return 0


class DialogWindow(Ui_Form):
    """
    А тут почти всё, что связано с взаимодействием с пользователем
    """
    start_manual = pyqtSignal()
    th_signal_loc = pyqtSignal(dict)
    th_signal_weath = pyqtSignal(dict)

    def __init__(self, CW, win_size):
        super().__init__()
        self.CW = CW  # Для функции погоды
        self.win_size = win_size
        self.th_signal_weath.connect(self.show_weather, Qt.QueuedConnection)
        self.win_size.size_dialog.connect(self.size_change)
        self.num_brow = None  # Для изменения основного бразузера
        self.OPERATIONS = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.floordiv,
            '^': operator.pow,
        }

    @pyqtSlot(int)
    def size_change(self, size):
        self.label.setGeometry(QRect(0, 0, 260 * size / 100,
                                     300 * size / 1.00))

        self.mini_pix = self.pixmap.scaled(260 * size / 100,
                                           300 * size / 100,
                                           Qt.KeepAspectRatio, Qt.FastTransformation)

        self.label.setPixmap(self.mini_pix)

    # Обработка команд
    @pyqtSlot(str)
    def input_comm(self, command):
        #self.textEdit.append(f'Вы сказали - {command}')
        command = wordskey.words_recog(command)
        self.do_command(command)

    def get_number(self, varstr):
        s = ""
        if varstr[0] == '-':
            s += "-"
            varstr = varstr[1:]
        for c in varstr:
            if not c.isdigit():
                break
            s += c
        return int(s), len(s)

    def perform_operation(self, string, num1, num2):
        op = self.OPERATIONS.get(string, None)
        if op is not None:
            return op(num1, num2)
        else:
            return None

    def eval_math_expr(self, expr):
        while True:
            try:
                number1, end_number1 = self.get_number(expr)
                expr = expr[end_number1:]
                if expr == '':
                    return number1
                op = expr[0]
                expr = expr[1:]
                number2, end_number2 = self.get_number(expr)
                number1 = self.perform_operation(op, number1, number2)
            except Exception as e:
                break

            return number1

    def open_file_dir(self, result):
        with open("Pickle/path_base_win.pickle", "rb") as f:
            path = pickle.load(f)
        for i in path:
            i = r"\b" + f"{i}" + r"\b"
            i = re.search(i, result)
            if i:
                os.startfile(path[i[0]])
                return 0
        self.textEdit.setText("Такой папки/файла нет.")

    def browser(self, ans, brow, choi):
        if choi == 0:
            self.textEdit.setText("Открываю браузер (сайт - 'Яндекс').")
            webbrowser.get(brow).open("https://yandex.ru")
            return 0

        elif choi == 1:

            with open("Pickle/site_base.pickle", "rb") as f:
                data_site = pickle.load(f)

            for key in data_site:
                key = r"\b" + f"{key}" + r"\b"
                key = re.search(key, ans)
                if key:
                    self.textEdit.setText(f"Открываю {key[0]} в браузере.")
                    webbrowser.get(brow).open(key[0])
                    return 0

            self.textEdit.setText("Я не знаю такого сайта")


        elif choi == 3:
            self.textEdit.setText("Открываю новости.")
            webbrowser.get(brow).open("http://newslab.ru/news/")

        elif choi == 2:
            check_browser = ['Google', 'Netscape', 'Mozilla', 'Opera',
                             'Konqueror', 'Yandex', 'Safari', 'lynx']
            self.textEdit.setText("Выберите другой БРАУЗЕР в проводнике.")
            choice_br = easygui.fileopenbox(filetypes=['*.exe'], default="*.exe")
            ok = -1
            if choice_br != None:
                if str(choice_br[-4:]) == '.exe':
                    for i in range(len(check_browser)):
                        ok = choice_br.find(check_browser[i])
                        if ok != -1:
                            break
                    if ok == -1:
                        text, ok = QInputDialog.getText(self, 'Ввод ответа',
                                                        'Я не знаю такого браузера. '
                                                        'Вы уверены, что хотите изменить браузер?\n'
                                                        'Напишете да, иначе этот браузер не будет выбран.')
                        if ok and text:
                            text = str(text).lower()
                            if text == 'да':
                                return choice_br

                        else:
                            QMessageBox.warning(self, "Ошибка", "Вы ничего не ввели (отмена операции)")
                    elif ok != -1:
                        return choice_br
                else:
                    self.textEdit.setText('Вы не выбрали браузер.')
                    return 0
            else:
                self.textEdit.setText('Вы не выбрали браузер.')
                return 0


    def time_now(self, dat_time):
        now = datetime.datetime.now()
        answer = ["Время", "Дата"]
        if dat_time == answer[0]:
            return f"Сейчас - {now.hour}:{now.minute}:{now.second}."
        elif dat_time == answer[1]:
            return f"Сегодняшняя дата - {now.date().day}-{now.date().month}-{now.date().year}. "

    def system(self):
        sys = platform.uname()
        return "Информация о системе:\n" \
               f"    Имя системы/OS - {sys[0]}\n" \
               f"    Сетевое имя компьютера - {sys[1]}\n" \
               f"    Выпуск системы - {sys[2]}\n" \
               f"    Версия выпуска системы - {sys[3]}\n" \
               f"    Тип машины - {sys[4]}\n" \
               f"    Имя процессора - {sys[5]}"

    def show_weather(self, weath_data):
        if 'name' in weath_data:
            self.textEdit.setText("Погода на сегодня:")
            self.textEdit.append(f"{weath_data['weather'][0]['description']},")
            self.textEdit.append(f"температура: {weath_data['main']['temp']} °C,")
            self.textEdit.append(f"мин.: {weath_data['main']['temp_min']}")
            self.textEdit.append(f"макс.: {weath_data['main']['temp_max']}")
            weat = weath_data['weather'][0]['description']
            self.CW.change_weather(weat)
        else:
            self.textEdit.setText(f"{weath_data[0]}")

    def do_command(self, result):
        self.show()
        self.textEdit.setText("Выполняю...")

        if re.search(r"\bбраузер\b", f"{result}") and re.search(r"\bоткрой\b", f"{result}"):
            self.browser(result, self.num_brow, 0)

        elif re.search(r"\bсайт\b", f"{result}") and re.search(r"\bоткрой\b", f"{result}"):
            result = wordskey.site_recog(result)
            self.browser(result, self.num_brow, 1)

        elif re.search(r"\bизменить\b", f"{result}") and re.search(r"\bбраузер\b", f"{result}"):
            self.num_brow = self.browser(result, self.num_brow, 2)
            if self.num_brow != 0 and self.num_brow != None:
                webbrowser.register('Browser', None,
                                    webbrowser.BackgroundBrowser(self.num_brow))
                self.num_brow = 'Browser'
                self.textEdit.setText("Браузер успешно изменен, пока я работаю).")

        elif re.search(r"\bоткрой\b", f"{result}") and ((re.search(r"\bпапку\b", f"{result}"))
                                                        or (re.search(r"\bфайл\b", f"{result}"))):
            self.open_file_dir(result)

        elif re.search(r"\bвремя\b", f"{result}"):
            self.textEdit.setText(self.time_now("Время"))

        elif re.search(r"\bдата\b", f"{result}"):
            self.textEdit.setText(self.time_now("Дата"))

        elif re.search(r"\bсистема\b", f"{result}"):
            QMessageBox.about(self, "Ваша система", f"{self.system()}")

        elif re.search(r"\bумеешь\b", f"{result}") and re.search(r"\bчто\b", f"{result}"):
            self.start_manual.emit()

        elif re.search(r"\bновости\b", f"{result}"):
            self.browser(result, self.num_brow, 3)

        elif re.search(r"\bтебя\b", f"{result}") and re.search(r"\bзовут\b", f"{result}") \
                and re.search(r"\bкак\b", f"{result}"):
            self.textEdit.setText(f"Мое имя {self.config['User']['character']}")


        elif re.search(r"\bпогода\b", f"{result}"):
            self.textEdit.setText(f"Загружаю информацию о погоде...")
            city_and_weather(self.th_signal_weath, 1)

        elif re.search(r"\b\d+[-+*/^]?\d+\b", f"{result}"):
            expr = re.search(r"\b\d+[-+*/^]?\d+\b", f"{result}")[0]
            self.textEdit.setText(f"{expr}={self.eval_math_expr(expr)}")

        elif re.search(r"\bпока\b", f"{result}"):
            self.flow.close()

        else:
            self.textEdit.setText("Я такого ещё не знаю :(")