from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class BaseAutoActionGUI(QWidget):
    changeSettings = pyqtSignal(dict, name='changeSettings')
    changeStatus = pyqtSignal(bool)

    def __init__(self, title: str):
        super().__init__()
        self.initUI(title)

    def initUI(self, title: str):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel(title)
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Start and Stop Buttons
        self.start_stop_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start_action)
        self.start_stop_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_action)
        self.start_stop_layout.addWidget(self.stop_button)

        main_layout.addLayout(self.start_stop_layout)

        self.setLayout(main_layout)

    def start_action(self):
        self.start_button.setEnabled(False)
        self.changeStatus.emit(True)
        self.status_label.setText("Status: Running")

    def stop_action(self):
        self.start_button.setEnabled(True)
        self.changeStatus.emit(False)
        self.start_button.setChecked(False)
        self.status_label.setText("Status: Idle")

    def update_GUI(self):
        self.start_button.setChecked(False)
        self.start_button.setEnabled(True)
