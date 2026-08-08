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
    QColor, QFont
)

import constants, helpers, widgets, settings
from modules import feltime


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
        self.clock_padding_px = 5
        self.clock_font_size = 16
        self.button_font_size = 12

        # Make main settings object
        self.settings = settings.Settings()

        # Set main window size restrictions
        self.setMinimumSize(400, 300)
        
        # Declare clock elements
        self.clock = QLabel()
        self.clock_font = QFont("Courier New", self.clock_font_size)
        self.clock_font.setBold(True)
        self.clock.setFont(self.clock_font)
        self.update_clock()

        # Declare clock container
        self.clock_container = QWidget(self)
        self.clock_container.setContentsMargins(
            self.padding_px,
            self.clock_padding_px,
            self.padding_px,
            self.clock_padding_px
        )
        self.clock_container.setFixedHeight((self.clock_padding_px * 2) + self.clock_font_size)
        self.clock_container.setStyleSheet("background-color:{bg}; color:{text}".format(
            bg=constants.COLORS["clock_background"],
            text=constants.COLORS["clock_text"])
        )

        # Declare clock area
        self.clock_area = QHBoxLayout(self.clock_container)
        self.clock_area.setContentsMargins(0, 0, 0, 0)
        self.clock_area.setSpacing(self.padding_px)

        # Populate clock area layout
        self.clock_area.addWidget(
            self.clock,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        
        # Declare clock timer
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(250)  # Update 4x a second to keep it as close to synced as possible
        
        # Declare button font
        self.button_font = QFont("Courier New", self.button_font_size)
        self.button_font.setBold(True)
        
        # Declare buttons
        self.converter_calculator_button = QPushButton("CONVERTER\nCALCULATOR")
        self.converter_calculator_button.setFont(self.button_font)
        self.converter_calculator_button.clicked.connect(self.converter_calculator)
         
        # Declare button area
        self.button_area = QGridLayout()
        self.button_area.setContentsMargins(self.padding_px, 0, self.padding_px, 0)
        self.button_area.setSpacing(self.padding_px)

        # Populate button area
        self.entries_array = [
            [
                self.converter_calculator_button,
            ],
        ]
        for column, column_item in enumerate(self.entries_array):
            for row, row_item in enumerate(column_item):
                if row_item is not None:
                    self.button_area.addWidget(
                        row_item,
                        row,
                        column,
                        alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
                    )
        
        # Declare main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(self.padding_px)
        
        # Populate main layout
        self.main_layout.addWidget(self.clock_container)
        self.main_layout.addLayout(self.button_area)
        
        # Set main layout as the central widget
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Finally, set the window size based on it's sizeHint after 10 millis
        #QTimer.singleShot(10, self.setup_window_size)

    def setup_window_size(self):
        size_hint = self.sizeHint()
        start_size = QSize(size_hint.width(), size_hint.height() * 3)
        min_size = QSize(size_hint.width(), size_hint.height() * 2)
        self.setMinimumSize(min_size)
        self.resize(start_size)
    
    def update_clock(self):
        self.clock.setText(feltime.feltime.now().strftime("EPOC %c"))
    
    def converter_calculator(self):
        self.converter_calculator_button.setEnabled(False)
        popup = ConverterCalculator(parent=self)
        result = popup.show()


# ---- POPUP WINDOWS ----

# Converter Calculator
#   Allows conversions and calculations related to in-game and real-life units
class ConverterCalculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"CONVERTER CALCULATOR")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setMinimumSize(300, 200)
        
        # Declare test label
        self.test = QLabel("TEST")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)

        self.setLayout(self.main_layout)
        
        # Finally, set the window size based on it's sizeHint after 10 millis
        #QTimer.singleShot(10, self.setup_window_size)

    def setup_window_size(self):
        size_hint = self.sizeHint()
        start_size = QSize(size_hint.width(), size_hint.height() * 3)
        min_size = QSize(size_hint.width(), size_hint.height() * 2)
        self.setMinimumSize(min_size)
        self.resize(start_size)
    
    def closeEvent(self, event):
        self.parent().converter_calculator_button.setEnabled(True)
        event.accept()