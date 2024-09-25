from base_components.base_gui import BaseGUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame,QPushButton, QLabel, QSpinBox, QComboBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class HorizontalLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class SettingsGUI(BaseGUI):
    # Define signals
    delay_changed = pyqtSignal(int)
    theme_changed = pyqtSignal(str)
    hide_in_tray = pyqtSignal()
    

    def __init__(self):
        super().__init__("Settings")
        self.initClickerUI()

    def initClickerUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title_widget.status_label.setText(
            "Clickey is an open-source, Python-based automation utility tool that combines several modules,\n"
            "such as an Auto Mouse Clicker, Auto Key Presser, Script Runner, Color Tools, System Monitor, and more."
        )
        main_layout.addWidget(self.title_widget)

        # Add new GUI elements here
        main_layout.addWidget(HorizontalLine())
        
        # GitHub link
        self.github_button = QPushButton("GitHub Page")
        self.github_button.clicked.connect(self.open_github)

        # Buy Me a Coffee link
        self.coffee_button = QPushButton("Buy Me a Coffee")
        self.coffee_button.clicked.connect(self.open_coffee)

        # Layout for links
        links_layout = QHBoxLayout()
        links_layout.addWidget(self.github_button)
        links_layout.addWidget(self.coffee_button)
        links_layout.addStretch()
        main_layout.addLayout(links_layout)

        main_layout.addWidget(HorizontalLine())

        # Delay before start (s)
        delay_layout = QHBoxLayout()
        self.delay_label = QLabel("Delay before start (s):")
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(0, 3600)  # 0 to 3600 seconds (1 hour)
        self.delay_spinbox.setValue(2)
        self.delay_spinbox.valueChanged.connect(self.on_delay_changed)
        delay_layout.addWidget(self.delay_label)
        delay_layout.addWidget(self.delay_spinbox)
        delay_layout.addStretch()
        main_layout.addLayout(delay_layout)

        main_layout.addWidget(HorizontalLine())

        # Color theme dropdown
        theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Select Color Theme:")
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Dark", "Light", "Modern"])
        self.theme_combobox.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.theme_label)
        theme_layout.addWidget(self.theme_combobox)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        main_layout.addWidget(HorizontalLine())

        # Hide in system tray button
        self.hide_tray_button = QPushButton("Hide in System Tray")
        self.hide_tray_button.clicked.connect(self.hide_in_tray.emit)
        main_layout.addWidget(self.hide_tray_button)

        main_layout.addWidget(HorizontalLine())

        # Spacer to push everything to the top
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

    # Slot methods
    def open_github(self):
        url = QUrl("https://github.com/Daniel6702/ClicKey")  
        QDesktopServices.openUrl(url)

    def open_coffee(self):
        url = QUrl("https://www.buymeacoffee.com/daniel6702") 
        QDesktopServices.openUrl(url)

    def on_delay_changed(self, value):
        self.delay_changed.emit(value)

    def on_theme_changed(self, text):
        self.theme_changed.emit(text)