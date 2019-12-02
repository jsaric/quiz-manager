from db.models import *
from peewee import *
from config import *
import datetime
import random
import IPython


if __name__ == '__main__':
    database = SqliteDatabase(DATABASE)

    with database:
        database.drop_tables([League, Team, Result, PlayoffResult])
        database.create_tables([League, Team, Result, PlayoffResult])

    zabac_wed_league = League.create(name="Zabac-Wed")
    zabac_wed_league.save()
    zabac_mon_league = League.create(name="Zabac-Mon")
    zabac_mon_league.save()
    team_names = ["Prasožder United", "Kongo XXL", "DanceNet-121", "Padobranci"]
    teams = []
    for name in team_names:
        team = Team.create(name=name)
        team.save()
        teams.append(team)

    # First Round
    playoff_1_1 = PlayoffResult.create(
        team1=teams[0],
        team2=teams[1],
        team1_score=4,
        team2_score=3,
        draw_score=None
    )
    playoff_1_1.save()
    playoff_1_2 = PlayoffResult.create(
        team1=teams[2],
        team2=teams[3],
        team1_score=4,
        team2_score=3,
        draw_score=None
    )
    playoff_1_2.save()

    for team, playoff_result in zip(teams, [playoff_1_1, playoff_1_1, playoff_1_2, playoff_1_2]):
        result = Result.create(
            round=1,
            league=zabac_wed_league,
            team=team,
            date=datetime.date.today(),
            round_one_score=random.randint(0, 37),
            playoff_result=playoff_result,
            final_round_score=random.randint(0, 18)
        )
        result.save()

    # Second Round
    playoff_2_1 = PlayoffResult.create(
        team1=teams[0],
        team2=teams[2],
        team1_score=4,
        team2_score=5,
        draw_score=None
    )
    playoff_2_1.save()
    playoff_2_2 = PlayoffResult.create(
        team1=teams[1],
        team2=teams[3],
        team1_score=4,
        team2_score=4,
        draw_score=-2
    )
    playoff_2_2.save()

    for team, playoff_result in zip(teams, [playoff_2_1, playoff_2_2, playoff_2_1, playoff_2_2]):
        result = Result.create(
            round=2,
            league=zabac_wed_league,
            team=team,
            date=datetime.date.today(),
            round_one_score=random.randint(0, 37),
            playoff_result=playoff_result,
            final_round_score=random.randint(0, 18)
        )
        result.save()