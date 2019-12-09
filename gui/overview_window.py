from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView
from models.league_results import LeagueResults


class LeagueOverviewWindow(QMainWindow):
    def __init__(self, league, parent=None):
        super(LeagueOverviewWindow, self).__init__(parent)
        self.resize(900, 600)
        self.table_view = QTableView()
        self.table_view.setModel(LeagueResults(league))
        self.setCentralWidget(self.table_view)
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSortingEnabled(True)

