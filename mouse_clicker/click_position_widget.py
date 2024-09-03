from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout, QGroupBox
import pyautogui
from PyQt5.QtCore import pyqtSignal, QTimer

class PositionComboWidget(QWidget):
    position_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.combo = QComboBox(self)
        self.combo.addItems(["follow mouse", "center", "coordinates", "random position", "rectangle"])
        self.combo.currentIndexChanged.connect(self.position_changed)
        
        layout.addWidget(QLabel("Click Position:"))
        layout.addWidget(self.combo)
        self.setLayout(layout)
    
    def currentText(self):
        return self.combo.currentText()
    
    def currentIndex(self):
        return self.combo.currentIndex()
    
    def setIndexChangedCallback(self, callback):
        self.combo.currentIndexChanged.connect(callback)

class CoordinateInputWidget(QWidget):
    coordinates_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        
        v_layout_left = QVBoxLayout()
        v_layout_right = QVBoxLayout()
        
        self.x_input = QLineEdit(self)
        self.x_input.textChanged.connect(
            lambda: self.coordinates_changed.emit({'x_pos': int(self.x_input.text())})
        )
        self.y_input = QLineEdit(self)
        self.y_input.textChanged.connect(
            lambda: self.coordinates_changed.emit({'y_pos': int(self.y_input.text())})
        )
        
        x_label = QLabel("X Coordinate:")
        y_label = QLabel("Y Coordinate:")
        
        v_layout_left.addWidget(x_label)
        v_layout_left.addWidget(y_label)
        v_layout_right.addWidget(self.x_input)
        v_layout_right.addWidget(self.y_input)
        
        layout.addLayout(v_layout_left)
        layout.addLayout(v_layout_right)
        
        self.setLayout(layout)

class RectangleInputWidget(QWidget):
    rectangle_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.top_left_layout = QHBoxLayout()
        self.bottom_right_layout = QHBoxLayout()
        
        self.top_left_x = QLineEdit(self)
        self.top_left_x.textChanged.connect(
            lambda: self.rectangle_changed.emit({'top_left_x_pos': int(self.top_left_x.text())})
        )
        self.top_left_y = QLineEdit(self)
        self.top_left_y.textChanged.connect(
            lambda: self.rectangle_changed.emit({'top_left_y_pos': int(self.top_left_y.text())})
        )
        top_left_x_label = QLabel("Top Left X:")
        top_left_y_label = QLabel("Top Left Y:")
        
        self.top_left_layout.addWidget(top_left_x_label)
        self.top_left_layout.addWidget(self.top_left_x)
        self.top_left_layout.addWidget(top_left_y_label)
        self.top_left_layout.addWidget(self.top_left_y)
        
        self.bottom_right_x = QLineEdit(self)
        self.bottom_right_x.textChanged.connect(
            lambda: self.rectangle_changed.emit({'bottom_right_x_pos': int(self.bottom_right_x.text())})
        )
        self.bottom_right_y = QLineEdit(self)
        self.bottom_right_y.textChanged.connect(
            lambda: self.rectangle_changed.emit({'bottom_right_y_pos': int(self.bottom_right_y.text())})
        )
        bottom_right_x_label = QLabel("Bottom Right X:")
        bottom_right_y_label = QLabel("Bottom Right Y:")
        
        self.bottom_right_layout.addWidget(bottom_right_x_label)
        self.bottom_right_layout.addWidget(self.bottom_right_x)
        self.bottom_right_layout.addWidget(bottom_right_y_label)
        self.bottom_right_layout.addWidget(self.bottom_right_y)
        
        layout.addLayout(self.top_left_layout)
        layout.addLayout(self.bottom_right_layout)
        
        self.setLayout(layout)

class MousePositionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Current Mouse Position:\n (X: 0, Y: 0)")
        self.label.setStyleSheet("font-size: 12px; color: #555; margin-left: 45px;")
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_mouse_position)
        self.timer.start(100)
    
    def update_mouse_position(self):
        x, y = pyautogui.position()
        self.label.setText(f"Current Mouse Position:\n (X: {x}, Y: {y})")

class ClickPositionWidget(QGroupBox):
    change_settings = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__("Click Position")
        self.setMinimumWidth(505)
        
        position_layout = QVBoxLayout()

        self.mouse_position_widget = MousePositionWidget()
        self.position_combo_widget = PositionComboWidget()
        self.coord_input_widget = CoordinateInputWidget()
        self.rectangle_input_widget = RectangleInputWidget()

        # Connecting signals
        self.position_combo_widget.position_changed.connect(self.update_position_fields)
        self.coord_input_widget.coordinates_changed.connect(self.change_settings.emit)
        self.rectangle_input_widget.rectangle_changed.connect(self.change_settings.emit)

        # Adding components to layout
        temp_h = QHBoxLayout()
        temp_h.addWidget(self.position_combo_widget)
        temp_h.addWidget(self.mouse_position_widget)
        position_layout.addLayout(temp_h)
        position_layout.addWidget(self.coord_input_widget)
        position_layout.addWidget(self.rectangle_input_widget)
        
        self.setLayout(position_layout)
        self.update_position_fields(0)
    
    def update_position_fields(self, index):
        self.change_settings.emit({'position_mode': self.position_combo_widget.currentText().replace(' ', '_')})
        self.coord_input_widget.setVisible(False)
        self.rectangle_input_widget.setVisible(False)
        if index == 2:  
            self.coord_input_widget.setVisible(True)            
        elif index == 4:  
            self.rectangle_input_widget.setVisible(True)
