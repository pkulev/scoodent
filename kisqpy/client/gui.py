"""GUI widgets."""

from datetime import date

from PyQt4 import uic
from PyQt4.QtCore import QDate
from PyQt4.QtGui import (
    QDialog, QItemSelectionModel, QLineEdit, QLabel, QMainWindow,
    QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout
)

from kisqpy.common import db, config
from kisqpy.models import Client, Ticket, Departure, Organisation


def from_datetime(date):
    """Return QDate object from datetime.date."""

    return QDate(date.year, date.month, date.day)


def to_datetime(qdate):
    """Return datetime.date object from QDate."""

    return date(day=qdate.day(), month=qdate.month(), year=qdate.year())

class DeleteDialog(QDialog):
    """Represents dialog for delete confirmation."""

    def __init__(self, what, from_what):
        QDialog.__init__(self)
        self.msg = "Delete {w} from {f} table?".format(w=what, f=from_what)
        uic.loadUi(config.UI["delete_dialog"], self)
        self.label.setText(self.msg)


def required_field_empty_warning(parent, msg="One or more fields are empty."):
    """Warn user."""

    QMessageBox.warning(parent, "Error", msg)


class TicketDialog(QDialog):
    """Implements ticket interaction."""

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["ticket_dialog"], self)

        self.ticket_id = model_id
        self.load_ticket_info()

    def load_ticket_info(self):
        """Get all needed info from DB."""

        session = db.get_session()
        ticket = session.query(Ticket).filter(
            Ticket.id == self.ticket_id
        ).first()

        self.lab_ticket_id.setText(str(ticket.id))
        self.lab_client.setText(str(ticket.client_id))  # replace by short info
        self.lab_organisation.setText(str(ticket.org_id))  # replace by name
        self.lab_place.setText(str(ticket.place_id))  # replace by info
        self.de_order_date.setDate(from_datetime(ticket.order_date))
        self.de_incoming_date.setDate(from_datetime(ticket.incoming_date))
        self.de_departure_date.setDate(from_datetime(ticket.departure_date))
        self.lab_table_num.setText(str(ticket.table_num))
        self.lab_cost.setText(str(ticket.cost))

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
            db.insert_objects(Ticket(**ticket))


class ClientDialog(QDialog):
    """Implements client interaction."""

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["client_dialog"], self)

        self.client_id = model_id
        self.pb_add_client.clicked.connect(self.add_client)

    def load_client_info(self):
        """Get all needed info from DB."""

        session.db.get_session()
        client = session.query(Client).filter(
            Client.id == self.client_id
        ).first()

       # self.lab_

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
            db.insert_objects(Client(**client))


class OrganisationDialog(QDialog):

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["organisation_dialog"], self)

        self.organisation_id = model_id
        self.pb_add_organisation.clicked.connect(self.add_organisation)

    def load_organisation_info(self):
        pass

    def add_organisation(self):
        """Insert new organisation to DB."""

        name = str(self.le_organisation_name.text())
        if not name:
            required_field_empty_warning(self)
        else:
            db.insert_objects(Organisation(name=name))


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(config.UI["main"], self)

        self.model = Ticket

        self.action_exit.triggered.connect(self.close)

        # TODO
        self.pb_add_client.clicked.connect(lambda: ClientDialog(1).exec_())
        self.pb_add_ticket.clicked.connect(lambda: TicketDialog(1).exec_())

        self.rb_client.clicked.connect(lambda: self.show_table(Client))
        self.rb_ticket.clicked.connect(lambda: self.show_table(Ticket))
        self.rb_departure.clicked.connect(lambda: self.show_table(Departure))
        self.rb_organisation.clicked.connect(lambda: self.show_table(Organisation))

        # TODO
        self.table_widget.cellClicked.connect(self.select_table_row)
        self.table_widget.cellDoubleClicked.connect(self.open_table_info)
        # TODO: get current selection or QMessageBox.error/ignore
        self.pb_view_and_modify.clicked.connect(self.open_table_info)

        self.show_table(self.model)

    def show_table(self, model):
        """Show all entries of model in table."""

        self.model = model
        session = db.get_session()
        names = model.__table__.columns.keys()
        data = list(session.query(model))

        rows = len(data)
        cols = len(names)
        self.table_widget.clear()
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(cols)
        self.table_widget.setHorizontalHeaderLabels(names)
        # self.table_widget.sortByColumn(0, Qt.AscendingOrder)

        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem(str(data[row].__dict__[names[col]]))
                self.table_widget.setItem(row, col, item)


    def select_table_row(self, row, column):
        """Select current table row."""

        # self.table_widget.setCurrentIndex(
        #     (row, column), QItemSelectionModel.NoUpdate)

    def open_table_info(self, row, column):
        """Open current table info window."""

        model_dialog_map = {
            Client: ClientDialog,
            Ticket: TicketDialog,
            Organisation: OrganisationDialog,
        }

        dialog = model_dialog_map.get(self.model)
        model_id = int(self.table_widget.item(row, 0).text())
        dialog(model_id=model_id).exec_()

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
