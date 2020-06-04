from PyQt5.QtCore import QAbstractItemModel, QStringListModel, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from db.models import *


class PlayoffInputModel(QAbstractItemModel):
    teams_split = pyqtSignal()

    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model
        self.pairs = []
        self.teams_left = []
        self.teams_left_model = QStandardItemModel()

    def initiate_pairing(self):
        results = sorted(self.base_model.get_results(), key=lambda x: x[1].round_one_score, reverse=True)
        for t, r in results[:len(results)//2]:
            pr = PlayoffResult.create(
                team1=t,
                team2=None,
                team1_score=0,
                team2_score=0,
                draw_score=0
            )
            pm = PlayoffPairModel(pr)
            r.playoff_result = pr
            self.pairs.append(pm)

        for t, r in results[len(results)//2:]:
            self.teams_left.append(t)
            self.teams_left_model.appendRow(QStandardItem(t.name))
        self.teams_split.emit()
        self.playoff_assign_index = 0

    def assign_team(self, index):
        team = self.teams_left[index]
        self.teams_left.remove(team)
        self.pairs[self.playoff_assign_index].set_opponent(team)
        self.base_model.team2result[team].playoff_result = self.pairs[self.playoff_assign_index].playoff_result
        self.teams_left_model.removeRow(index)
        self.playoff_assign_index += 1

    def finish(self):
        for p in self.pairs:
            p.finish()


class PlayoffPairModel(QAbstractItemModel):
    model_changed = pyqtSignal()

    def __init__(self, playoff_result: PlayoffResult):
        super().__init__()
        self.playoff_result = playoff_result
        self.finished = False

    def set_opponent(self, team):
        self.playoff_result.team2 = team
        self.model_changed.emit()

    def set_score(self, team_index, score):
        if team_index == 0:
            self.playoff_result.team1_score = score
        elif team_index == 1:
            if self.playoff_result.team2 is not None:
                self.playoff_result.team2_score = score
            else:
                raise Exception()
        self.model_changed.emit()

    def get_name(self, team_index):
        if team_index == 0:
            return self.playoff_result.team1.name
        elif team_index == 1:
            if self.playoff_result.team2 is not None:
                return self.playoff_result.team2.name
            else:
                return ""

    def get_score(self, team_index):
        if team_index == 0:
            return self.playoff_result.team1_score
        elif team_index == 1:
            if self.playoff_result.team2 is not None:
                return self.playoff_result.team2_score
            else:
                return 0

    def get_final_score(self, team_index):
        if team_index == 0:
            if self.playoff_result.team2 is not None:
                return self.playoff_result.total_points(self.playoff_result.team1)
            else:
                return self.get_score(0)
        elif team_index == 1:
            if self.playoff_result.team2 is not None:
                return self.playoff_result.total_points(self.playoff_result.team2)
            else:
                return 0

    def is_draw(self):
        return self.get_score(0) == self.get_score(1)

    def set_draw_state(self, state):
        self.playoff_result.draw_score = state
        self.model_changed.emit()

    def finish(self):
        self.finished = True
        self.model_changed.emit()
