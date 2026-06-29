import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from src.ui.popup import PickerPopup

os.environ["QT_LOGGING_RULES"] = "qt.text.font.*=false"

class UnownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unown")
        self.setFixedSize(785, 480)
        self.setWindowIcon(QIcon("./assets/icon.png"))

        self.setCentralWidget(PickerPopup())

def main():
    app = QApplication(sys.argv)
    window = UnownApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
