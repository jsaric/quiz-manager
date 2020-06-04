import datetime
from collections import OrderedDict
from db.models import *


class BaseInputModel:
    def __init__(self, teams, league, round):
        self.teams = teams
        self.league = league
        self.round = round
        self.teams = sorted(teams, key=lambda x: x.name)
        self.team2result = OrderedDict()
        for t in self.teams:
            self.team2result[t] = Result(
                round=self.round,
                league=league,
                team=t,
                date=datetime.date.today(),
                round_one_score=0,
                playoff_result=None,
                final_round_score=0
            )

    def get_result(self, index):
        return self.team2result[self.teams[index]]

    def get_results(self):
        return [(t, self.team2result[t]) for t in self.teams]


