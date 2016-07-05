"""GUI widgets."""

import datetime

from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (
    QDialog, QItemSelectionModel, QLineEdit, QLabel, QMainWindow,
    QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout
)

from kisqpy.common import db, config
from kisqpy.models import Client, Ticket, Departure, Organisation


class DeleteDialog(QDialog):
    """Represents dialog for delete confirmation."""

    def __init__(self, what, from_what):
        QDialog.__init__(self)
        self.msg = "Delete {w} from {f} table?".format(w=what, f=from_what)
        # TODO: self.label = QLabel
        uic.loadUi(config.UI["delete_dialog"], self)
        self.label.setText(self.msg)


def required_field_empty_warning(parent, msg="One or more fields are empty."):
    """Warn user."""

    QMessageBox.warning(parent, "Error", msg)


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(config.UI["main"], self)

        self.action_exit.triggered.connect(self.close)
        self.pb_show_table.clicked.connect(self.show_table)

        self.rb_client.clicked.connect(self.rb_to_pb_client)
        self.rb_ticket.clicked.connect(self.rb_to_pb_ticket)
        self.rb_departure.clicked.connect(self.rb_to_pb_departure)
        self.rb_organisation.clicked.connect(self.rb_to_pb_organisation)

        self.pb_add_client.clicked.connect(self.add_client)
        self.pb_add_ticket.clicked.connect(self.add_ticket)
        self.pb_add_organisation.clicked.connect(self.add_organisation)

        self.pb_del_client.clicked.connect(self.del_client)
        self.pb_del_organisation.clicked.connect(self.del_organisation)
        self.pb_del_ticket.clicked.connect(self.del_ticket)

        self.pb_change_client.clicked.connect(self.change_client)
        self.pb_change_organisation.clicked.connect(self.change_organisation)
        self.pb_change_ticket.clicked.connect(self.change_ticket)

        self.tableWidget.cellClicked.connect(self.select_table_row)
        self.tableWidget.cellDoubleClicked.connect(self.open_ticket_info)

        self.show_table()

    @staticmethod
    def insert_objects(obj):
        """Insert object or objects to DB."""

        session = db.get_session()
        if isinstance(obj, (tuple, list)):
            session.add_all(obj)
        else:
            session.add(obj)
        session.commit()

    def show_table(self):
        def get_table_choise():
            choises = {
                self.rb_client: Client,
                self.rb_ticket: Ticket,
                self.rb_departure: Departure,
                self.rb_organisation: Organisation,
            }

            for rb, res in choises.items():
                if rb.isChecked():
                    return res

        def column_names(model):
            """Extract column names from table."""

            return model.__table__.columns.keys()

        session = db.get_session()
        model = get_table_choise()
        names = column_names(model)
        data = list(session.query(model))

        rows = len(data)
        columns = len(names)
        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.setHorizontalHeaderLabels(names)
        # self.tableWidget.sortByColumn(0, Qt.AscendingOrder)

        for i in range(rows):
            for j in range(columns):
                item = QTableWidgetItem(str(data[i].__dict__[names[j]]))
                self.tableWidget.setItem(i, j, item)

    def select_table_row(self, row, column):
        """Select current table row."""

        self.tableWidget.setCurrentIndex(
            (row, column), QItemSelectionModel.NoUpdate)

    def open_ticket_info(self, row, column):
        """Open current ticket info window."""

        raise Exception("double" + str((row, column)))

    def rb_to_pb_client(self):
        self.pb_show_table.setText("Show client table")

    def rb_to_pb_ticket(self):
        self.pb_show_table.setText("Show ticket table")

    def rb_to_pb_departure(self):
        self.pb_show_table.setText("Show departure table")

    def rb_to_pb_organisation(self):
        self.pb_show_table.setText("Show organisation table")

    def add_client(self):
        client = {
            "name": str(self.le_client_name.text()),
            "surname": str(self.le_client_surname.text()),
            "birthdate": datetime.date(2016, 6, 12),
            "city": str(self.le_client_city.text()),
            "street": str(self.le_client_street.text()),
            "phone": str(self.le_client_phone.text()),
        }

        if not all(client.values()):
            required_field_empty_warning(self)
        else:
            self.insert_objects(Client(**client))

    def add_ticket(self, client, place, organisation=None):
        """Insert new ticket to DB."""

        ticket = {
            "client": client,
            "place": place,
            "organisation": organisation,
            "order_date": datetime.date(2016, 6, 23),  # self.le_ticket_order_d
            "incoming_date": datetime.date(2016, 6, 25),
            "departure_date": datetime.date(2016, 6, 30),
            "table_num": 100,
            "cost": 17000
        }

        if not all(ticket.values()):
            required_field_empty_warning(self)
        else:
            self.insert_objects(Ticket(**ticket))

    def add_organisation(self):
        """Insert new organisation to DB."""

        name = str(self.le_organisation_name.text())
        if not name:
            required_field_empty_warning(self)
        else:
            org = Organisation(name=name)
            self.insert_objects(org)  # Organisation(name=name))

    def addProjectToDB(self):
        def parseDate(original):
            date = original[(original.index("(") + 1): original.index(")")]
            digits = [str(i) for i in range(10)]
            result = ""
            for char in date:
                if char == ",":
                    result += "-"
                elif char in digits:
                    result += char
                else:
                    pass

            return result

        class Project:
            pass

        Project.CreatorID = str(self.le_projectCreatorID.text())
        Project.ClientID = str(self.le_projectClientID.text())
        Project.OpenDate = parseDate(str(self.de_projectOpenDate.date()))
        Project.CloseDate = parseDate(str(self.de_projectCloseDate.date()))
        Project.Time = str(self.sb_projectTime.text())
        Project.CreationProg = str(self.cb_projectCreationProg.currentText())
        Project.RenderProg = str(self.cb_projectRenderProg.currentText())
        Project.SendForm = str(self.cb_projectSendForm.currentText())
        if (Project.CreatorID == "" or Project.ClientID == "" or Project.Time == ""):
            QMessageBox.warning(
                self,
                "Error",
                "One or more fields are empty!")
        else:
            query = """INSERT INTO project (creatorID, clientID, openDate, closeDate,
                                            time, creationProg, renderProg, sendForm)
                       VALUES ({creator}, {client}, {od}, {cd}, {t}, {cp}, {rp}, {sf});
                    """.format(creator=repr(Project.CreatorID),
                               client=repr(Project.ClientID),
                               od=repr(Project.OpenDate),
                               cd=repr(Project.CloseDate),
                               #without repr because in DB - int
                               t=Project.Time,
                               cp=repr(Project.CreationProg),
                               rp=repr(Project.RenderProg),
                               sf=repr(Project.SendForm))

            try:
                self.connectToDB("model", "most")
                cur = self.conn.cursor()
                cur.execute(query)
                self.conn.commit()
            except ps2.DatabaseError as e:
                if self.conn:
                    self.conn.rollback()
                    QMessageBox.warning(self, "Error", str(e))
            finally:
                self.disconnect()

    def abstractDel(
            self, table, object_id=None, surname=None, name=None):
        if surname is None and name is None and object_id:
            query = "DELETE FROM {t} WHERE id = {i}".format(t=table, i=object_id)
        elif surname and name and object_id is None:
            query = "DELETE FROM {t} WHERE surname = {s} AND name = {n}".format(
                t=table,
                s=repr(surname),
                n=repr(name))
        else:
            QMessageBox(self, "Error", "One field is empty")
            return

        try:
            self.connectToDB("model", "most")
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
        except ps2.DatabaseError as e:
            if self.conn:
                QMessageBox(self, "Error", str(e))
                self.conn.rollback()
        finally:
            self.disconnect()

    def delClient(self):
        # get info

        if self.rb_delClientByID.isChecked():
            clientID = str(self.le_delClientID.text())
            clientSurname = None
            clientName = None
        else:
            clientSurname = str(self.le_delClientSurname.text())
            clientName = str(self.le_delClientName.text())
            clientID = None

        # set parameters
        w = DeleteDialog("this record", "client")
        if w.exec_() == QDialog.Accepted:
            self.abstractDel("client", clientID, clientSurname, clientName)
            self.show_table()

    def del_client(self):
        """Delete client."""

        w = DeleteDialog("this record", "client")
        if w.exec_() == QDialog.Accepted:
            self.abstractDel("client", clientID, clientSurname, clientName)
            self.show_table()

    def del_organisation(self):
        """Delete organisation."""

        pass

    def del_ticket(self):
        """Delete ticket."""

        pass

    def abstractChange(self, table, field, target, ident):
        query = "UPDATE {T} SET {f} = {t} WHERE id = {i}".format(
            T=table,
            f=field,
            t=repr(target),
            i=ident)
        try:
            self.connectToDB("model", "most")
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
        except ps2.DatabaseError as e:
            QMessageBox.warning(self, "Error", str(e))
            if self.conn:
                self.conn.rollback()
        finally:
            self.conn.close

    def change_client(self):
        pass

    def change_organisation(self):
        pass

    def change_ticket(self):
        pass

    def changeClient(self):
        table = "client"
        ident = str(self.le_changeClientID.text())
        field = str(self.cb_changeClientField.currentItem())
        target = str(self.le_changeClientTarget.text())
        self.abstractChange(table, field, target, ident)
        self.rb_client.setEnabled(True)
        self.show_table()

    def changeCreator(self):
        table = "creator"
        ident = str(self.le_changeCreatorID.text())
        field = str(self.cb_changeCreatorField.currentText())
        target = str(self.le_changeCreatorTarget.text())
        self.abstractChange(table, field, target, ident)
        self.rb_creator.setEnabled(True)
        self.show_table()

    def changeProject(self):
        table = "project"
        ident = str(self.le_changeProjectID.text())
        field = str(self.cb_changeProjectField.currentText())
        target = str(self.le_changeProjectTarget.text())
        self.abstractChange(table, field, target, ident)
        self.rb_project.setEnabled(True)
        self.show_table()


def login(login):
    l = login()
    return l.exec_() == QDialog.Accepted


class LoginWindow(QDialog):
    """Login dialog window."""

    def __init__(self):
        QDialog.__init__(self)
        self.login = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.b_login = QPushButton("Login", self)
        self.b_login.clicked.connect(self.handle_login)
        layout = QVBoxLayout(self)
        layout.addWidget(self.login)
        layout.addWidget(self.password)
        layout.addWidget(self.b_login)

    def handle_login(self):
        """Login handler."""

        # TODO: get user from database
        if (
                self.login.text() == "admin" and
                self.password.text() == "admin"
        ):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Bad user or password")

    @staticmethod
    def do_login():
        return LoginWindow().exec_() == QDialog.Accepted
