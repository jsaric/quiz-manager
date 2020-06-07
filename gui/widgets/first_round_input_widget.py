from PyQt5.QtWidgets import QWidget, QTableView, QHeaderView, QPushButton, QVBoxLayout, QLabel, QItemDelegate, QSpinBox
from qtpy import QtCore
from .custom_widgets import ZeroMaxIntDelegate

import config


class FirstRoundInputWidget(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.label = QLabel(config.ROUND_STRINGS[0])
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setItemDelegateForColumn(1, ZeroMaxIntDelegate(self, config.MAX_FIRST_ROUND))
        self.advance_button = QPushButton("Advance")
        self.advance_button.clicked.connect(self.on_advance)
        layout.addWidget(self.label)
        layout.addWidget(self.table_view)
        layout.addWidget(self.advance_button)

    def on_advance(self):
        self.model.sourceModel().finish()
        self.table_view.sortByColumn(1, QtCore.Qt.DescendingOrder)
        self.table_view.setSortingEnabled(False)
        self.layout().removeWidget(self.advance_button)
        self.advance_button.deleteLater()

        self.round_one_finished_label = QLabel("Round Finished")
        self.round_one_finished_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout().addWidget(self.round_one_finished_label)
        self.parent().finish_first_round()
