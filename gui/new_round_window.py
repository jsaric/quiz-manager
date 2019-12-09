import typing

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from gui.custom_widgets import AddItemWidget
from models.league_results import LeagueResults
from db.models import *
from models.team_list import TeamList
import config


class NewRoundWindow(QMainWindow):
    def __init__(self, parent=None):
        super(NewRoundWindow, self).__init__(parent)
        self.resize(900, 600)
        self.setCentralWidget(TeamChooserWidget(self))
        self.setWindowTitle(config.TITLE)


class TeamChooserWidget(QWidget):
    def __init__(self, parent, league=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.list_view = QListView()
        self.league = league
        self.model = TeamList(league)
        self.list_view.setModel(self.model)
        self.list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.list_context_menu)
        self.layout.addWidget(self.list_view)
        self.team_add = AddItemWidget(self, "New Team Name: ", self.add_team, unavailable_options=list(map(lambda x: x.name, Team.get_all())))
        self.layout.addWidget(self.team_add)

        self.button_h_layout = QHBoxLayout()
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.on_cancel)
        self.button_next = QPushButton("Next")
        self.button_h_layout.addWidget(self.button_cancel)
        self.button_h_layout.addWidget(self.button_next)
        self.layout.addLayout(self.button_h_layout)
        self.setLayout(self.layout)
        self.new_teams = []

    def add_team(self, name):
        self.new_teams.append(name)
        team = Team.create(name=name)
        self.model.add_team(team)

    def list_context_menu(self, pos):
        self.listMenu = QMenu()
        current_index = self.list_view.currentIndex()
        select = self.listMenu.addAction("Select")
        select.triggered.connect(
            lambda: self.list_view.selectionModel().select(current_index, QtCore.QItemSelectionModel.Select)
        )

        deselect = self.listMenu.addAction("Deselect")
        deselect.triggered.connect(
            lambda: self.list_view.selectionModel().select(current_index, QtCore.QItemSelectionModel.Deselect)
        )
        delete = self.listMenu.addAction("Delete")
        delete.setDisabled(current_index.data() not in self.new_teams)
        delete.triggered.connect(lambda: self.model.delete_team(current_index.row()))

        parentPosition = self.list_view.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + pos)
        self.listMenu.show()

    def on_next(self):
        pass

    def on_cancel(self):
        self.model.delete_added_teams()
        self.parent().close()
