"""GUI client application."""

import os
import sys

from PyQt4.QtGui import QApplication

from scoodent.client.gui import LoginWindow, MainWindow


def main():
    """Entry point."""

    app = QApplication(sys.argv)
    if LoginWindow.do_login():
        main_window = MainWindow()
        main_window.show()
        return app.exec_()
    return os.EX_SOFWARE


if __name__ == "__main__":
    sys.exit(main())
