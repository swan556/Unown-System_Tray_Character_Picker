import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from src.ui.popup import PickerPopup
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "assets"

os.environ["QT_LOGGING_RULES"] = (
    "qt.text.font.warning=false;"
    "qt.text.font.*=false;"
    "qt.*=false;"
)

class UnownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unown")
        self.setFixedWidth(785)
        self.setWindowIcon(QIcon(str(ASSETS_DIR / "icon.png")))
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border-radius: 2px;
                color: white;
            }
            """)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint
        )
        self.setCentralWidget(PickerPopup())

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Noto Sans"))
    # qdarktheme.setup_theme("dark")
    window = UnownApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
