

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class StartStopWidget(QWidget):
    change_status = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.change_status.connect(self.status_changed)
        self.start_stop_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(lambda: self.change_status.emit(True))
        self.start_stop_layout.addWidget(self.start_button)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(lambda: self.change_status.emit(False))
        self.start_stop_layout.addWidget(self.stop_button)
        self.setLayout(self.start_stop_layout)

    def status_changed(self, status: bool):
        if status:
            self.start_button.setChecked(True)
        else:
            self.start_button.setChecked(False)



#class StartStopWidget():
#    pass