from PyQt5.QtWidgets import QWidget, QTableView, QHeaderView, QPushButton, QVBoxLayout, QLabel
from qtpy import QtCore

import config


class FinalRoundInputWidget(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.label = QLabel(config.ROUND_STRINGS[2])
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.finish_button = QPushButton("Finish")
        self.finish_button.clicked.connect(self.finish)
        layout.addWidget(self.label)
        layout.addWidget(self.table_view)
        layout.addWidget(self.finish_button)

    def finish(self):
        self.model.sourceModel().finish()
        self.table_view.sortByColumn(3, QtCore.Qt.DescendingOrder)
        self.table_view.setSortingEnabled(False)
        self.layout().removeWidget(self.finish_button)
        self.finish_button.deleteLater()

        self.round_one_finished_label = QLabel("Final Round Finished")
        self.round_one_finished_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout().addWidget(self.round_one_finished_label)
        self.parent().finish()
