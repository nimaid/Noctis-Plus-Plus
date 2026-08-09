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
        self.submit_button.pressed.connect(self.submit)
        
        self.chat_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["chat"]["up"],
            pixmap_hover=BUTTON_ICONS["chat"]["up"],
            pixmap_pressed=BUTTON_ICONS["chat"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.chat_button.setFocusPolicy(Qt.NoFocus)
        self.chat_button.setFixedSize(self.chat_button.width, self.chat_button.height)
        self.chat_button.pressed.connect(self.chat)
        
        self.map_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["map"]["up"],
            pixmap_hover=BUTTON_ICONS["map"]["up"],
            pixmap_pressed=BUTTON_ICONS["map"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.map_button.setFocusPolicy(Qt.NoFocus)
        self.map_button.setFixedSize(self.map_button.width, self.map_button.height)
        self.map_button.pressed.connect(self.map)
        
        self.movie_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["movie"]["up"],
            pixmap_hover=BUTTON_ICONS["movie"]["up"],
            pixmap_pressed=BUTTON_ICONS["movie"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.movie_button.setFocusPolicy(Qt.NoFocus)
        self.movie_button.setFixedSize(self.movie_button.width, self.movie_button.height)
        self.movie_button.pressed.connect(self.movie)
        
        self.screenshot_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["screenshot"]["up"],
            pixmap_hover=BUTTON_ICONS["screenshot"]["up"],
            pixmap_pressed=BUTTON_ICONS["screenshot"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.screenshot_button.setFocusPolicy(Qt.NoFocus)
        self.screenshot_button.setFixedSize(self.screenshot_button.width, self.screenshot_button.height)
        self.screenshot_button.pressed.connect(self.screenshot)
        
        self.calculator_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["calculator"]["up"],
            pixmap_hover=BUTTON_ICONS["calculator"]["up"],
            pixmap_pressed=BUTTON_ICONS["calculator"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.calculator_button.setFocusPolicy(Qt.NoFocus)
        self.calculator_button.setFixedSize(self.calculator_button.width, self.calculator_button.height)
        self.calculator_button.pressed.connect(self.calculator)
        
        self.build_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["build"]["up"],
            pixmap_hover=BUTTON_ICONS["build"]["up"],
            pixmap_pressed=BUTTON_ICONS["build"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.build_button.setFocusPolicy(Qt.NoFocus)
        self.build_button.setFixedSize(self.build_button.width, self.build_button.height)
        self.build_button.pressed.connect(self.build)
        
        self.update_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["update"]["up"],
            pixmap_hover=BUTTON_ICONS["update"]["up"],
            pixmap_pressed=BUTTON_ICONS["update"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.update_button.setFocusPolicy(Qt.NoFocus)
        self.update_button.setFixedSize(self.update_button.width, self.update_button.height)
        self.update_button.pressed.connect(self.update)
        
        self.launch_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["launch"]["up"],
            pixmap_hover=BUTTON_ICONS["launch"]["up"],
            pixmap_pressed=BUTTON_ICONS["launch"]["down"],
            scale=self.button_scale,
            parent=self
        )
        self.launch_button.setFocusPolicy(Qt.NoFocus)
        self.launch_button.setFixedSize(self.launch_button.width, self.launch_button.height)
        self.launch_button.pressed.connect(self.launch)
        
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
                self.movie_button,
                self.screenshot_button,
                self.calculator_button,
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
    
    def position_popup(self, popup, horizontal, vertical):
        main_geometry = self.frameGeometry()
        main_available_geometry = self.geometry()
        popup_geometry = popup.frameGeometry()
        screen_available_geometry = self.windowHandle().screen().availableGeometry()
        screen_geometry = self.windowHandle().screen().geometry()
        
        taskbar_height = screen_geometry.height() - screen_available_geometry.height()
        titlebar_height = main_geometry.height() - main_available_geometry.height()
        
        match horizontal:
            case constants.HorizontalAlign.LEFT:
                x = main_geometry.x() - popup_geometry.width()
            case constants.HorizontalAlign.CENTER:
                 x = round(main_geometry.x() - (popup_geometry.width() / 2) + (main_geometry.width() / 2))
            case constants.HorizontalAlign.RIGHT:
                x = main_geometry.x() + main_geometry.width()
        
        match vertical:
            case constants.VerticalAlign.TOP:
                y = main_geometry.y() - popup_geometry.height() - titlebar_height
            case constants.VerticalAlign.CENTER:
                 y = round(main_geometry.y() - (popup_geometry.height() / 2) + (main_geometry.height() / 2))
            case constants.VerticalAlign.BOTTOM:
                y = main_geometry.y() + main_geometry.height()
        
        min_x = screen_available_geometry.x()
        max_x = min_x + screen_available_geometry.width() - popup_geometry.width()
        min_y = screen_available_geometry.y()
        max_y = min_y + screen_available_geometry.height() - popup_geometry.height() - taskbar_height
        
        if x < min_x:
            x = min_x
        if x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        if y > max_y:
            y = max_y
        
        popup.move(x, y)
    
    def submit(self):
        self.submit_button.setEnabled(False)
        self.submit_button.setDown(True)
        
        popup = Submit(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.LEFT, constants.VerticalAlign.TOP)
        result = popup.show()
    
    def chat(self):
        self.chat_button.setEnabled(False)
        self.chat_button.setDown(True)
        
        popup = Chat(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.CENTER, constants.VerticalAlign.TOP)
        result = popup.show()
    
    def map(self):
        self.map_button.setEnabled(False)
        self.map_button.setDown(True)
        
        popup = Map(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.RIGHT, constants.VerticalAlign.TOP)
        result = popup.show()
    
    def movie(self):
        self.movie_button.setEnabled(False)
        self.movie_button.setDown(True)
        
        popup = Movie(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.LEFT, constants.VerticalAlign.CENTER)
        result = popup.show()
    
    def screenshot(self):
        self.screenshot_button.setEnabled(False)
        self.screenshot_button.setDown(True)
        
        popup = Screenshot(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.LEFT, constants.VerticalAlign.CENTER)
        result = popup.show()
    
    def calculator(self):
        self.calculator_button.setEnabled(False)
        self.calculator_button.setDown(True)
        
        popup = Calculator(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.RIGHT, constants.VerticalAlign.CENTER)
        result = popup.show()
    
    def build(self):
        self.build_button.setEnabled(False)
        self.build_button.setDown(True)
        
        popup = Build(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.LEFT, constants.VerticalAlign.BOTTOM)
        result = popup.show()
    
    def update(self):
        self.update_button.setEnabled(False)
        self.update_button.setDown(True)
        
        popup = Update(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.CENTER, constants.VerticalAlign.BOTTOM)
        result = popup.show()
    
    def launch(self):
        self.launch_button.setEnabled(False)
        self.launch_button.setDown(True)
        
        popup = Launch(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.RIGHT, constants.VerticalAlign.BOTTOM)
        result = popup.show()


# ---- POPUP WINDOWS ----

# Submit Outbox
#   Allows the user to submit their outbox
class Submit(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"SUBMIT OUTBOX")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().submit_button.setDown(False)
        self.parent().submit_button.setEnabled(True)
        
        event.accept()


# Live Chat
#   Allows the user to speak live with other players
class Chat(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"LIVE CHAT")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().chat_button.setDown(False)
        self.parent().chat_button.setEnabled(True)
        
        event.accept()


# View Map
#   Allows the user to view the Starmap, GUIDE, and their outbox
class Map(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"VIEW MAP")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().map_button.setDown(False)
        self.parent().map_button.setEnabled(True)
        
        event.accept()


# Movie Converter
#   Allows the user to convert their moviedecks into videos
class Movie(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"MOVIE CONVERTER")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().movie_button.setDown(False)
        self.parent().movie_button.setEnabled(True)
        
        event.accept()


# Screenshot Converter
#   Allows the user to convert their screenshots into different formats and
#   higher resolutions
class Screenshot(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"SCREENSHOT CONVERTER")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().screenshot_button.setDown(False)
        self.parent().screenshot_button.setEnabled(True)
        
        event.accept()


# Converter Calculator
#   Allows conversions and calculations related to in-game and real-life units
class Calculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"CONVERTER CALCULATOR")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().calculator_button.setDown(False)
        self.parent().calculator_button.setEnabled(True)
        
        event.accept()


# Build Noctis
#   Allows the user to build Noctis from source
class Build(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"BUILD NOCTIS")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().build_button.setDown(False)
        self.parent().build_button.setEnabled(True)
        
        event.accept()


# Update Data
#   Allows the user to download updates to the GUIDE and Starmap
class Update(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"UPDATE DATA")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().update_button.setDown(False)
        self.parent().update_button.setEnabled(True)
        
        event.accept()

# Launch Noctis
#   Allows the user to launch Noctis
class Launch(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setup window title and icon
        self.setWindowTitle(f"LAUNCH NOCTIS")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = QLabel("COMING SOON")
        self.test.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().launch_button.setDown(False)
        self.parent().launch_button.setEnabled(True)
        
        event.accept()
