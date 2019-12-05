from PyQt5 import QtWidgets
from PyQt5 import Qt, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QHeaderView, QDialog

from gui.overview_window import LeagueOverviewWindow
from config import *
from db.models import *


class DialogWithDisablingOptions(QDialog):
    def __init__(self, title, text, unavailable_options):
        super().__init__()
        self.unavailable_options = unavailable_options
        self.setWindowTitle(title)
        self.label = QtWidgets.QLabel(text
                                      )
        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.textChanged.connect(self.on_text_change)
        self.line_edit.setText("")
        self._available = False

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.on_save)
        self.button_box.rejected.connect(self.close)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_text_change(self):
        if self.line_edit.text().__str__() in self.unavailable_options or len(self.line_edit.text()) == 0:
            self.line_edit.setStyleSheet("border: 2px solid red")
            self._available = False
        else:
            self.line_edit.setStyleSheet("border: 2px solid green")
            self._available = True

    @pyqtSlot()
    def on_save(self):
        if self._available:
            self.ret_str = self.line_edit.text()
            self.accept()
        else:
            pass