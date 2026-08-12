import os
from PIL import Image
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget,
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
        self.noctis_font = QPixmap(constants.FONT_PATHS["noctis"])
        self.main_font = QPixmap(constants.FONT_PATHS["legible"])
        self.pixel_scale = 3

        # Make main settings object
        self.settings = settings.Settings()

        # Set main window size restrictions
        self.setFixedSize(500, 350)
        
        # Declare clock elements
        self.clock = widgets.ImageFontLabel(self.noctis_font, scale=self.pixel_scale, color=constants.COLORS["clock_text"])
        self.update_clock()

        # Declare clock container
        self.clock_container = QWidget(self)
        self.clock_container.setContentsMargins(
            self.padding_px,
            self.clock_padding_px,
            self.padding_px,
            self.clock_padding_px
        )
        self.clock_container.setFixedHeight((self.clock_padding_px * 2) + self.clock.char_height)
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
        
        # Declare "DON'T PANIC" icon
        self.panic_icon = QPixmap(constants.PANIC_ICON_PATH)
        
        # Declare "DON'T PANIC" picture label
        self.panic_label = widgets.ImageLabel(
            pixmap=self.panic_icon,
            scale=self.pixel_scale,
            parent=self
        )
        
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
            "media": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["media"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["media"]["down"]),
            },
            "manual": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["manual"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["manual"]["down"]),
            },
            "data": {
                "up": QPixmap(constants.BUTTON_ICON_PATHS["data"]["up"]),
                "down": QPixmap(constants.BUTTON_ICON_PATHS["data"]["down"]),
            },
        }
        
        # Declare buttons
        self.manual_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["manual"]["up"],
            pixmap_hover=BUTTON_ICONS["manual"]["up"],
            pixmap_pressed=BUTTON_ICONS["manual"]["down"],
            scale=self.pixel_scale,
            parent=self
        )
        self.manual_button.setFocusPolicy(Qt.NoFocus)
        self.manual_button.setFixedSize(self.manual_button.width, self.manual_button.height)
        self.manual_button.pressed.connect(self.manual)
        
        self.chat_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["chat"]["up"],
            pixmap_hover=BUTTON_ICONS["chat"]["up"],
            pixmap_pressed=BUTTON_ICONS["chat"]["down"],
            scale=self.pixel_scale,
            parent=self
        )
        self.chat_button.setFocusPolicy(Qt.NoFocus)
        self.chat_button.setFixedSize(self.chat_button.width, self.chat_button.height)
        self.chat_button.pressed.connect(self.chat)
        
        self.map_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["map"]["up"],
            pixmap_hover=BUTTON_ICONS["map"]["up"],
            pixmap_pressed=BUTTON_ICONS["map"]["down"],
            scale=self.pixel_scale,
            parent=self
        )
        self.map_button.setFocusPolicy(Qt.NoFocus)
        self.map_button.setFixedSize(self.map_button.width, self.map_button.height)
        self.map_button.pressed.connect(self.map)
        
        self.media_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["media"]["up"],
            pixmap_hover=BUTTON_ICONS["media"]["up"],
            pixmap_pressed=BUTTON_ICONS["media"]["down"],
            scale=self.pixel_scale,
            parent=self
        )
        self.media_button.setFocusPolicy(Qt.NoFocus)
        self.media_button.setFixedSize(self.media_button.width, self.media_button.height)
        self.media_button.pressed.connect(self.media)
        
        self.calculator_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["calculator"]["up"],
            pixmap_hover=BUTTON_ICONS["calculator"]["up"],
            pixmap_pressed=BUTTON_ICONS["calculator"]["down"],
            scale=self.pixel_scale,
            parent=self
        )
        self.calculator_button.setFocusPolicy(Qt.NoFocus)
        self.calculator_button.setFixedSize(self.calculator_button.width, self.calculator_button.height)
        self.calculator_button.pressed.connect(self.calculator)
        
        self.build_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["build"]["up"],
            pixmap_hover=BUTTON_ICONS["build"]["up"],
            pixmap_pressed=BUTTON_ICONS["build"]["down"],
            scale=self.pixel_scale,
            parent=self
        )
        self.build_button.setFocusPolicy(Qt.NoFocus)
        self.build_button.setFixedSize(self.build_button.width, self.build_button.height)
        self.build_button.pressed.connect(self.build)
        
        self.data_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["data"]["up"],
            pixmap_hover=BUTTON_ICONS["data"]["up"],
            pixmap_pressed=BUTTON_ICONS["data"]["down"],
            scale=self.pixel_scale,
            parent=self
        )
        self.data_button.setFocusPolicy(Qt.NoFocus)
        self.data_button.setFixedSize(self.data_button.width, self.data_button.height)
        self.data_button.pressed.connect(self.data)
        
        self.launch_button = widgets.ImageButton(
            pixmap=BUTTON_ICONS["launch"]["up"],
            pixmap_hover=BUTTON_ICONS["launch"]["up"],
            pixmap_pressed=BUTTON_ICONS["launch"]["down"],
            scale=self.pixel_scale,
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
                self.manual_button,
                self.chat_button,
                self.map_button,
            ],
            [
                self.media_button,
                self.panic_label,
                self.calculator_button,
            ],
            [
                self.build_button,
                self.data_button,
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
        self.clock.setText(feltime.datetime.now().strftime("EPOC %e & %t"))
    
    def position_popup(self, popup, horizontal, vertical):
        main_geometry = self.frameGeometry()
        main_available_geometry = self.geometry()
        popup_geometry = popup.frameGeometry()
        screen_available_geometry = self.windowHandle().screen().availableGeometry()
        screen_geometry = self.windowHandle().screen().geometry()
        
        taskbar_height = screen_geometry.height() - screen_available_geometry.height()
        titlebar_height = main_geometry.height() - main_available_geometry.height()
        frame_width = main_geometry.width() - main_available_geometry.width()
        
        match horizontal:
            case constants.HorizontalAlign.LEFT:
                x = main_geometry.x() - popup_geometry.width() - frame_width
            case constants.HorizontalAlign.CENTER:
                 x = round(main_geometry.x() - (popup_geometry.width() / 2) + (main_geometry.width() / 2))
            case constants.HorizontalAlign.RIGHT:
                x = main_geometry.x() + main_geometry.width()
        
        match vertical:
            case constants.VerticalAlign.TOP:
                y = main_geometry.y() - (popup_geometry.height() + titlebar_height)
            case constants.VerticalAlign.CENTER:
                 y = main_geometry.y() - round((popup_geometry.height() + titlebar_height - main_geometry.height()) / 2)
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
    
    def manual(self):
        self.manual_button.setEnabled(False)
        self.manual_button.setDown(True)
        
        popup = Manual(parent=self)
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
    
    def media(self):
        self.media_button.setEnabled(False)
        self.media_button.setDown(True)
        
        popup = Media(parent=self)
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
    
    def data(self):
        self.data_button.setEnabled(False)
        self.data_button.setDown(True)
        
        popup = Data(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.CENTER, constants.VerticalAlign.BOTTOM)
        result = popup.show()
    
    def launch(self):
        self.launch_button.setEnabled(False)
        self.launch_button.setDown(True)
        
        popup = Launch(parent=self)
        self.position_popup(popup, constants.HorizontalAlign.RIGHT, constants.VerticalAlign.BOTTOM)
        result = popup.show()


# ---- POPUP WINDOWS ----

# Manual Reader
#   Allows the user to view the HTML manual
class Manual(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Manual Reader")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = widgets.ImageFontLabel(self.font, "Coming Soon", scale=self.pixel_scale, color=constants.COLORS["text"])
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().manual_button.setDown(False)
        self.parent().manual_button.setEnabled(True)
        
        event.accept()


# Live Chat
#   Allows the user to speak live with other players
class Chat(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Live Chat")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = widgets.ImageFontLabel(self.font, "Coming Soon", scale=self.pixel_scale, color=constants.COLORS["text"])
        
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


# Map Viewer
#   Allows the user to view the Starmap, GUIDE, and their outbox
class Map(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Map Viewer")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = widgets.ImageFontLabel(self.font, "Coming Soon", scale=self.pixel_scale, color=constants.COLORS["text"])
        
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


# Media Converter
#   Allows the user to convert their screenshots and moviedecks into different
#   formats and higher resolutions
class Media(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Media Converter")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = widgets.ImageFontLabel(self.font, "Coming Soon", scale=self.pixel_scale, color=constants.COLORS["text"])
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().media_button.setDown(False)
        self.parent().media_button.setEnabled(True)
        
        event.accept()


# Converter Calculator
#   Allows conversions and calculations related to in-game and real-life units
class Calculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Converter Calculator")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(400, 300)
        
        # ---- TABS START ----
        
        # Declare tab bar
        self.tab_bar = QTabWidget()
        self.tab_bar.setStyleSheet(f"""
            QTabWidget > QWidget {{ 
                background-color: {constants.COLORS["background"]}; 
            }}
            
            QTabWidget::pane {{
                border: 0;
            }}
            
            QTabBar::tab {{
                background-color: {constants.COLORS["tab_background"]};
                color: {constants.COLORS["text"]};
            }}
            
            QTabBar::tab:selected {{
                background-color: {constants.COLORS["tab_foreground"]};
            }}
        """)
        
        # Declare tab variables
        self.tabs = []
        self.tab_layouts = []
        
        # -- TIME TAB --
        
        # Declare time tab
        self.tabs.append(QWidget())
        self.tab_bar.addTab(self.tabs[-1], "Time")
        
        # Declare time tab layout
        self.tab_layouts.append(QGridLayout())
        
        # Declare time tab test labels
        self.fox_label = widgets.ImageFontLabel(
            self.font,
            "THE QUICK BROWN FOX\nJUMPS OVER THE\nLAZY DOG\n\nthe quick brown fox\njumps over the\nlazy dog\n\n`1234567890-=[]\\;',./\n~!@#$%^&*()_+{}|:\"<>?",
            align=constants.TextAlign.CENTERED,
            scale=self.pixel_scale,
            color=constants.COLORS["text"]
        )
        
        # Populate time tab layout
        self.tab_layouts[-1].addWidget(self.fox_label, 0, 0)
        
        # Set the time tab layout
        self.tabs[-1].setLayout(self.tab_layouts[-1])
        
        # -- DISTANCE TAB --
        
        # Declare distance tab
        self.tabs.append(QWidget())
        self.tab_bar.addTab(self.tabs[-1], "Distance")
        
        # Declare distance tab layout
        self.tab_layouts.append(QGridLayout())
        
        # Declare distance tab test labels
        self.alphabet_label = widgets.ImageFontLabel(
            self.font,
            "3x5 Microfont by\nElla Jameson (nimaid)\n\nABCDEFGHIJKLM\nabcdefghijklm\n\nNOPQRSTUVWXYZ\nnopqrstuvwxyz\n\n`1234567890-=[]\\;',./\n~!@#$%^&*()_+{}|:\"<>?",
            align=constants.TextAlign.CENTERED,
            scale=self.pixel_scale,
            color=constants.COLORS["text"]
        )
        
        # Populate distance tab layout
        self.tab_layouts[-1].addWidget(self.alphabet_label, 0, 0)
        
        # Set the time tab layout
        self.tabs[-1].setLayout(self.tab_layouts[-1])
        
        # ---- TABS END ---
        
        # Declare main layout
        self.main_layout = QVBoxLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.tab_bar)
        
        # Set the main layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().calculator_button.setDown(False)
        self.parent().calculator_button.setEnabled(True)
        
        event.accept()


# Noctis Builder
#   Allows the user to build Noctis from source
class Build(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Noctis Builder")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = widgets.ImageFontLabel(self.font, "Coming Soon", scale=self.pixel_scale, color=constants.COLORS["text"])
        
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


# Data Manager
#   Allows the user to download updates to the GUIDE and Starmap, in addition
#   to submitting their outbox
class Data(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Data Manager")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = widgets.ImageFontLabel(self.font, "Coming Soon", scale=self.pixel_scale, color=constants.COLORS["text"])
        
        # Declare main layout
        self.main_layout = QGridLayout()
        
        # Populate main layout
        self.main_layout.addWidget(self.test, 0, 0)
        
        # Set the layout
        self.setLayout(self.main_layout)
        
    
    def closeEvent(self, event):
        self.parent().data_button.setDown(False)
        self.parent().data_button.setEnabled(True)
        
        event.accept()

# Noctis Launcher
#   Allows the user to launch Noctis
class Launch(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Declare window variables
        self.pixel_scale = self.parent().pixel_scale
        self.font = self.parent().main_font
        
        # Setup window title and icon
        self.setWindowTitle(f"Noctis Launcher")
        self.setWindowIcon(QIcon(constants.ICON_PATH))

        # Hide "?" button
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Set window size restrictions
        self.setFixedSize(300, 200)
        
        # Declare test label
        self.test = widgets.ImageFontLabel(self.font, "Coming Soon", scale=self.pixel_scale, color=constants.COLORS["text"])
        
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
