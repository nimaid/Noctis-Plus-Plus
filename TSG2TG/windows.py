import os
from PIL import Image
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QGridLayout, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton,
    QFileDialog, QAction, QSizePolicy,
    QDialog, QDialogButtonBox, QComboBox, QCheckBox,
    QSpinBox, QDoubleSpinBox
)
from PyQt5.QtGui import (
    QPixmap, QIcon,
    QColor
)

import constants, helpers, widgets, settings


# ---- MAIN WINDOW ----

# My QMainWindow class
#   Used to customize the main window.
class MyQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup window title and icon
        self.setWindowTitle(f"{constants.TITLE}")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Declare variables
        self.padding_px = 10

        # Make main settings object
        self.settings = settings.Settings()

        # Set main window size restrictions
        self.setMinimumSize(300, 300)
        
        # Declare 
        

        # Declare main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(self.padding_px)

        # Populate main layout
        

        # Set main layout as the central widget
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Declare a menu bar
        self.main_menu = self.menuBar()

        # Declare 
        

        # Populate 
        

        # Finally, set the window size based on it's sizeHint after 10 millis
        #QTimer.singleShot(10, self.setup_window_size)

    def setup_window_size(self):
        size_hint = self.sizeHint()
        start_size = QSize(size_hint.width(), size_hint.height() * 3)
        min_size = QSize(size_hint.width(), size_hint.height() * 2)
        self.setMinimumSize(min_size)
        self.resize(start_size)



# ---- POPUP WINDOWS ----

