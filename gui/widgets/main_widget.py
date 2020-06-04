from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QHeaderView
from db.models import *
from gui.widgets.custom_widgets import DialogWithDisablingOptions


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout(self)

        self.league_list = QtWidgets.QTableView(self)
        self.league_list.setModel(model)
        self.league_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.league_list.clearSelection()
        self.league_list.resizeColumnsToContents()
        self.league_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.league_list, 2)

        self.button_layout = QtWidgets.QVBoxLayout(self)

        self.new_league_button = QtWidgets.QPushButton("New league", self)
        self.button_layout.addWidget(self.new_league_button)
        self.new_league_button.clicked.connect(self.on_new_league)

        self.new_round_button = QtWidgets.QPushButton("New round", self)
        self.button_layout.addWidget(self.new_round_button)
        self.new_round_button.clicked.connect(self.on_new_round)

        self.del_button = QtWidgets.QPushButton("Delete league", self)
        self.button_layout.addWidget(self.del_button)
        self.del_button.clicked.connect(self.on_delete)

        self.results_overview_button = QtWidgets.QPushButton("Results overview", self)
        self.button_layout.addWidget(self.results_overview_button)
        self.results_overview_button.clicked.connect(self.on_load)

        self.quit_button = QtWidgets.QPushButton("Quit", self)
        self.button_layout.addWidget(self.quit_button)
        self.quit_button.clicked.connect(self.on_quit)

        self.button_layout.addStretch()
        self.jsolutions_label = QtWidgets.QLabel("JSolutions")
        self.jsolutions_label.setAlignment(QtCore.Qt.AlignCenter)
        self.button_layout.addWidget(self.jsolutions_label)
        self.button_layout.setAlignment(QtCore.Qt.AlignTop)
        self.button_layout.setAlignment(self.jsolutions_label, QtCore.Qt.AlignBottom)

        self.layout.addLayout(self.button_layout, 1)
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
            QtWidgets.QMessageBox.warning(self, "Zero rounds error", "Zero rounds have been played in this league. "
                                                                     "Unable to show the results overview.")
        else:
            from gui.windows import LeagueOverviewWindow
            win = LeagueOverviewWindow(league, parent=self)
            win.show()

    @pyqtSlot()
    def on_delete(self):
        league = self.get_selected_league()
        if league is None:
            return
        league = League.get_by_name(league.name)
        reply = QtWidgets.QMessageBox.question(self, "Message", f"Are you sure you want to delete {league.name} league?",
                                                      QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            Result.delete_all_from_league(league)
            league.delete_instance()
            self.league_list.model().refresh()
        else:
            return

    @pyqtSlot()
    def on_new_league(self):
        league_names = list(map(lambda x: x.name, League.get_all()))
        dialog = DialogWithDisablingOptions("New league", "Please enter valid league name:", league_names)
        if dialog.exec_():
            league = League.create(name=dialog.ret_str)
            league.save()
            self.league_list.model().refresh()

    @pyqtSlot()
    def on_new_round(self):
        league = self.get_selected_league()
        if league is None:
            return
        from gui.windows import InputWindow
        new_round_win = InputWindow(self, league)
        new_round_win.show()

    def refresh_leagues_overview(self):
        self.league_list.model().refresh()
