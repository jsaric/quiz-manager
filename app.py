import IPython
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication, QTableView, QHeaderView
from peewee import *
from config import *
from db.models import  *
from gui.main_widget import MainWidget
from models.league_results import LeagueResults
from models.leagues_overview import LeaguesOverview

database = SqliteDatabase(DATABASE)


class MainWindow(QMainWindow):
    # Constructor
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.setFixedSize(*constants.SIZE)
        self.setWindowTitle("Quiz Manager")
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.main_widget = MainWidget(self, LeaguesOverview())
        self.central_widget.addWidget(self.main_widget)


if __name__ == "__main__":
    # IPython.embed()
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()