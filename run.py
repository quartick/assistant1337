"""
Модуль, отвечающий за связный запуск основной визуальной части
и некоторых доступных действий помощника.
"""
import sys
import threading

from pynput import keyboard
import dialog_window

from settings import Settings
import speech_manager
import types
import datetime
from character_window import DialogWindow

from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QAction, QWidget, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QIcon



class Runner(QThread):
    start_image = pyqtSignal(str)
    change_text = pyqtSignal(str)
    change_text_enter = pyqtSignal(str)
    timer_exit = pyqtSignal(int)
    proc_comm = pyqtSignal(str)
    voice = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()

        self.settings_class = Settings()
        self.config = 0
        self.command = ""
        self.win_check = True                                                       # Проверка на отрытие основного окна
        self.ent_check = False                                              # Проверка на октрытие текстового окна ввода
        self.voice_check = 0                                                       # Проверка на запуск голосового ввода
        self.quote = True
        self.config = config
        self.voice.connect(self.say_command, QtCore.Qt.QueuedConnection)
        self.character = self.config["User"]["character"]
        self.image = "Image/Characters/%s_set/%s_main.png" % (self.character, self.character)

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
        menu = {"Ввод": self.enter,  "Голосовой ввод": self.start_say,
                "Свернуть/развернуть в трей": self.show_and_close_win,
                "Размер": self.window.show_size_setup,
                "Закрыть окно уведомлений": self.close_ob,
                "Настройки": self.settings,
                "Выход": self.close}
        # if not menu:
        #     menu = []
        items = []
        functions = []
        for elem in menu:
            items.append(elem)
            functions.append(menu[elem])

        for i, item in enumerate(items):
            function = functions[i]
            action = QAction(item, self)
            action.triggered.connect(function)
            self.menu.addAction(action)
        self.icon.setContextMenu(self.menu)
        self.icon.show()


    def close(self):
        print('1')

    # Метод для отображения изображения
    def image_display(self):
        if self.num == 1:
            self.num = 2
            self.start_image.emit(self.image)
        #
        # elif self.num == 2:
        #     self.num = 1
        #     self.start_image.emit(self.speak_gif)
        self.window.choi_timer = 0


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
            self.change_text.emit("Слушаю...")
            self.command = speech_manager.recognize()
            # DialogWindow.do_command(self.command)
            self.change_text.emit(self.command)
            self.voice_check = 0
        if self.ent_check:
            self.ent_check = False
            self.window.enterWindow.hide()



    # Открытие и закрытие поля вывода помощника
    def close_ob(self):
        if self.window:
            self.window.show()
            if self.quote == True:
                self.quote = False
                text = ""
                self.change_text.emit(text)
                self.window.quoteWindow.hide()
            else:
                self.quote = True
                self.window.quoteWindow.show()

    # Открытие и закрытие окна ввода
    def enter(self):
        if self.window:
            self.window.show()
            if self.voice_check == 1:
                self.voice_check = 0
            if self.ent_check == False:
                self.ent_check = True
                self.window.enterWindow.win2 = self.window.quoteWindow
                self.window.enterWindow.edit_line.setFocus()
                self.window.enterWindow.show()
                self.change_text.emit("Пишите...")


            else:
                self.ent_check = False
                self.window.enterWindow.hide()


    def settings(self):
        if self.win_check == True:
            self.win_check = False
            self.window.hide()
        self.settings_class.show()


    # # Закрытие
    # def close(self):
    #     if self.window:
    #         self.close()

    def say_command(self, say_comm):
        self.proc_comm.emit(say_comm)
        self.voice_check = 0

    def say_command(self, say_comm):
        self.proc_comm.emit(say_comm)
        self.voice_check = 0

    # Метод для получения времени для обращения к пользователю
    def change_window(self, window):
        self.window = window
        hour = datetime.datetime.now().hour
        if 0 <= hour < 5:
            self.change_text.emit(f"Доброй ночи, {self.config['User']['username']}")
        elif 5 <= hour < 12:
            self.change_text.emit(f"Доброе утро, {self.config['User']['username']}")
        elif 12 <= hour < 16:
            self.change_text.emit(f"Добрый день, {self.config['User']['username']}")
        elif 16 <= hour <= 23:
            self.change_text.emit(f"Добрый вечер, {self.config['User']['username']}")

        self.window.quoteWindow.show()
