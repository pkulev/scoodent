"""GUI client application."""

import sys

from PyQt4 import QtGui

from kisqpy.client.gui import LoginWindow, MainWindow
from kisqpy.common import config


def main():
    """Entry point."""
    print(config.UI)
    app = QtGui.QApplication(sys.argv)
    if LoginWindow.do_login():
        main_window = MainWindow()
        main_window.show()
        return app.exec_()
    return 1


if __name__ == "__main__":
    sys.exit(main())
