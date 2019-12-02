from PyQt5 import QtWidgets
from PyQt5 import Qt, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QHeaderView

from gui.overview_window import LeagueOverviewWindow
from config import *
from db.models import *


class StartWidget(QtWidgets.QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout(self)

        self.league_list = QtWidgets.QTableView(self)
        self.league_list.setModel(model)
        self.league_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.league_list.clearSelection()
        self.league_list.resizeColumnsToContents()
        self.league_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.league_list)

        self.button_layout = QtWidgets.QVBoxLayout(self)

        self.new_button = QtWidgets.QPushButton("New league", self)
        self.button_layout.addWidget(self.new_button)

        self.del_button = QtWidgets.QPushButton("Delete league", self)
        self.button_layout.addWidget(self.del_button)
        self.del_button.clicked.connect(self.on_delete)

        self.load_button = QtWidgets.QPushButton("Load league", self)
        self.button_layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.on_load)

        self.quit_button = QtWidgets.QPushButton("Quit", self)
        self.button_layout.addWidget(self.quit_button)
        self.quit_button.clicked.connect(self.on_quit)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def get_selected_league(self):
        selected_indexes = self.league_list.selectedIndexes()
        if len(selected_indexes) != 2 or (selected_indexes[0].row() != selected_indexes[1].row()):
            return None
        else:
            return self.league_list.model().get_league(selected_indexes[0])

    @pyqtSlot()
    def on_quit(self):
        QtCore.QCoreApplication.instance().quit()

    @pyqtSlot()
    def on_load(self):
        league = self.get_selected_league()
        if league is None:
            return
        if league.max_round == 0 or league.max_round is None:
            print("Error")
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Zero rounds have been played in this league.')
            error_dialog.exec_()
        else:
            win = LeagueOverviewWindow(league, parent=self)
            win.show()

    @pyqtSlot()
    def on_delete(self):
        league = self.get_selected_league()
        league = League.get_by_name(league.name)
        if league is None:
            return
        reply = QtWidgets.QMessageBox.question(self, "Message", f"Are you sure you want to delete {league.name} league?",
                                                      QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            Result.delete_all_from_league(league)
            league.delete_instance()
            self.league_list.model().refresh()
            self.league_list.update()
        else:
            return