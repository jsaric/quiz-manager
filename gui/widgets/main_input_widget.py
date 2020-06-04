from PyQt5 import Qt
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtWidgets import *
from qtpy import QtCore

from gui.widgets import FirstRoundInputWidget, PlayoffInputWidget, FinalRoundInputWidget
from models.playoff_input_model import PlayoffInputModel
from models.first_round_input_model import FirstRoundModel
from models.final_round_input_model import FinalRoundModel
import config


class MainInputWidget(QWidget):
    def __init__(self, parent, base_model):
        super(MainInputWidget, self).__init__(parent)
        self.resize(1024, 768)
        self.base_model = base_model
        self.fr_model = QSortFilterProxyModel()
        self.fr_model.setSourceModel(FirstRoundModel(self.base_model))
        self.playoff_model = PlayoffInputModel(self.base_model)
        self.final_round_model = QSortFilterProxyModel()
        self.final_round_model.setSourceModel(FinalRoundModel(self.base_model))
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(FirstRoundInputWidget(self, self.fr_model))
        layout.addWidget(PlayoffInputWidget(self, self.playoff_model))
        layout.addWidget(FinalRoundInputWidget(self, self.final_round_model))
        self.setWindowTitle(config.TITLE)
        self.game_state = 0

    def finish_first_round(self):
        self.playoff_model.initiate_pairing()

    def finish_playoff(self):
        self.final_round_model.sort(1, QtCore.Qt.DescendingOrder)
        self.final_round_model.sourceModel().refresh()

    def finish(self):
        for t, r in self.base_model.get_results():
            r.save()