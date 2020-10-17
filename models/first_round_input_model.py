from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt, QAbstractItemModel, pyqtSignal


class FirstRoundModel(QAbstractTableModel):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model
        self.finished = False
        self._init_headers()

    def _init_headers(self):
        headers = ["Team", "Points"]
        self._headers = headers

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.base_model.teams)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._headers)

    def headerData(self, section: int, orientation, role: int = ...):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return self._headers[section]
        else:
            return range(1, len(self.base_model.teams) + 1)

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            if index.column() == 1:
                return self.base_model.get_result(index.row()).round_one_score
            elif index.column() == 0:
                return self.base_model.teams[index.row()].name
            else:
                return QVariant()
        elif role == Qt.TextAlignmentRole:
            if index.column() == 1:
                return Qt.AlignCenter
        else:
            return QVariant()

    def setData(self, index: QModelIndex, value, role: int = ...) -> bool:
        try:
            self.base_model.get_result(index.row()).round_one_score = int(value)
            return True
        except ValueError:
            return False

    def finish(self):
        self.finished = True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.column() == 1:
            if self.finished:
                return Qt.ItemIsEnabled
            else:
                return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled
