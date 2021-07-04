from PyQt5.QtCore import QObject
from PyQt5.QtSql import *
from PyQt5.QtWidgets import QMessageBox, qApp

testData = [[155493.83000, 139550.56000, 55.430000000],
            [155493.83000, 139550.56000, 45.430000000],
            [153.43494879, 0.0640584421, 0.1921753287],
            [155493.84000, 139550.54000, 35.430000000],
            [155493.81000, 139550.52000, 25.430000000],
            [155493.79000, 139550.56000, 15.430000000],
            [155493.85000, 139550.59000, 5.4300000000]]


class Model(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tableName = "trajectory"
        self.dataBaseName = ":memory:"
        self.connectionName = "TRAJECTORY"
        self.driver = "QSQLITE"

        self.createConnection()
        self.loadData(testData)

        self.tableModel = QSqlTableModel(self, QSqlDatabase.database(self.connectionName))
        self.tableModel.setTable(self.tableName)
        self.tableModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.tableModel.submitAll()
        self.tableModel.select()

    def createConnection(self):
        dataBase = QSqlDatabase.addDatabase(self.driver, self.connectionName)
        dataBase.setDatabaseName(self.dataBaseName)
        if not dataBase.open():
            QMessageBox.critical(None, qApp.tr("Cannot open database"),
                                 qApp.tr("Unable to establish a database connection.\n"
                                         "This example needs SQLite support. Please read "
                                         "the Qt SQL driver documentation for information "
                                         "how to build it.\n\n"
                                         "Click Cancel to exit."),
                                 QMessageBox.Cancel)
            return False

    def loadData(self, data):
        dataBase = QSqlDatabase.database(self.connectionName)

        dataBase.exec("DROP TABLE IF EXISTS " + self.tableName)
        dataBase.exec("CREATE TABLE " + self.tableName + "(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, X REAL, "
                                                         "Y REAL, Z REAL)")

        insertDataQuery = QSqlQuery(dataBase)
        insertDataQuery.prepare(f"INSERT INTO {self.tableName} (X, Y, Z) "
                                f"VALUES (:X, :Y, :Z)")

        for X, Y, Z in data:
            insertDataQuery.bindValue(":X", X)
            insertDataQuery.bindValue(":Y", Y)
            insertDataQuery.bindValue(":Z", Z)
            if not insertDataQuery.execBatch():
                QMessageBox.warning(None, "Database Error",
                                    insertDataQuery.lastError().text())
            dataBase.commit()
        insertDataQuery.finish()

    @property
    def TableModel(self):
        return self.tableModel
