"""GUI widgets."""

import datetime

from PyQt4 import QtCore, QtGui, uic

from kisqpy.common import db, config
from kisqpy.models import Client, Ticket, Departure


class DeleteDialog(QtGui.QDialog):

    def __init__(self, what, from_what):
        QtGui.QDialog.__init__(self)
        self.msg = "Delete {w} from {f} table?".format(w=what, f=from_what)
        uic.loadUi(config.UI["delete_dialog"], self)
        self.label.setText(self.msg)


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(config.UI["main"], self)

        # callbacks
        self.pb_showTable.clicked.connect(self.showTable)

        self.rb_client.clicked.connect(self.rb_to_pb_client)
        self.rb_ticket.clicked.connect(self.rb_to_pb_ticket)
        self.rb_departure.clicked.connect(self.rb_to_pb_departure)

        # add to DB callbacks
        self.pb_addClient.clicked.connect(self.add_client)
        self.pb_addCreator.clicked.connect(self.addCreatorToDB)
        self.pb_addProject.clicked.connect(self.addProjectToDB)
        # remove from DB callbacks
        self.pb_delClient.clicked.connect(self.delClient)
        self.pb_delCreator.clicked.connect(self.delCreator)
        self.pb_delProject.clicked.connect(self.delProject)
        # modify callbacks
        self.pb_changeClient.clicked.connect(self.changeClient)
        self.pb_changeCreator.clicked.connect(self.changeCreator)
        self.pb_changeProject.clicked.connect(self.changeProject)

        # Database variables
        self.conn = None
        # delete if not needed
        self.cur = None
        self.data = None

    @staticmethod
    def insert_objects(obj):
        """Insert object or objects to DB."""

        session = db.get_session()
        if isinstance(obj, (tuple, list)):
            session.add_all(obj)
        else:
            session.merge(obj)
        session.commit()

    def showTable(self):
        def get_table_choise():
            choises = {
                self.rb_client: Client,
                self.rb_ticket: Ticket,
                self.rb_departure: Departure,
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

        lines = len(data)
        columns = len(names)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setRowCount(lines)
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.setHorizontalHeaderLabels(names)

        for i in range(lines):
            for j in range(columns):
                item = QtGui.QTableWidgetItem(str(data[i].__dict__[names[j]]))
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def rb_to_pb_client(self):
        self.pb_showTable.setText("Show client table")

    def rb_to_pb_ticket(self):
        self.pb_showTable.setText("Show ticket table")

    def rb_to_pb_departure(self):
        self.pb_showTable.setText("Show departure table")

    def add_client(self):
        client = {
            "name": str(self.le_clientName.text()),
            "surname": str(self.le_clientSurname.text()),
            "birthdate": datetime.date(2016, 6, 12),
            "city": str(self.le_clientCity.text()),
            "street": str(self.le_clientStreet.text()),
            "phone": str(self.le_clientPhone.text()),
        }

        if not all(client.values()):
            QtGui.QMessageBox.warning(
                self, "Error",
                "One or more fields are empty!")
        else:
            #self.insert_objects(Client(**client))
            db.get_session().merge(Client(**client))

    def addCreatorToDB(self):
        class Creator:
            pass

        Creator.Surname = unicode(
            self.le_creatorSurname.text()).encode("utf-8")
        Creator.Name = str(self.le_creatorName.text())
        Creator.Position = str(self.cb_creatorPosition.currentText())
        print(Creator.Surname)
        if (Creator.Surname == "" or Creator.Name == ""):
            QtGui.QMessageBox.warning(
                self,
                "Error",
                "One or more fields are empty!")
        else:
            query = """INSERT INTO creator (surname, name, position)
                       VALUES ({s}, {n}, {p});
                    """.format(s=repr(Creator.Surname), n=repr(Creator.Name),
                               p=repr(Creator.Position))
            try:
                self.connectToDB("model", "most")
                cur = self.conn.cursor()
                cur.execute(query)
                self.conn.commit()
            except ps2.DatabaseError as e:
                if self.conn:
                    self.conn.rollback()
                    QtGui.QMessageBox.warning(self, "Error", str(e))
            finally:
                self.disconnect()

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
            QtGui.QMessageBox.warning(
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
                    QtGui.QMessageBox.warning(self, "Error", str(e))
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
            QtGui.QMessageBox(self, "Error", "One field is empty")
            return

        try:
            self.connectToDB("model", "most")
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
        except ps2.DatabaseError as e:
            if self.conn:
                QtGui.QMessageBox(self, "Error", str(e))
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
        if w.exec_() == QtGui.QDialog.Accepted:
            self.abstractDel("client", clientID, clientSurname, clientName)
            self.showTable()

    def delCreator(self):
        # get info
        if self.rb_delCreatorByID.isChecked():
            creatorID = str(self.le_delCreatorID.text())
            creatorSurname = None
            creatorName = None
        else:
            creatorSurname = str(self.le_delCreatorSurname.text())
            creatorName = str(self.le_delCreatorName.text())
            creatorID = None

        # set parameters
        w = DeleteDialog("this record", "creator")
        if w.exec_() == QtGui.QDialog.Accepted:
            self.abstractDel("creator", creatorID, creatorSurname, creatorName)
            self.showTable()

    def delProject(self):
        projectID = str(self.le_delProjectID.text())

        w = DeleteDialog("this record", "project")
        if w.exec_() == QtGui.QDialog.Accepted:
            self.abstractDel("project", object_id=projectID)
            self.showTable()

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
            QtGui.QMessageBox.warning(self, "Error", str(e))
            if self.conn:
                self.conn.rollback()
        finally:
            self.conn.close

    def changeClient(self):
        table = "client"
        ident = str(self.le_changeClientID.text())
        field = str(self.cb_changeClientField.currentItem())
        target = str(self.le_changeClientTarget.text())
        self.abstractChange(table, field, target, ident)
        self.rb_client.setEnabled(True)
        self.showTable()

    def changeCreator(self):
        table = "creator"
        ident = str(self.le_changeCreatorID.text())
        field = str(self.cb_changeCreatorField.currentText())
        target = str(self.le_changeCreatorTarget.text())
        self.abstractChange(table, field, target, ident)
        self.rb_creator.setEnabled(True)
        self.showTable()

    def changeProject(self):
        table = "project"
        ident = str(self.le_changeProjectID.text())
        field = str(self.cb_changeProjectField.currentText())
        target = str(self.le_changeProjectTarget.text())
        self.abstractChange(table, field, target, ident)
        self.rb_project.setEnabled(True)
        self.showTable()


def login(login):
    l = login()
    return l.exec_() == QtGui.QDialog.Accepted


class LoginWindow(QtGui.QDialog):
    """Login dialog window."""

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.login = QtGui.QLineEdit(self)
        self.password = QtGui.QLineEdit(self)
        self.b_login = QtGui.QPushButton("Login", self)
        self.b_login.clicked.connect(self.handle_login)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.login)
        layout.addWidget(self.password)
        layout.addWidget(self.b_login)

    def handle_login(self):
        if (
                self.login.text() == "admin" and
                self.password.text() == "admin"
        ):
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, "Error", "Bad user or password")

    @staticmethod
    def do_login():
        return LoginWindow().exec_() == QtGui.QDialog.Accepted
