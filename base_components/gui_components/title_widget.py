from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

class TitleWidget(QWidget):
    change_status = pyqtSignal(bool)
    def __init__(self, title: str):
        super().__init__()
        self.change_status.connect(self.change_status_label)
        self.title_layout = QVBoxLayout()
        self.title = QLabel(title)
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.title)
        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.status_label)
        self.setLayout(self.title_layout)

    def change_status_label(self, status: bool):
        if status:
            self.status_label.setText("Status: Running")
        else:
            self.status_label.setText("Status: Idle")



    