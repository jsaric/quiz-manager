import typing

from PyQt5.QtCore import *
from db.models import *
from peewee import *
import config


class TeamList(QAbstractListModel):
    def __init__(self, league=None):
        super().__init__()
        self.league = league
        self._load_data()
        self._init_headers()
        self._added_teams = []

    def _load_data(self):
        if self.league is None:
            query = Team.get_all()
        else:
            query = Team.get_all_from_league(self.league)
        self._teams = list(query)

    def _init_headers(self):
        headers = ["Teams"]
        self._headers = headers

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._teams)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self._headers[section]

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self._teams[index.row()].name
        else:
            return QVariant()

    def refresh(self):
        self._load_data()
        self._init_headers()
        self.layoutChanged.emit()

    def add_team(self, team):
        self._teams.append(team)
        self._added_teams.append(team)
        self.layoutChanged.emit()

    def delete_team(self, index):
        team = self._teams.pop(index)
        team.delete_instance()
        self.layoutChanged.emit()

    def delete_added_teams(self):
        for t in self._added_teams:
            t.delete_instance()