import operator
import pickle
import webbrowser
import datetime
import easygui
import os
import platform
import re

from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import wordskey

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

from enter_window import EnterWindow
from weather_widget import WeatherForm
import avatar_setup

import wordskey


"""
Модуль с настройкой диалогового облачка помощника
"""

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
        self.textEdit.append(f'Вы сказали - {command}')
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