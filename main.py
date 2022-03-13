import sys
from pynput import keyboard
import speech_recognition as sr
from configparser import ConfigParser
import types
import datetime
import threading
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from character_window import CustomWindow
from register_window import stackedExample
from settings import Settings


def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper


@thread
def say(signal, text):
    recor = sr.Recognizer()
    micro = sr.Microphone(device_index=None)

    with micro as source:
        recor.adjust_for_ambient_noise(source, duration=1)
        text.emit("Слушаю...")
        audio = recor.listen(source)
    try:
        task = recor.recognize_google(audio, language="ru-RU").lower()

    except sr.UnknownValueError:
        task = "?"

    signal.emit(task)


class TheThread(QThread):
    start_new_gif = pyqtSignal(str)
    change_text = pyqtSignal(str)
    timer_gif = pyqtSignal(int)
    timer_exit = pyqtSignal(int)
    voice = pyqtSignal(str)
    proc_comm = pyqtSignal(str)
    change_text_enter = pyqtSignal(str)
    """
    Короче второй поток, в котором горячие клавиши и голосовой ввод.
    """

    def __init__(self, config):
        super().__init__()

        self.config = 0
        self.win_check = True                                                       # Проверка на отрытие основного окна
        self.ent_check = False                                              # Проверка на октрытие текстового окна ввода
        self.voice_check = 0                                                       # Проверка на запуск голосового ввода
        self.num = 2
        self.config = config
        self.voice.connect(self.say_command, QtCore.Qt.QueuedConnection)
        self.character = self.config["User"]["character"]
        self.base_gif = "Image/Characters/%s_set/%s_main.png" % (self.character, self.character)

    # Хоткейс
    def run(self):
        hotkeys = {}
        hotkey1 = self.config['Hotkeys']['hotkey_1']
        if hotkey1:
            hotkeys[hotkey1] = self.show_and_close_win
        hotkey2 = self.config['Hotkeys']['hotkey_2']
        if hotkey2:
            hotkeys[hotkey2] = self.start_say
        hotkey3 = self.config['Hotkeys']['hotkey_3']
        if hotkey3:
            hotkeys[hotkey3] = self.close_ob
        hotkey4 = self.config['Hotkeys']['hotkey_4']
        if hotkey4:
            hotkeys[hotkey4] = self.enter
        hotkey5 = self.config['Hotkeys']['hotkey_5']
        if hotkey5:
            hotkeys[hotkey5] = self.close
        if hotkeys:
            with keyboard.GlobalHotKeys(hotkeys) as self.listener:
                self.listener.join()

    def tray_start(self):
        self.menu = QMenu()
        self.menu.setStyleSheet(
            '''  
            QMenu{
            background-image: url(Image/Other/Tray2.png); 
            border: 1px solid black;
            font:  16px;
            color: #002756;
            }
            QMenu::item {
            background-color: transparent;
            }
            QMenu::item:selected { /* when user selects item using mouse or keyboard */
            background-color: white;
            }
            '''
        )
        icon = "Image/Characters/%s_set/Icon.png" % (self.character)
        self.icon = QSystemTrayIcon(QIcon(icon))
        menu = {"Ввод": self.enter,  "Голосовой ввод":self.start_say,
                "Свернуть/развернуть в трей": self.show_and_close_win,
                "Размер": self.window.show_size_setup,
                "Закрыть окно уведомлений":self.close_ob,
                "Выход": self.close}
        if not menu:
            menu = []
        items = []
        functions = []
        for elem in menu:
            items.append(elem)
            functions.append(menu[elem])

        for i, item in enumerate(items):
            function = functions[i]
            if isinstance(function, types.MethodType) \
                    or isinstance(function, types.FunctionType):
                self.menu.addAction(QAction(item, self,
                                            triggered=function))
        self.icon.setContextMenu(self.menu)
        self.icon.show()

    def pic_display(self):
        if self.num == 1:
            self.num = 2
            self.start_new_gif.emit(self.base_gif)

        elif self.num == 2:
            self.num = 1
            self.start_new_gif.emit(self.speak_gif)
        self.window.choi_timer = 0
        self.timer_gif.emit(3000)

    # Метод для закрытия и открытия основного окна
    def show_and_close_win(self):
        if self.window:
            if self.win_check == False:
                self.win_check = True
                self.window.show()

            elif self.win_check == True:
                self.win_check = False
                self.window.hide()

    # Метод для запуска голосового ввода
    def start_say(self):
        if self.voice_check == 0:
            self.voice_check = 1
            self.window.show()
            self.window.quoteWindow.show()
            say(self.voice, self.change_text)

    # Закрыть поле вывода помощника
    def close_ob(self):
        if self.window:
            text = ""
            self.change_text.emit(text)
            self.window.quoteWindow.hide()

    # Открытие и закрытие окна ввода
    def enter(self):
        if self.window:
            self.window.show()
            if self.ent_check == False:
                self.ent_check = True
                self.window.enterWindow.win2 = self.window.quoteWindow
                self.window.enterWindow.edit_line.setFocus()
                self.window.enterWindow.show()
                self.change_text.emit("Пишите...")


            elif self.ent_check == True:
                self.ent_check = False
                self.window.enterWindow.hide()
                comm = "Вводимый текст"
                self.change_text_enter.emit(f"{comm}")

    # Закрытие
    def close(self):
        if self.window:
            self.window.exit()

    # Метод для получения времени
    def change_window(self, window):
        self.window = window
        hour = datetime.datetime.now().hour
        if 0 <= hour < 5:
            self.change_text.emit(f"- Доброй ночи, {self.config['User']['username']}")
        elif 5 <= hour < 12:
            self.change_text.emit(f"- Доброе утро, {self.config['User']['username']}")
        elif 12 <= hour < 16:
            self.change_text.emit(f"- Добрый день, {self.config['User']['username']}")
        elif 16 <= hour <= 23:
            self.change_text.emit(f"- Добрый вечер, {self.config['User']['username']}")

        self.window.quoteWindow.show()

    def say_command(self, say_comm):
        """
        Тут будет голосовой ввод
        """
        return 1


def main():
    config = ConfigParser()
    config.read("Data/Config.ini")
    if config["User"]["registered"] == "No":
        config["Exit"]["Answer_w1"] = "Yes"
        with open("Data/Config.ini", 'w') as configfile:
            config.write(configfile)
        app_1 = QApplication(sys.argv)
        w = stackedExample(config)
        w.show()
        app_1.exec_()

    config.read("Data/Config.ini")

    if config["Exit"]["Answer_w1"] == "No":
        config["Exit"]["Answer_w2"] = "Yes"
        with open("Data/Config.ini", 'w') as configfile:
            config.write(configfile)
        app_2 = QApplication(sys.argv)
        settings = Settings()
        settings.show()
        app_2.exec_()

    config.read("Data/Config.ini")

    if config["Exit"]["Answer_w2"] == "No":
        app_3 = QApplication(sys.argv)
        thread1 = TheThread(config=config)
        thread1.start()
        window = CustomWindow(config, flow=thread1)
        window.show()
        thread1.change_window(window=window)
        thread1.tray_start()
        app_3.exec_()


if __name__ == "__main__":
    main()
