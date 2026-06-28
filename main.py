import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from src.ui.popup import PickerPopup

class UnownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unown")
        self.setFixedSize(320, 480)

        self.setCentralWidget(PickerPopup())

def main():
    app = QApplication(sys.argv)
    window = UnownApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
