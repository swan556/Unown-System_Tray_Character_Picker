from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import Qt

class PickerPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(320, 440)
        self.build_ui()
    
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8,8,8,8)

        self.search = QLineEdit()
        self.search.setPlaceholderText("search something...")
        root.addWidget(self.search)

        self.character_list = QWidget()
        self.character_list.setMinimumHeight(320)
        root.addWidget(self.character_list)

        buffer_row = QHBoxLayout()
        self.buffer_display = QLabel("")
        self.buffer_display.setMinimumWidth(160)

        self.copy_button = QPushButton("copy")
        self.clear_button = QPushButton("X")
        self.clear_button.setFixedWidth(28)

        buffer_row.addWidget(self.buffer_display)
        buffer_row.addStretch()

        buffer_row.addWidget(self.copy_button)
        buffer_row.addWidget(self.clear_button)

        root.addLayout(buffer_row)

        self.search.textChanged.connect(lambda str: self._on_search(str))
        self.clear_button.clicked.connect(lambda: self.buffer_display.setText(""))
        self.copy_button.clicked.connect(lambda: self._on_copy(self.search.text()))

    def _on_search(self, str):
        print(str)
    def _on_copy(self, str):
        print(f"copy triggered: {str}")
