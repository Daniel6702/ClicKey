from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QSpinBox, QLineEdit, QApplication, QLabel, QPushButton, QSizePolicy, QSlider, QSizePolicy
import colorsys

class ColorEditorWidget(QWidget):
    colorChanged = pyqtSignal(QColor)

    def __init__(self, color, orientation):
        super().__init__()
        self.__current_color = color
        self.clipboard = QApplication.clipboard()
        self.__initUi(color, orientation)

    def __initUi(self, color, orientation):
        # Color Preview Block
        self.__colorPreviewWithGraphics = QLabel()
        #self.__colorPreviewWithGraphics.setFixedSize(200, 100)
        self.setColorPreviewWithGraphics()

        # HEX input with Copy Button
        self.__hexLineEdit = QLineEdit()
        self.__hexLineEdit.editingFinished.connect(self.__hexColorChanged)
        self.__copyButton = QPushButton()
        self.__copyButton.setIcon(QIcon('color_tool\color_picker\style\COPY_ICON.png'))
        self.__copyButton.setStyleSheet("background-color: transparent")
        self.__copyButton.setFixedSize(25, 25)
        self.__copyButton.clicked.connect(self.__copyHexToClipboard)

        # RGB input
        self.__rgbLineEdit = QLineEdit()
        self.__rgbLineEdit.setPlaceholderText("R, G, B")
        self.__rgbLineEdit.editingFinished.connect(self.__rgbColorChanged)

        # CMYK input
        self.__cmykLineEdit = QLineEdit()
        self.__cmykLineEdit.setPlaceholderText("C, M, Y, K")
        self.__cmykLineEdit.editingFinished.connect(self.__cmykColorChanged)

        # HSV input
        self.__hsvLineEdit = QLineEdit()
        self.__hsvLineEdit.setPlaceholderText("H, S, V")
        self.__hsvLineEdit.editingFinished.connect(self.__hsvColorChanged)

        # HSL input
        self.__hslLineEdit = QLineEdit()
        self.__hslLineEdit.setPlaceholderText("H, S, L")
        self.__hslLineEdit.editingFinished.connect(self.__hslColorChanged)

        # Layout for HEX + Copy button
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(self.__hexLineEdit)
        hex_layout.addWidget(self.__copyButton)

        # Form Layout for color codes
        form_layout = QFormLayout()
        form_layout.addRow('HEX', hex_layout)
        form_layout.addRow('RGB', self.__rgbLineEdit)
        form_layout.addRow('CMYK', self.__cmykLineEdit)
        form_layout.addRow('HSV', self.__hsvLineEdit)
        form_layout.addRow('HSL', self.__hslLineEdit)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Main Layout
        layout = QVBoxLayout()

        layout.addWidget(self.__colorPreviewWithGraphics)
        layout.addLayout(form_layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.setCurrentColor(color)

    def setColorPreviewWithGraphics(self):
        self.__colorPreviewWithGraphics.setStyleSheet(f'background-color: {self.__current_color.name()}; border: 1px solid black')

    def setCurrentColor(self, color):
        self.__current_color = color
        self.setColorPreviewWithGraphics()
        self.__updateColorFields()

    def __updateColorFields(self):
        # Update HEX
        self.__hexLineEdit.setText(self.__current_color.name())

        # Update RGB field
        r, g, b = self.__current_color.red(), self.__current_color.green(), self.__current_color.blue()
        self.__rgbLineEdit.setText(f"{r}, {g}, {b}")

        # Update CMYK field
        c, m, y, k = self.__rgb_to_cmyk(r, g, b)
        self.__cmykLineEdit.setText(f"{c:.0f}, {m:.0f}, {y:.0f}, {k:.0f}")

        # Update HSV field
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self.__hsvLineEdit.setText(f"{h*360:.0f}, {s*100:.0f}, {v*100:.0f}")

        # Update HSL field
        h, s, l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        self.__hslLineEdit.setText(f"{h*360:.0f}, {s*100:.0f}, {l*100:.0f}")

    def __rgb_to_cmyk(self, r, g, b):
        """ Converts RGB to CMYK. """
        if (r == 0) and (g == 0) and (b == 0):
            return 0, 0, 0, 100
        c = 1 - r / 255.
        m = 1 - g / 255.
        y = 1 - b / 255.
        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy
        return c * 100, m * 100, y * 100, k * 100

    # Slot: Handle HEX input changes
    def __hexColorChanged(self):
        hex_value = self.__hexLineEdit.text().strip()
        if QColor.isValidColor(hex_value):
            self.__current_color.setNamedColor(hex_value)
            self.__procColorChanged()

    # Slot: Handle RGB input changes
    def __rgbColorChanged(self):
        print("RGB changed")
        try:
            rgb_values = list(map(int, self.__rgbLineEdit.text().split(',')))
            if len(rgb_values) == 3 and all(0 <= v <= 255 for v in rgb_values):
                self.__current_color.setRgb(*rgb_values)
                self.__procColorChanged()
        except ValueError:
            pass

    # Slot: Handle CMYK input changes
    def __cmykColorChanged(self):
        print("CMYK changed")
        try:
            cmyk_values = list(map(float, self.__cmykLineEdit.text().split(',')))
            if len(cmyk_values) == 4 and all(0 <= v <= 100 for v in cmyk_values):
                c, m, y, k = [v / 100 for v in cmyk_values]
                r, g, b = self.__cmyk_to_rgb(c, m, y, k)
                self.__current_color.setRgb(r, g, b)
                self.__procColorChanged()
        except ValueError:
            pass

    def __cmyk_to_rgb(self, c, m, y, k):
        print(c, m, y, k)
        """ Converts CMYK to RGB. """
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return round(r), round(g), round(b)

    # Slot: Handle HSV input changes
    def __hsvColorChanged(self):
        print("HSV changed")
        try:
            hsv_values = list(map(float, self.__hsvLineEdit.text().split(',')))
            if len(hsv_values) == 3 and 0 <= hsv_values[0] <= 360 and 0 <= hsv_values[1] <= 100 and 0 <= hsv_values[2] <= 100:
                h, s, v = hsv_values[0] / 360, hsv_values[1] / 100, hsv_values[2] / 100
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                self.__current_color.setRgb(round(r * 255), round(g * 255), round(b * 255))
                self.__procColorChanged()
        except ValueError:
            pass

    # Slot: Handle HSL input changes
    def __hslColorChanged(self):
        print("HSL changed")
        try:
            hsl_values = list(map(float, self.__hslLineEdit.text().split(',')))
            if len(hsl_values) == 3 and 0 <= hsl_values[0] <= 360 and 0 <= hsl_values[1] <= 100 and 0 <= hsl_values[2] <= 100:
                h, l, s = hsl_values[0] / 360, hsl_values[1] / 100, hsl_values[2] / 100
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                self.__current_color.setRgb(round(r * 255), round(g * 255), round(b * 255))
                self.__procColorChanged()
        except ValueError:
            pass

    def __procColorChanged(self):
        self.setColorPreviewWithGraphics()
        self.__updateColorFields()
        self.colorChanged.emit(self.__current_color)

    def __copyHexToClipboard(self):
        self.clipboard.setText(self.__hexLineEdit.text())

    def getCurrentColor(self):
        return self.__current_color


