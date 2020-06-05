from PyQt5.QtCore import *
from db.models import *
import config


class LeagueResultsModel(QAbstractTableModel):
    def __init__(self, league: League):
        super().__init__()
        self.league = league
        self._init_data()
        self._init_headers()

    def _init_data(self):
        round = 1
        league_points = {}
        teams = set()
        while True:
            results = Result.get_all_from_league_and_round(self.league, round)
            if len(results) == 0:
                break
            league_points[round] = {}
            results = sorted(results, key=lambda x: (x.total_points(), x.round_one_score), reverse=True)
            for i, res in enumerate(results):
                league_points[round][res.team.name] = config.FIRST_PLACE_POINTS - i
                teams.add(res.team)
            round += 1

        self._league_points = league_points
        self._teams = teams
        self._rounds = round - 1
        self._team_scores = []
        for team in self._teams:
            scores = []
            for round in range(1, self._rounds + 1):
                scores.append(league_points[round].get(team.name, 0))
            self._team_scores.append((team.name, scores))
        self._team_scores = sorted(self._team_scores, key=lambda x: sum(x[1]), reverse=True)

    def _init_headers(self):
        headers = ["Team"]
        for i in range(1, self._rounds + 1):
            headers.append(f"R{i}")
        headers.append("Total")
        self._headers = headers

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._teams)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self._rounds + 2

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            r, c = index.row(), index.column()
            if c == 0:
                return self._team_scores[r][0]
            elif c == self._rounds + 1:
                return sum(self._team_scores[r][1])
            else:
                return self._team_scores[r][1][c-1]
        elif role == Qt.TextAlignmentRole:
            if index.column() >= 1:
                return Qt.AlignCenter

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self._headers[section]

    def sort(self, column: int, order: Qt.SortOrder = ...):
        ascending = order == Qt.AscendingOrder
        if column == 0:
            self._team_scores = sorted(self._team_scores, key=lambda x: x[0], reverse=ascending)
        elif column <= self._rounds:
            self._team_scores = sorted(self._team_scores, key=lambda x: x[1][column - 1], reverse=ascending)
        elif column == self._rounds + 1:
            self._team_scores = sorted(self._team_scores, key=lambda x: sum(x[1]), reverse=ascending)
        self.layoutChanged.emit()


