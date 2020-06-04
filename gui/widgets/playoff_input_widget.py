from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QLineEdit, \
    QListView, QPushButton, QMenu
from PyQt5 import QtCore
import config


class PlayoffInputWidget(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.model.teams_split.connect(self.create_pair_widgets)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.label = QLabel(config.ROUND_STRINGS[1])
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.pairs_list = QListWidget(self)
        self.pairs_list.setStyleSheet("QListWidget::item { border-bottom: 0.5px solid }")
        self.pairs_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pairs_list.customContextMenuRequested.connect(self.list_context_menu)

        self.teams_left_list = QListView(self)
        self.teams_left_list.setModel(self.model.teams_left_model)
        self.teams_left_list.doubleClicked.connect(self.team_clicked)

        self.button = QPushButton("Finish Pairing")
        self.button.clicked.connect(self.finish_pairing)
        self.button.setDisabled(True)

        layout.addWidget(self.label)
        layout.addWidget(self.pairs_list)
        layout.addWidget(self.teams_left_list)
        layout.addWidget(self.button)
        self.playoff_assign_index = 0

    def create_pair_widgets(self):
        for ppm in self.model.pairs:
            pr_widget = PlayoffPairWidget(ppm)
            item = QListWidgetItem(self.pairs_list)
            item.setSizeHint(pr_widget.sizeHint())
            self.pairs_list.addItem(item)
            self.pairs_list.setItemWidget(item, pr_widget)

    def team_clicked(self, model_index: QtCore.QModelIndex):
        index = model_index.row()
        self.model.assign_team(index)
        if len(self.model.teams_left) == 0:
            self.button.setDisabled(False)

    def finish_pairing(self):
        self.layout().removeWidget(self.teams_left_list)
        self.teams_left_list.deleteLater()
        self.button.setText("Finish Playoff")
        self.button.clicked.disconnect(self.finish_pairing)
        self.button.clicked.connect(self.finish_playoff)

    def finish_playoff(self):
        self.model.finish()
        self.pairs_list.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.layout().removeWidget(self.button)
        self.button.deleteLater()

        self.finished_label = QLabel("Playoff Finished")
        self.finished_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout().addWidget(self.finished_label)
        self.parent().finish_playoff()

    def list_context_menu(self, pos):
        self.listMenu = QMenu()
        current_index = self.pairs_list.currentIndex()
        model = self.pairs_list.indexWidget(current_index).model
        name1, name2 = model.get_name(0), model.get_name(1)

        team_1_won = self.listMenu.addAction(f"{name1} Won")
        team_1_won.triggered.connect(
            lambda: model.set_draw_state(-1)
        )
        team_1_won.setDisabled(not model.is_draw())

        team_1_plus1 = self.listMenu.addAction(f"{name1} +1 ")
        team_1_plus1.triggered.connect(
            lambda: model.set_draw_state(-2)
        )
        team_1_plus1.setDisabled(not model.is_draw())

        draw = self.listMenu.addAction(f"Draw")
        draw.triggered.connect(
            lambda: model.set_draw_state(0)
        )
        draw.setDisabled(not model.is_draw())

        team_2_won = self.listMenu.addAction(f"{name2} Won")
        team_2_won.triggered.connect(
            lambda: model.set_draw_state(1)
        )
        team_2_won.setDisabled(not model.is_draw())

        team_2_plus1 = self.listMenu.addAction(f"{name2} +1 ")
        team_2_plus1.triggered.connect(
            lambda: model.set_draw_state(2)
        )
        team_2_plus1.setDisabled(not model.is_draw())

        parentPosition = self.pairs_list.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + pos)
        self.listMenu.show()


class PlayoffPairWidget(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.model_changed.connect(self.refresh)
        self.main_layout = QVBoxLayout()
        self.rows = []
        self.name_labels = []
        self.score_edits = []
        self.fscore_labels = []
        self._add_row()
        self._add_row()
        self.score_edits[0].textChanged.connect(partial(self._update_score, 0))
        self.score_edits[1].textChanged.connect(partial(self._update_score, 1))
        self.main_layout.addItem(self.rows[0])
        self.main_layout.addItem(self.rows[1])
        self.setLayout(self.main_layout)
        self.refresh()

    def _update_score(self, team_index):
        try:
            score = int(self.score_edits[team_index].text())
            self.model.set_score(team_index, score)
        except Exception:
            return

    def _add_row(self):
        layout = QHBoxLayout()
        l_name = QLabel()
        le_score = QLineEdit()
        le_score.setAlignment(QtCore.Qt.AlignCenter)
        l_fscore = QLabel()
        l_fscore.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(l_name)
        layout.addWidget(le_score)
        layout.addWidget(l_fscore)
        layout.setStretch(0, 10)
        layout.setStretch(1, 1)
        layout.setStretch(2, 1)
        self.rows.append(layout)
        self.name_labels.append(l_name)
        self.score_edits.append(le_score)
        self.fscore_labels.append(l_fscore)
        return layout, l_name, le_score, l_fscore

    def _pull_team_info(self, team_index):
        self.name_labels[team_index].setText(self.model.get_name(team_index))
        self.score_edits[team_index].setText(str(self.model.get_score(team_index)))
        self.fscore_labels[team_index].setText(str(self.model.get_final_score(team_index)))
        self.score_edits[team_index].setDisabled(self.model.finished)

    def refresh(self):
        self._pull_team_info(0)
        self._pull_team_info(1)