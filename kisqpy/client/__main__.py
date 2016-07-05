"""GUI client application."""

import sys

from PyQt4 import QtGui

from kisqpy.client.gui import LoginWindow, MainWindow


def main():
    """Entry point."""

    app = QtGui.QApplication(sys.argv)
    if LoginWindow.do_login():
        main_window = MainWindow()
        main_window.show()
        return app.exec_()
    return 1


if __name__ == "__main__":
    sys.exit(main())
