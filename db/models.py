from peewee import *
from config import *


__all__ = ["League", "Team", "Result", "PlayoffResult"]


database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class League(BaseModel):
    name = CharField(unique=True)

    @staticmethod
    def get_all():
        return League.select()

    @staticmethod
    def get_by_name(name):
        return League.select().where(League.name == name)[0]


class Team(BaseModel):
    name = CharField(unique=True)

    @staticmethod
    def get_all_from_league(league: League):
        return Team.select().join(Result).join(League).where(Result.league == league).distinct()

    @staticmethod
    def get_all():
        return Team.select()


class PlayoffResult(BaseModel):
    team1 = ForeignKeyField(Team)
    team2 = ForeignKeyField(Team)
    team1_score = IntegerField()
    team2_score = IntegerField()
    draw_score = IntegerField(null=True)

    def total_points(self, team: Team):
        is_team1 = team == self.team1
        score = self.team1_score if is_team1 else self.team2_score
        d_score = 0
        if self.team1_score == self.team2_score:
            if (self.draw_score == 0) or \
                    (self.draw_score == -1 and not is_team1) or \
                    (self.draw_score == 1 and is_team1) or \
                    (self.draw_score == -2 and not is_team1) or \
                    (self.draw_score == 2 and is_team1):
                d_score = 0
            elif (self.draw_score == -1 and is_team1) or \
                    (self.draw_score == 1 and not is_team1):
                d_score = score
            elif (self.draw_score == -2 and is_team1) or \
                    (self.draw_score == 2 and not is_team1):
                d_score = 1
        elif self.team1_score > self.team2_score:
            d_score = self.team2_score if is_team1 else 0
        elif self.team1_score < self.team2_score:
            d_score = self.team1_score if not is_team1 else 0
        return score + d_score


class Result(BaseModel):
    round = IntegerField()
    league = ForeignKeyField(League, backref='results')
    team = ForeignKeyField(Team, backref='results')
    date = DateField()
    round_one_score = IntegerField()
    playoff_result = ForeignKeyField(PlayoffResult)
    final_round_score = IntegerField()

    @staticmethod
    def get_all_from_league_and_round(league, round: int):
        return Result.select().join(Team, on=Result.team).switch(Result).join(League, on=Result.league).switch(Result).\
            join(PlayoffResult).where((Result.round == round)).where((League.name == league.name))

    @staticmethod
    def get_all_from_league(league):
        return Result.select().join(Team, on=Result.team).switch(Result).join(League, on=Result.league).switch(Result).\
            join(PlayoffResult).where(Result.league == league)

    @staticmethod
    def delete_all_from_league(league):
        Result.delete().where(Result.league == league).execute()

    def total_points(self):
        final_score = (self.round_one_score + self.playoff_result.total_points(self.team)) / 2. \
                      + self.final_round_score
        return final_score