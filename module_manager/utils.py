from PyQt5.QtWidgets import QApplication

def apply_stylesheet(app: QApplication, path: str) -> None:
    with open(path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)