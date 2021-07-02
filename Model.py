from PyQt5.QtSql import *
from PyQt5.QtWidgets import QMessageBox, qApp

tableName = "trajectory"
dataBaseName = ":memory:"
driver = "QSQLITE"


def createConnection():
    db = QSqlDatabase.addDatabase(driver)
    db.setDatabaseName(dataBaseName)
    if not db.open():
        QMessageBox.critical(None, qApp.tr("Cannot open database"),
                             qApp.tr("Unable to establish a database connection.\n"
                                     "This example needs SQLite support. Please read "
                                     "the Qt SQL driver documentation for information "
                                     "how to build it.\n\n"
                                     "Click Cancel to exit."),
                             QMessageBox.Cancel)
        return False

    query = QSqlQuery()
    query.exec_("DROP TABLE " + tableName)
    query.exec_("CREATE TABLE " + tableName + "(Id integer PRIMARY KEY, X real, Y real, Z real)")
    query.exec_("INSERT INTO " + tableName + " VALUES(1, 1.0, 1.2, 1.3)")
    query.exec_("INSERT INTO " + tableName + " VALUES(2, 2.0, 1.3, 1.6)")
    query.exec_("INSERT INTO " + tableName + " VALUES(3, 2.0, 1.4, 1.9)")
    query.exec_("INSERT INTO " + tableName + " VALUES(4, 2.0, 1.5, 1.2)")
    query.exec_("INSERT INTO " + tableName + " VALUES(5, 3.0, 1.6, 1.4)")
    query.exec_("INSERT INTO " + tableName + " VALUES(6, 4.0, 1.7, 1.9)")


class Model(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTable(tableName)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.select()
