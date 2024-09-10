from PyQt5.QtWidgets import  QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from random import randint

from modules.color_tool.color_picker.colorPickerWidget import ColorPickerWidget

from base_components.base_gui import BaseAutoActionGUI

from modules.color_tool.pixel_color_detector import PixelDetectorWidget

class ColorGUI(BaseAutoActionGUI):
    def __init__(self):
        super().__init__("Color Tools")
        self.profiles = []
        self.initColorToolUI()

    def initColorToolUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        self.title_widget.status_label.setText("")
        main_layout.addWidget(self.title_widget)

        pixel_detector_group = QGroupBox("Pixel Detector")
        pixel_detector_layout = QVBoxLayout()
        self.pixel_detector_widget = PixelDetectorWidget()
        pixel_detector_layout.addWidget(self.pixel_detector_widget)
        pixel_detector_group.setLayout(pixel_detector_layout)
        main_layout.addWidget(pixel_detector_group)

        color_picker_group = QGroupBox("Color Picker")
        color_picker_layout = QVBoxLayout()
        self.color_picker_widget = ColorPickerWidget(color=QColor(randint(0, 255), randint(0, 255), randint(0, 255)), orientation='horizontal')
        color_picker_layout.addWidget(self.color_picker_widget)
        color_picker_group.setLayout(color_picker_layout)
        main_layout.addWidget(color_picker_group)

        self.setLayout(main_layout)


