import typing

from PyQt5.QtCore import *
from db.models import *
from peewee import *
import config


class LeaguesOverview(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._load_data()
        self._init_headers()

    def _load_data(self):
        query = (League.select(League.name, fn.MAX(Result.round).alias("max_round"))
            .join(Result, JOIN.LEFT_OUTER).group_by(League.name))
        self._leagues = list(query)

    def _init_headers(self):
        headers = ["League Name", "Rounds Played"]
        self._headers = headers

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._leagues)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self._headers[section]

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            if index.column() == 1:
                round = self._leagues[index.row()].max_round
                if round is None:
                    round = 0
                return round
            elif index.column() == 0:
                return self._leagues[index.row()].name
            else:
                return QVariant()
        else:
            return QVariant()

    def get_league(self, index):
        return self._leagues[index.row()]

    def refresh(self):
        self._load_data()
        self._init_headers()
        self.layoutChanged.emit()

