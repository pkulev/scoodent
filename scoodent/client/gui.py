"""GUI widgets."""

from datetime import date

from PyQt4 import uic
from PyQt4.QtCore import QDate
from PyQt4.QtGui import (
    QDialog, QItemSelectionModel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout
)

from scoodent.common import db, config
from scoodent.models import Student, Report, Discipline, StudentGroup


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


class sdsdialog(QDialog):
    """Implements ticket interaction."""

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["student_dialog"], self)

        self.ticket_id = model_id
        self.load_student_info()

    def load_student_info(self):
        """Get all needed info from DB."""

        session = db.get_session()
        student = session.query(Student).filter(
            Student.id == self.student_id
        ).first()

        self.lab_student_id.setText(str(ticket.id))
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
            "order_date": date(2016, 6, 23),  # self.le_ticket_order_d
            "incoming_date": date(2016, 6, 25),
            "departure_date": date(2016, 6, 30),
            "table_num": 100,
            "cost": 17000
        }

        if not all(ticket.values()):
            required_field_empty_warning(self)
        else:
            db.insert_objects(Ticket(**ticket))


class StudentDialog(QDialog):
    """Implements student interaction."""

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["student_dialog"], self)

        self.student_id = model_id
        self.pb_add_student.clicked.connect(self.add_student)

        self.load_student_info()

    def load_student_info(self):
        """Get all needed info from DB."""

        session = db.get_session()
        student = session.query(Student).filter(
            Student.id == self.student_id
        ).first()

        self.le_name.setText(student.name)
        self.le_surname.setText(student.surname)
        self.de_birthdate.setDate(from_datetime(student.birthdate))
        self.le_address.setText(student.address)
        self.le_phone.setText(student.phone)
        self.le_parents_phone.setText(student.parents_phone)
        self.le_school.setText(student.school)
        self.de_enter_date.setDate(from_datetime(student.enter_date))

    def add_student(self):
        student = {
            "name": str(self.le_name.text()),
            "surname": str(self.le_surname.text()),
            "birthdate": to_datetime(self.de_birthdate.date()),
            "address": str(self.le_address.text()),
            "phone": str(self.le_phone.text()),
            "parents_phone": str(self.le_parents_phone.text()),
            "school": str(self.le_school.text()),
            "enter_date": to_datetime(self.de_enter_date.date()),
        }

        if not all(student.values()):
            required_field_empty_warning(self)
        else:
            db.insert_objects(Student(**student))


class ReportDialog(QDialog):
    """Implements reports interaction."""

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["report_dialog"], self)

        self.report_id = model_id
        self.pb_add_report.clicked.connect(self.add_report)

        self.load_report_info()

    def load_report_info(self):
        """Get all needed info from DB."""

        session = db.get_session()
        report = session.query(Report).filter(
            Report.id == self.report_id
        ).first()

        self.lab_report_id.setText(str(report.id))
        self.lab_mark.setText(str(report.mark))
        self.de_mark_date.setDate(from_datetime(report.mark_date))
        self.lab_report_type.setText(report.report_type)
        self.lab_discipline_id.setText(str(report.discipline_id))
        self.lab_discipline_name.setText(report.discipline.name)
        self.lab_student.setText(str(report.student.id))

    def add_report(self):
        """Add report to DB."""

        session = db.get_session()
        report = {
            "mark": int(self.lab_mark.text()),
            "mark_date": to_datetime(self.de_mark_date.date()),
            "report_type": str(self.lab_report_type.text()),
            "discipline": session.query(Discipline).filter(
                Discipline.id == int(self.lab_discipline_id.text())),
            "student": session.query(Student).filter(
                Student.id == int(self.lab_student.text()))
        }

        if not all(report.values()):
            required_field_empty_warning(self)
        else:
            db.insert_objects(Report(**report))


class DisciplineDialog(QDialog):

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["discipline_dialog"], self)

        self.discipline_id = model_id
        self.pb_add_discipline.clicked.connect(self.add_discipline)

        self.load_discipline_info()

    def load_discipline_info(self):
        session = db.get_session()
        discipline = session.query(Discipline).filter(
            Discipline.id == self.discipline_id
        ).first()

        self.le_name.setText(discipline.name)

    def add_discipline(self):
        """Insert new discipline to DB."""

        name = str(self.le_discipline_name.text())
        if not name:
            required_field_empty_warning(self)
        else:
            db.insert_objects(Discipline(name=name))


class StudentGroupDialog(QDialog):

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["group_dialog"], self)

        self.group_id = model_id
        self.pb_add_group.clicked.connect(self.add_group)

        self.load_group_info()

    def load_group_info(self):
        session = db.get_session()
        group = session.query(StudentGroup).filter(
            StudentGroup.id == self.group_id
        ).first()

        self.le_name.setText(group.name)
        self.ch_fulltime.setChecked(group.fulltime)

    def add_group(self):
        """Insert new group to DB."""

        name = str(self.le_name.text())
        fulltime = bool(self.ch_fulltime.checked())
        if not name:
            required_field_empty_warning(self)
        else:
            db.insert_objects(Discipline(name=name, fulltime=fulltime))


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(config.UI["main"], self)

        self.model = Student

        self.action_exit.triggered.connect(self.close)

        # TODO
        self.pb_add_student.clicked.connect(lambda: StudentDialog(1).exec_())
        self.pb_add_report.clicked.connect(lambda: ReportDialog(1).exec_())
        self.pb_add_discipline.clicked.connect(
            lambda: DisciplineDialog(1).exec_())

        self.rb_student.clicked.connect(lambda: self.show_table(Student))
        self.rb_report.clicked.connect(lambda: self.show_table(Report))
        self.rb_discipline.clicked.connect(lambda: self.show_table(Discipline))
        self.rb_group.clicked.connect(lambda: self.show_table(StudentGroup))

        # TODO
        self.table_widget.cellClicked.connect(self.select_table_row)
        self.table_widget.cellDoubleClicked.connect(self.open_table_info)
        # TODO: get current selection or QMessageBox.error/ignore
        # self.pb_view_and_modify.clicked.connect(self.table_widget.cellDoubleClicked)  # self.open_table_info)

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
            Student: StudentDialog,
            Report: ReportDialog,
            Discipline: DisciplineDialog,
            StudentGroup: StudentGroupDialog
        }

        dialog = model_dialog_map.get(self.model)
        model_id = int(self.table_widget.item(row, 0).text())
        dialog(model_id=model_id).exec_()


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
