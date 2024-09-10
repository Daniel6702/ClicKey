from PyQt5.QtWidgets import QApplication,QLabel, QMainWindow, QWidget, QHBoxLayout, QListWidget,QVBoxLayout, QStackedWidget
from PyQt5.QtCore import QTimer, Qt
from module_manager.utils import MODULES
from modules.profile_manager.profiles_controller import ProfilesController

class CentralManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Automation Manager")
        self.setGeometry(100, 100, 800, 600)

        self.controllers = []

        # Stacked widget to display the different modules
        self.stacked_widget = QStackedWidget()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        nav_layout = QVBoxLayout()

        # Title for the nav menu
        self.title_label = QLabel("Clickey")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignCenter)  # Center the title

        # Nav menu (QListWidget)
        self.nav_menu = QListWidget()
        self.nav_menu.addItems(MODULES.keys())
        self.nav_menu.currentRowChanged.connect(self.display_module)
        self.nav_menu.setFixedWidth(200) 
        self.nav_menu.setCurrentRow(0)

        # Add the title and nav menu to the nav layout
        nav_layout.addWidget(self.title_label)
        nav_layout.addWidget(self.nav_menu)        
        main_layout.addLayout(nav_layout)  
        main_layout.addWidget(self.stacked_widget)

        central_widget.setLayout(main_layout)

    def load_modules(self):
        for module in MODULES.values():
            self.controllers.append(module())
        
        for controller in self.controllers:
            #add all controllers to the stacked widget
            self.stacked_widget.addWidget(controller.gui)

            if isinstance(controller, ProfilesController):
                controller.add_controllers(self.controllers)

        self.display_module(0)

    def display_module(self, index):
        self.stacked_widget.setCurrentIndex(index)

