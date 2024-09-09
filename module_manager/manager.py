from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget
from PyQt5.QtCore import QTimer

from mouse_clicker.mouse_clicker_controller import ClickerController
from key_presser.key_presser_controller import PresserController
from color_tool.color_tool_controller import ColorController
from script_runner.script_controller import ScriptController

def apply_stylesheet(app: QApplication, path: str) -> None:
    with open(path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)

class CentralManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main layout
        self.setWindowTitle("Automation Manager")
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a horizontal layout to divide the navigation and module display
        main_layout = QHBoxLayout()

        # Navigation menu on the left (QListWidget)
        self.nav_menu = QListWidget()
        self.nav_menu.addItems(["Mouse Clicker", "Key Presser", "Color Tool", "Script Runner"])
        self.nav_menu.currentRowChanged.connect(self.display_module)  # Connect navigation change to display handler

        # Stacked widget on the right to display module GUIs
        self.stacked_widget = QStackedWidget()

        # Add both widgets to the main layout
        main_layout.addWidget(self.nav_menu)
        main_layout.addWidget(self.stacked_widget)

        # Set the layout to the central widget
        central_widget.setLayout(main_layout)

        # Initialize a placeholder for the controllers
        self.controllers = [None] * 4  # This will store controller instances

        # Set empty widgets as placeholders in the stacked widget (for now)
        for _ in range(4):
            self.stacked_widget.addWidget(QWidget())  # Empty placeholder widget for each module

        # Schedule display_module(0) to run after 1 second
        QTimer.singleShot(1000, lambda: self.display_module(0))  # 1000 milliseconds = 1 second

    def display_module(self, index):
        """ Lazy load the module when selected """
        if self.controllers[index] is None:
            # Initialize the controller only when it is accessed for the first time
            if index == 0:
                self.controllers[index] = ClickerController()
            elif index == 1:
                self.controllers[index] = PresserController()
            elif index == 2:
                self.controllers[index] = ColorController()
            elif index == 3:
                self.controllers[index] = ScriptController()

            # Replace the placeholder widget with the actual controller's GUI
            self.stacked_widget.removeWidget(self.stacked_widget.widget(index))  # Remove placeholder
            self.stacked_widget.insertWidget(index, self.controllers[index].gui)

        # Display the selected module
        self.stacked_widget.setCurrentIndex(index)