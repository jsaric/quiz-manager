from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView, QAbstractItemView, QHBoxLayout, QPushButton, QMenu
from qtpy import QtCore
from gui.widgets.custom_widgets import AddItemWidget
from models.team_list_model import TeamListModel, Team


class TeamChooserWidget(QWidget):
    def __init__(self, parent, on_next, league=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.list_view = QListView()
        self.league = league
        self.model = TeamListModel(league)
        self.list_view.setModel(self.model)
        self.list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.list_context_menu)
        self.layout.addWidget(self.list_view)
        self.team_add = AddItemWidget(self, "New Team Name: ", self.add_team, unavailable_options=self.model.all_team_names)
        self.layout.addWidget(self.team_add)

        self.button_h_layout = QHBoxLayout()
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.on_cancel)
        self.button_next = QPushButton("Next")
        self.button_next.clicked.connect(on_next)
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

    def on_cancel(self):
        self.model.delete_added_teams()
        self.window().close()

    def get_selected_teams(self):
        teams = []
        for i in self.list_view.selectedIndexes():
            teams.append(self.model.get_team(i.row()))
        return teams
