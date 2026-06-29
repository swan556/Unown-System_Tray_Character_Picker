from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QScrollArea
from PySide6.QtGui import Qt
import json

class PickerPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(785, 440)
        self.build_ui()
    
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8,8,8,8)

        self.search = QLineEdit()
        self.search.setPlaceholderText("search something...")
        root.addWidget(self.search)

        self.scrollable_emoji_tray = QScrollArea()
        self.scrollable_emoji_tray.setMinimumHeight(320)
        self.scrollable_emoji_tray.setWidgetResizable(True)
        self.scrollable_emoji_tray.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.character_list = QWidget()
        self.scrollable_emoji_tray.setWidget(self.character_list)
        root.addWidget(self.scrollable_emoji_tray)
        self.load_emojis()

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
    def _on_emoji_click(self, new_emoji):
        cur_buffer_text = self.buffer_display.text()
        self.buffer_display.setText(cur_buffer_text+new_emoji)


    def load_emojis(self):
        kaomoji_data = {}
        filepath = "assets/emoticon_dict.json"
        with open(filepath, 'r', encoding="utf-8") as f:
            kaomoji_data = json.load(f)
        
        self.emoji_tray = QGridLayout()
        

        row = 0
        col = 0
        for index, key in enumerate(kaomoji_data):
            if index>=100: break

            kaomoji = QPushButton(f"{key}")
            kaomoji.setFixedSize(100, 50)
            kaomoji.setContentsMargins(4,4,4,4)
            kaomoji.clicked.connect(lambda checked=False, k=key: self._on_emoji_click(k))
            self.emoji_tray.addWidget(kaomoji, row, col)
            col += 1
            if col >= 7:
                col = 0
                row += 1

        self.character_list.setLayout(self.emoji_tray)