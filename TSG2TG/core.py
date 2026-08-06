import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

import windows, constants


class MainWindow:
    def __init__(self, qt_args):
        # Apply dark mode on Windows systems
        if constants.PLATFORM == constants.PlatformCode.WINDOWS:
            os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=1"

        # Make main objects
        self.app = QApplication(qt_args)
        self.window = windows.MyQMainWindow()

    def run(self):
        self.window.show()
        self.app.exec()


def run(args=None):
    if args is None:
        args = sys.argv

    main_window = MainWindow(args)
    main_window.run()

run()
