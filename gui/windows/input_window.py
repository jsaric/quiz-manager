from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtWidgets import *
from gui.widgets import TeamChooserWidget, MainInputWidget
from models.base_input_model import *
import config


class InputWindow(QMainWindow):
    def __init__(self, parent, league):
        super(InputWindow, self).__init__(parent)
        self.league = League.get_by_name(league.name)
        if league.max_round is None:
            self.round = 1
        else:
            self.round = league.max_round + 1
        self.resize(1024, 768)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.team_chooser_widget = TeamChooserWidget(self, self.on_next, league=self.league)
        self.stack.addWidget(self.team_chooser_widget)
        self.setWindowTitle(config.TITLE)

    def on_next(self):
        teams = self.team_chooser_widget.get_selected_teams()
        base_model = BaseInputModel(teams, self.league, self.round)
        ir_widget = MainInputWidget(self, base_model)
        self.stack.addWidget(ir_widget)
        self.stack.setCurrentWidget(ir_widget)

    def closeEvent(self, a0):
        self.parent().refresh_leagues_overview()
        super(InputWindow, self).closeEvent(a0)
