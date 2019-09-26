import sys

from PyQt5.QtCore import pyqtSlot, Qt

import pinglib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QPushButton, \
    QMessageBox, QCheckBox
import multiprocessing

address_pool = []


def build_db(ip_from, ip_to):

    ip_from = list(map(int, ip_from))
    ip_to = list(map(int, ip_to))
    while int(ip_from[3]) <= int(ip_to[3]):
        address_pool.append('{}.{}.{}.{}'.format(ip_from[0], ip_from[1], ip_from[2], ip_from[3]))
        ip_from[3] = int(ip_from[3] + 1)
    # Построение базы IP аддрессов

    pool = multiprocessing.Pool(100)
    result = pool.map(pinglib.output, address_pool)
    return result


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(648, 480)
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.from_ip_textbox = QLineEdit(self)
        self.to_ip_textbox = QLineEdit(self)
        self.table = QTableWidget(self)
        self.from_label = QLabel(self)
        self.to_label = QLabel(self)
        self.start_button = QPushButton('Start', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyPing")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.from_label.move(5, 5)
        self.from_ip_textbox.move(80, 10)
        self.from_ip_textbox.resize(100, 20)
        self.to_label.move(190, 5)
        self.to_ip_textbox.move(210, 10)
        self.to_ip_textbox.resize(100, 20)
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
        self.start_button.clicked.connect(self.start)
        self.show()


    def start(self):
        ip_from = self.from_ip_textbox.text().split('.')
        ip_to = self.to_ip_textbox.text().split('.')
        result = build_db(ip_from, ip_to)
        for i in range(len(result)):
            if result[i][1][0]:
                self.table.setItem(i, 0, QTableWidgetItem(result[i][0]))
                self.table.setItem(i, 1, QTableWidgetItem("Online"))
                self.table.setItem(i, 2, QTableWidgetItem(result[i][1][2]))
                self.table.setItem(i, 3, QTableWidgetItem(result[i][1][0]))
                self.table.setItem(i, 4, QTableWidgetItem(result[i][1][1]))
                self.table.setItem(i, 5, QTableWidgetItem("*nix"))
            else:
                self.table.setItem(i, 0, QTableWidgetItem(result[i][0]))
                self.table.setItem(i, 1, QTableWidgetItem("Offline"))
                self.table.setItem(i, 2, QTableWidgetItem(""))
                self.table.setItem(i, 3, QTableWidgetItem(""))
                self.table.setItem(i, 4, QTableWidgetItem(""))
                self.table.setItem(i, 5, QTableWidgetItem(""))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
