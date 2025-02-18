from PyQt5.QtWidgets import QApplication
from peewee import *
from config import *
from gui.windows import MainWindow

database = SqliteDatabase(DATABASE)

if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()