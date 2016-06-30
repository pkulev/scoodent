"""GUI widgets."""

from PyQt4 import QtCore, QtGui, uic

from kisqpy.common import db
from kisqpy.models import Client


class DeleteDialog(QtGui.QDialog):

    def __init__(self, what, from_what):
        QtGui.QDialog.__init__(self)
        self.msg = "Delete {w} from {f} table?".format(w=what, f=from_what)
        uic.loadUi("deldial.ui", self)
        self.label.setText(self.msg)


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("main.ui", self)

        # callbacks
        self.pb_showTable.clicked.connect(self.showTable)

        self.rb_client.clicked.connect(self.rb_to_pb_client)
        self.rb_creator.clicked.connect(self.rb_to_pb_creator)
        self.rb_project.clicked.connect(self.rb_to_pb_project)

        # add to DB callbacks
        self.pb_addClient.clicked.connect(self.addClientToDB)
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

    # Database features
    def connectToDB(self, db, usr):
        """db and usr are strings. If all is OK links to conn connection object"""
        try:
            self.conn = ps2.connect(database=db, user=usr)
        except ps2.DatabaseError as e:
            QtGui.QMessageBox.warning(None, "Error", str(e))
            return False
        else:
            return True

    def disconnect(self):
        """if connection is open - closes it, otherwise prints message"""
        if self.conn.closed:
            print("Already closed")
        else:
            self.conn.close()

    def showTable(self):
        def getTableChoise(self):
            choises = {
                self.rb_client: "client",
                self.rb_creator: "creator",
                self.rb_project: "project",
            }

            for rb, res in choises.items():
                if rb.isChecked():
                    return res

        def extractColumnNames(self, table):
            """Extract column names from table.

            Table is string from which table is needed to extract names
            returns list of column names.
            """

            query = """SELECT column_name FROM information_schema.columns
                       WHERE table_name = {t}""".format(t=repr(table))
            cur = self.conn.cursor()
            cur.execute(query)
            tupledList = cur.fetchall()
            resList = []
            for i in tupledList:
                resList.append(i[0])
            resList.reverse()
            return resList

        def replaceIDs(self, cur_table):
#            query = """SELECT idj from
            pass

        # connect to DB and get table and column labels
        self.connectToDB("model", "most")
        cur = self.conn.cursor()
        cur_what = "*"
        cur_table = getTableChoise(self)
        query = "SELECT {0} FROM {1};".format(cur_what, cur_table)
        cur.execute(query)
        data = cur.fetchall()
        names = extractColumnNames(self, cur_table)
        self.disconnect()

        lines = len(data)
        columns = len(data[0])
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setRowCount(lines)
        self.tableWidget.setColumnCount(columns)

        self.tableWidget.setHorizontalHeaderLabels(names)
        for i in range(lines):
            for j in range(columns):
                decoded = data[i][j]
                decoded = str(decoded).decode("utf-8")
                item = QtGui.QTableWidgetItem(decoded)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)

    # radiobuttons features
    def rb_to_pb_client(self):
        self.pb_showTable.setText("Show client table")

    def rb_to_pb_creator(self):
        self.pb_showTable.setText("Show creator table")

    def rb_to_pb_project(self):
        self.pb_showTable.setText("Show project table")

    def addClientToDB(self):
        class Client:
            pass

        Client.Surname = str(self.le_clientSurname.text())
        Client.Name = str(self.le_clientName.text())
        Client.Address = str(self.le_clientAddress.text())
        Client.Email = str(self.le_clientEmail.text())
        Client.Phone = str(self.le_clientPhone.text())

        if any(
            field == ""
            for field in [
                Client.Surname,
                Client.Name,
                Client.Address,
                Client.Email,
                Client.Phone,
            ]):
            QtGui.QMessageBox.warning(
                self,
                "Error",
                "One or more fields are empty!")
        else:
            query = """INSERT INTO client (surname, name, address, email, phone)
                       VALUES ({s}, {n}, {a}, {e}, {p});
                    """.format(s=repr(Client.Surname), n=repr(Client.Name),
                               a=repr(Client.Address), e=repr(Client.Email),
                               p=repr(Client.Phone))
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
