import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(640, 480)
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
        self.stop_button = QPushButton('Stop', self)
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
        self.table.resize(640, 420)
        self.start_button.move(535, 5)
        self.stop_button.move(430, 5)

        self.table.setColumnCount(17)
        self.table.setRowCount(256)
        self.from_label.setText('IP range from')
        self.to_label.setText('to')
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(
            ["IP address", "Status","Hostname", "Ping, ms", "TTL", "FTP/20", "FTP/21", "SSH", "SMTP", "DNS", "DHCP/67", "DHCP/68",
             "HTTP", "POP3", "IMAP", "HTTPS", "RDP"])

        self.table.setItem(0, 0, QTableWidgetItem("192.168.1.1"))
        self.table.setItem(0, 1, QTableWidgetItem("Online"))
        self.table.setItem(0, 2, QTableWidgetItem("openwrt.lan"))
        self.table.setItem(0, 3, QTableWidgetItem("64"))
        self.table.setItem(0, 4, QTableWidgetItem("2"))
        self.table.setItem(0, 5, QTableWidgetItem("True"))
        self.table.setItem(0, 6, QTableWidgetItem("True"))
        self.table.setItem(0, 7, QTableWidgetItem("True"))
        self.table.setItem(0, 8, QTableWidgetItem("True"))
        self.table.setItem(0, 9, QTableWidgetItem("True"))
        self.table.setItem(0, 10, QTableWidgetItem("True"))
        self.table.setItem(0, 11, QTableWidgetItem("True"))
        self.table.setItem(0, 12, QTableWidgetItem("True"))
        self.table.setItem(0, 13, QTableWidgetItem("True"))
        self.table.setItem(0, 14, QTableWidgetItem("True"))
        self.table.setItem(0, 15, QTableWidgetItem("True"))
        self.table.setItem(0, 16, QTableWidgetItem("True"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
