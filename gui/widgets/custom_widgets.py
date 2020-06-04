from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

__all__ = ["DialogWithDisablingOptions", "AddItemWidget", ]


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


class AddItemWidget(QWidget):
    def __init__(self, parent, label, on_add, unavailable_options=[]):
        super().__init__(parent)
        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.edit = QLineEdit()
        self.edit.textChanged.connect(self.on_text_change)
        self.edit.installEventFilter(self)
        self.layout.addWidget(self.edit)

        self.button = QPushButton("Add")
        self.layout.addWidget(self.button)
        self.on_add = on_add
        self.button.clicked.connect(self.on_click)

        self.unavailable_options = unavailable_options
        self.setLayout(self.layout)

    def on_click(self):
        if self._available:
            self.on_add(self.edit.text())
            self.edit.clear()

    def eventFilter(self, widget, event):
        if (event.type() == QtCore.QEvent.KeyPress and
                widget is self.edit):
            key = event.key()
            if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                self.button.clicked.emit()
                return True
        return QWidget.eventFilter(self, widget, event)

    @pyqtSlot()
    def on_text_change(self):
        if self.edit.text().__str__() in self.unavailable_options or len(self.edit.text()) == 0:
            self.edit.setStyleSheet("border: 1.5px solid red")
            self._available = False
        else:
            self.edit.setStyleSheet("border: 1.5px solid green")
            self._available = True
