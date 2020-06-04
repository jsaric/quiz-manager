import os

dir_path = os.path.dirname(os.path.realpath(__file__))
DATABASE = dir_path + "/quiz_manager.db"

FIRST_PLACE_POINTS = 50
TITLE = "Quiz Manager"
ROUND_STRINGS = ["First Round", "Playoff", "Final Round"]