import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class coffeeInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('coffee')
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.fill_table()

    def fill_table(self):
        result = self.cur.execute("""SELECT ID, name, degree, type, 
                                            description, price, volume from coffee
                                            """).fetchall()
        self.table.setRowCount(len(result))
        if result:
            self.table.setColumnCount(len(result[0]))
            self.table.setHorizontalHeaderLabels(
                ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                 'описание вкуса', 'цена', 'объем упоковки'])
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))


class ChangeForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('addEditCoffee')
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.fill_editor()
        self.buttCreate.clicked.connect(self.create_new)
        self.buttSave.clicked.connect(self.save_date)

    def fill_editor(self):
        result = self.cur.execute("""SELECT ID, name, degree, type, 
                                            description, price, volume from coffee
                                            """).fetchall()
        self.editTable.setRowCount(len(result))
        if result:
            self.editTable.setColumnCount(len(result[0]))
            self.editTable.setHorizontalHeaderLabels(
                ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                 'описание вкуса', 'цена', 'объем упоковки'])
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.editTable.setItem(i, j, QTableWidgetItem(str(val)))

    def create_new(self):
        result = self.cur.execute("""SELECT ID, name, degree, type, 
                                            description, price, volume from coffee
                                            """).fetchall()
        self.editTable.setRowCount(len(result) + 1)
        if result:
            self.editTable.setColumnCount(len(result[0]))
            self.editTable.setHorizontalHeaderLabels(
                ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                 'описание вкуса', 'цена', 'объем упоковки'])
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.editTable.setItem(i, j, QTableWidgetItem(str(val)))
            for j in range(7):
                self.editTable.setItem(len(result), j, QTableWidgetItem(''))

    def save_date(self):
        for i in range(self.editTable.rowCount()):
            columns = self.editTable.columnCount()
            column = [self.editTable.item(i, col).text() for col in range(columns)]
            try:
                if column[0] == '':
                    self.cur.execute("""INSERT into coffee(name, degree, type, 
                                            description, price, volume) VALUES(?, ?, ?, ?, ?, ?)""",
                                     (column[1], column[2], column[3], column[4], column[5],
                                      column[6],))
                    self.con.commit()
                    widget.fill_table()
                else:
                    self.cur.execute("""UPDATE coffee 
                                     SET name=?, degree=?, type=?, description=?, price=?, 
                                     volume=?
                                    WHERE id=?""",
                                     (column[1], column[2], column[3], column[4], column[5],
                                      column[6], column[0],))
                    self.con.commit()
                    widget.fill_table()
            except:
                continue


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = coffeeInfo()
    widget.show()
    widget2 = ChangeForm()
    widget2.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
