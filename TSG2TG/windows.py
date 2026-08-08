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
        self.button_padding_px = 10
        self.clock_font_size = 16
        self.button_scale = 3.0

        # Make main settings object
        self.settings = settings.Settings()

        # Set main window size restrictions
        self.setFixedSize(500, 350)
        
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
        
        # Declare button icons
        BUTTON_ICONS = {
            "build": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["build"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["build"]["down"]),
            },
            "calculator": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["calculator"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["calculator"]["down"]),
            },
            "chat": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["chat"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["chat"]["down"]),
            },
            "launch": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["launch"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["launch"]["down"]),
            },
            "map": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["map"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["map"]["down"]),
            },
            "movie": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["movie"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["movie"]["down"]),
            },
            "submit": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["submit"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["submit"]["down"]),
            },
            "screenshot": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["screenshot"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["screenshot"]["down"]),
            },
            "update": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["update"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["update"]["down"]),
            },
        }
        
        # Declare buttons
        self.submit_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["submit"]["up"],
            pixmap_hover=BUTTON_ICONS["submit"]["up"],
            pixmap_pressed=BUTTON_ICONS["submit"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.submit_button.setFocusPolicy(Qt.NoFocus)
        self.submit_button.setFixedSize(self.submit_button.width, self.submit_button.height)
        
        self.chat_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["chat"]["up"],
            pixmap_hover=BUTTON_ICONS["chat"]["up"],
            pixmap_pressed=BUTTON_ICONS["chat"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.chat_button.setFocusPolicy(Qt.NoFocus)
        self.chat_button.setFixedSize(self.chat_button.width, self.chat_button.height)
        
        self.map_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["map"]["up"],
            pixmap_hover=BUTTON_ICONS["map"]["up"],
            pixmap_pressed=BUTTON_ICONS["map"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.map_button.setFocusPolicy(Qt.NoFocus)
        self.map_button.setFixedSize(self.map_button.width, self.map_button.height)
        
        self.movie_converter_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["movie"]["up"],
            pixmap_hover=BUTTON_ICONS["movie"]["up"],
            pixmap_pressed=BUTTON_ICONS["movie"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.movie_converter_button.setFocusPolicy(Qt.NoFocus)
        self.movie_converter_button.setFixedSize(self.movie_converter_button.width, self.movie_converter_button.height)
        
        self.screenshot_converter_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["screenshot"]["up"],
            pixmap_hover=BUTTON_ICONS["screenshot"]["up"],
            pixmap_pressed=BUTTON_ICONS["screenshot"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.screenshot_converter_button.setFocusPolicy(Qt.NoFocus)
        self.screenshot_converter_button.setFixedSize(self.screenshot_converter_button.width, self.screenshot_converter_button.height)
        
        self.converter_calculator_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["calculator"]["up"],
            pixmap_hover=BUTTON_ICONS["calculator"]["up"],
            pixmap_pressed=BUTTON_ICONS["calculator"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.converter_calculator_button.setFocusPolicy(Qt.NoFocus)
        self.converter_calculator_button.setFixedSize(self.converter_calculator_button.width, self.converter_calculator_button.height)
        self.converter_calculator_button.pressed.connect(self.converter_calculator)
        
        self.build_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["build"]["up"],
            pixmap_hover=BUTTON_ICONS["build"]["up"],
            pixmap_pressed=BUTTON_ICONS["build"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.build_button.setFocusPolicy(Qt.NoFocus)
        self.build_button.setFixedSize(self.build_button.width, self.build_button.height)
        
        self.update_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["update"]["up"],
            pixmap_hover=BUTTON_ICONS["update"]["up"],
            pixmap_pressed=BUTTON_ICONS["update"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.update_button.setFocusPolicy(Qt.NoFocus)
        self.update_button.setFixedSize(self.update_button.width, self.update_button.height)
        
        self.launch_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["launch"]["up"],
            pixmap_hover=BUTTON_ICONS["launch"]["up"],
            pixmap_pressed=BUTTON_ICONS["launch"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.launch_button.setFocusPolicy(Qt.NoFocus)
        self.launch_button.setFixedSize(self.launch_button.width, self.launch_button.height)
        
        # Declare button area
        self.button_area = QGridLayout()
        self.button_area.setContentsMargins(self.padding_px, 0, self.padding_px, 0)
        self.button_area.setSpacing(self.padding_px)

        # Populate button area
        self.entries_array = [
            [
                self.submit_button,
                self.chat_button,
                self.map_button,
            ],
            [
                self.movie_converter_button,
                self.screenshot_converter_button,
                self.converter_calculator_button,
            ],
            [
                self.build_button,
                self.update_button,
                self.launch_button,
            ],
        ]
        for row, row_item in enumerate(self.entries_array):
            for column, column_item in enumerate(row_item):
                if column_item is not None:
                    self.button_area.addWidget(
                        column_item,
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
    
    def update_clock(self):
        self.clock.setText(feltime.feltime.now().strftime("EPOC %c"))
    
    def converter_calculator(self):
        self.converter_calculator_button.setEnabled(False)
        self.converter_calculator_button.setDown(True)
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
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().converter_calculator_button.setDown(False)
        self.parent().converter_calculator_button.setEnabled(True)
        event.accept()
