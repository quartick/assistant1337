import sys
from configparser import ConfigParser
from unittest import runner

from PyQt5.QtWidgets import QApplication

from character_window import CustomWindow
from register_window import Stacked
from settings import Settings
from run import Runner


def main():
    config = ConfigParser()
    config.read("Data/Config.ini")
    if config["User"]["registered"] == "No":
        config["Exit"]["Answer_w1"] = "Yes"
        with open("Data/Config.ini", 'w') as configfile:
            config.write(configfile)
        app_1 = QApplication(sys.argv)
        w = Stacked(config)
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
        thread1 = Runner(config=config)
        thread1.start()
        window = CustomWindow(config, flow=thread1)
        thread1.change_text.connect(window.temp)
        window.show()
        thread1.change_window(window=window)
        thread1.tray_start()
        app_3.exec_()


if __name__ == "__main__":
    main()
