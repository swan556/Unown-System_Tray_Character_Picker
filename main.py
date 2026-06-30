import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.ui.popup import PickerPopup
import qdarktheme

os.environ["QT_LOGGING_RULES"] = "qt.text.font.*=false"

class UnownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unown")
        self.setFixedSize(785, 480)
        self.setWindowIcon(QIcon("./assets/icon.png"))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint
        )
        self.setCentralWidget(PickerPopup())

def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    window = UnownApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
