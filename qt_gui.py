import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(648, 480)
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.from_diapason = QLineEdit(self)
        self.to_diapason = QLineEdit(self)
        self.table = QTableWidget(self)
        self.from_label = QLabel(self)
        self.to_label = QLabel(self)
        self.start_button = QPushButton('Start', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyPing")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.from_label.move(5, 5)
        self.from_diapason.move(80, 10)
        self.from_diapason.resize(100, 20)
        self.to_label.move(190, 5)
        self.to_diapason.move(210, 10)
        self.to_diapason.resize(100, 20)
        self.table.move(0, 40)
        self.table.resize(648, 420)
        self.start_button.move(430, 5)

        self.table.setColumnCount(6)
        self.table.setRowCount(256)
        self.from_label.setText('IP range from')
        self.to_label.setText('to')
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(
            ["IP address", "Status", "Hostname", "Ping, ms", "TTL", "OS type"])

        self.table.setItem(0, 0, QTableWidgetItem("192.168.1.1"))
        self.table.setItem(0, 1, QTableWidgetItem("Online"))
        self.table.setItem(0, 2, QTableWidgetItem("openwrt.lan"))
        self.table.setItem(0, 3, QTableWidgetItem("64"))
        self.table.setItem(0, 4, QTableWidgetItem("2"))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
