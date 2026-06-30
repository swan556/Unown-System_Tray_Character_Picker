from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication
from PySide6.QtCore import Signal

class AccumulationBuffer(QWidget):
    changed = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setStyleSheet("")
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border-radius: 16px;
                font-size: 25px;
            }
            """)
        self.chars: list[str] = []
        self.build_ui()

    def build_ui(self):
        buffer_row = QHBoxLayout()
        self.setLayout(buffer_row)

        self.buffer_display = QLabel("")
        self.buffer_display.setMinimumWidth(400)
        self.buffer_display.setContentsMargins(4, 0, 0, 0)

        self.copy_button = QPushButton("copy")
        self.clear_button = QPushButton("X")
        self.clear_button.setFixedWidth(28)

        buffer_row.addWidget(self.buffer_display)
        buffer_row.addStretch()
        buffer_row.addWidget(self.copy_button)
        buffer_row.addWidget(self.clear_button)

        self.add_connections()
    
    def add_connections(self):
        self.clear_button.clicked.connect(lambda: self._on_clear())
        self.copy_button.clicked.connect(lambda: self._on_copy())

    def _on_clear(self):
        self.buffer_display.setText("")
        self.chars = []
        self.changed.emit("")
        
    def _on_copy(self):
        if self.chars:
            print(self.chars)
            QApplication.clipboard().setText("".join(self.chars))
            self.chars.clear()

    def _on_emoji_click(self, new_char):
        self.chars.append(new_char)
        self.buffer_display.setText("".join(self.chars))
        self.changed.emit("".join(self.chars))