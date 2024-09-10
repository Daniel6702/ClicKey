from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QCursor, QGuiApplication
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QWidget, QPushButton, QHBoxLayout

class PixelDetectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_pixel_color)
        self.timer.start(100)  # Refresh every 100 milliseconds
        
        self.locked = False
        self.lock_countdown = 5
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)

    def initUI(self):
        layout = QVBoxLayout()

        # Display for color preview
        temp_V = QVBoxLayout()
        self.color_display = QLabel()
        self.color_display.setFixedSize(150, 150)
        self.color_display.setStyleSheet("background-color: #FFFFFF; border: 2px solid black;")
        temp_V.addWidget(self.color_display, alignment=Qt.AlignCenter)

        # Countdown label
        self.countdown_label = QLabel("Countdown: 5s")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        temp_V.addWidget(self.countdown_label)

        # Lock/Unlock button
        self.lock_button = QPushButton("Lock Color")
        self.lock_button.clicked.connect(self.toggle_lock)
        temp_V.addWidget(self.lock_button, alignment=Qt.AlignCenter)


        # Grid Layout for color codes
        grid_layout = QGridLayout()

        # Create labels and fields for RGB, HEX, HSV, HSL, CMYK
        self.create_color_field(grid_layout, 'RGB', 0)
        self.create_color_field(grid_layout, 'HEX', 1)
        self.create_color_field(grid_layout, 'HSV', 2)
        self.create_color_field(grid_layout, 'HSL', 3)
        self.create_color_field(grid_layout, 'CMYK', 4)

        temp_H = QHBoxLayout()
        temp_H.addLayout(grid_layout)
        temp_H.addLayout(temp_V)
        layout.addLayout(temp_H)
        
        self.setLayout(layout)

    def create_color_field(self, layout, label_text, row):
        label = QLabel(f"{label_text}:")
        label.setAlignment(Qt.AlignRight)
        field = QLineEdit()
        field.setReadOnly(True)  # Make it non-editable
        layout.addWidget(label, row, 0)
        layout.addWidget(field, row, 1)
        setattr(self, f"{label_text.lower()}_field", field)

    def get_pixel_color(self):
        if self.locked:
            return

        cursor_pos = QCursor.pos()  # Get current cursor position
        screen = QGuiApplication.primaryScreen()  # Get the screen object
        if screen:
            pixmap = screen.grabWindow(0, cursor_pos.x(), cursor_pos.y(), 1, 1)  # Capture 1x1 pixel at cursor
            image = pixmap.toImage()
            color = image.pixel(0, 0)
            q_color = QColor(color)

            # Update color display
            self.color_display.setStyleSheet(f"background-color: {q_color.name()}; border: 2px solid black;")

            # Update RGB and HEX
            self.rgb_field.setText(f"({q_color.red()}, {q_color.green()}, {q_color.blue()})")
            self.hex_field.setText(f"{q_color.name().upper()}")

            # Convert and Update HSV
            hsv = q_color.getHsv()
            hue, sat, val = hsv[0], hsv[1] / 255 * 100, hsv[2] / 255 * 100
            self.hsv_field.setText(f"{hue+1}°, {sat:.1f}%, {val:.1f}%")

            # Convert and Update HSL
            hsl = q_color.getHsl()
            hue, sat, light = hsl[0], hsl[1] / 255 * 100, hsl[2] / 255 * 100
            self.hsl_field.setText(f"{hue+1}°, {sat:.1f}%, {light:.1f}%")

            # Convert and Update CMYK
            cmyk = q_color.getCmyk()
            cyan = cmyk[0] / 255 * 100
            magenta = cmyk[1] / 255 * 100
            yellow = cmyk[2] / 255 * 100
            black = cmyk[3] / 255 * 100
            self.cmyk_field.setText(f"{cyan:.1f}%, {magenta:.1f}%, {yellow:.1f}%, {black:.1f}%")

    def toggle_lock(self):
        if self.locked:
            self.unlock_color()
        else:
            self.start_countdown()

    def start_countdown(self):
        self.lock_countdown = 5
        self.countdown_label.setText(f"Countdown: {self.lock_countdown}s")
        self.countdown_timer.start(1000)  # Update every 1 second
        self.lock_button.setEnabled(False)

    def update_countdown(self):
        self.lock_countdown -= 1
        self.countdown_label.setText(f"Countdown: {self.lock_countdown}s")

        if self.lock_countdown == 0:
            self.lock_color()

    def lock_color(self):
        self.locked = True
        self.countdown_timer.stop()
        self.countdown_label.setText("Color locked!")
        self.lock_button.setText("Unlock Color")
        self.lock_button.setEnabled(True)

    def unlock_color(self):
        self.locked = False
        self.countdown_label.setText("Countdown: 5s")
        self.lock_button.setText("Lock Color")

