from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QListView
from PySide6.QtGui import Qt as Qtgui
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
import json
import pandas as pd

class CharacterModel(QAbstractListModel):
    def __init__(self, characters: list[dict], parent=None):
        super().__init__(parent)
        self.all_data = characters
        self.visible = characters[:]
    
    def rowCount(self, parent=QModelIndex()) -> int:
        if parent.isValid(): return 0
        return len(self.visible)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self.visible):
            return None
        
        item = self.visible[index.row()]
        if role == Qt.ItemDataRole.DisplayRole: return f"{item["char"]} {item["tags"]}"
        if role == Qt.ItemDataRole.UserRole: return f"{item["char"]}"
        return None
    
    def filter(self, text):
        self.beginResetModel()
        q = text.lower().strip()

        if q:
            self.visible = [
                c for c in self.all_data if q in c['tags']
            ]
        else: self.visible = self.all_data[:]

        self.endResetModel()

    

class PickerPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qtgui.WindowType.Tool | Qtgui.WindowType.FramelessWindowHint | Qtgui.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(785, 440)
        self.complete_data: list[dict] = []
        with open("assets/complete_data.json", "r", encoding="utf-8") as f:
            self.complete_data = json.load(f)

        self.build_ui()
            

    
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8,8,8,8)

        self.search = QLineEdit()
        self.search.setPlaceholderText("search something...")
        root.addWidget(self.search)

        self.model = CharacterModel(characters=self.complete_data)
        self.char_view = QListView()
        self.char_view.setModel(self.model)
        self.char_view.setSpacing(2)
        root.addWidget(self.char_view)
        # self.load_emojis()

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
        self.model.filter(str)
    def _on_copy(self, str):
        print(f"copy triggered: {str}")
    def _on_emoji_click(self, new_emoji):
        cur_buffer_text = self.buffer_display.text()
        self.buffer_display.setText(cur_buffer_text+new_emoji)


    def load_emojis(self):
        kaomoji_data = {}
        complete_data = pd.read_csv('assets/complete_data.csv')
        data_len = len(complete_data)
        self.emoji_tray = QGridLayout()
        

        row = 0
        col = 0
        for i in range(data_len):
            key = complete_data.iloc[i]["char"]
            kaomoji = QPushButton(f"{key}")
            kaomoji.setFixedSize(100, 50)
            kaomoji.setContentsMargins(4,4,4,4)
            kaomoji.clicked.connect(lambda checked=False, k=key: self._on_emoji_click(k))
            self.emoji_tray.addWidget(kaomoji, row, col)
            col += 1
            if col >= 7:
                col = 0
                row += 1

        # self.character_list.setLayout(self.emoji_tray)