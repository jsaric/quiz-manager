from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from gui.widgets import MainWidget
from models.leagues_overview_model import LeaguesOverviewModel


class MainWindow(QMainWindow):
    # Constructor
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Quiz Manager")
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.main_widget = MainWidget(self, LeaguesOverviewModel())
        self.central_widget.addWidget(self.main_widget)
        self.resize(1024, 768)
