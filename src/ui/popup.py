from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QListView
from PySide6.QtGui import Qt as Qtgui
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
import json
import pandas as pd
from src.ui.buffer import AccumulationBuffer

class CharacterModel(QAbstractListModel):
    def __init__(self, characters: list[dict], parent=None):
        super().__init__(parent)
        self.all_data = characters
        self.visible = characters[:]
    
    def rowCount(self, parent=QModelIndex()) -> int:
        if parent.isValid(): return 0
        return len(self.visible)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.UserRole):
        if not index.isValid() or index.row() >= len(self.visible):
            return None
        
        item = self.visible[index.row()]
        if role == Qt.ItemDataRole.DisplayRole: return f"{item["char"]}"
        if role == Qt.ItemDataRole.UserRole: return f"{item["char"]}"
        return None
    
    def filter(self, text):
        self.beginResetModel()
        q = text.lower().strip()

        if q:
            self.visible = [
                c for c in self.all_data if q in c['tags'].lower()
            ]
        else: self.visible = self.all_data[:]

        self.endResetModel()

    

class PickerPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qtgui.WindowType.Tool | Qtgui.WindowType.FramelessWindowHint | Qtgui.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(785, 480)

        self.complete_data: list[dict] = []
        with open("assets/complete_data.json", "r", encoding="utf-8") as f:
            self.complete_data = json.load(f)
        self.emoji_data = [
            item for item in self.complete_data if item["category"]=="emoji"
        ]
        self.kaomoji_data = [
            item for item in self.complete_data if item["category"]!="emoji"
        ]
        self.build_ui()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8,8,8,8)

        self.search = QLineEdit()
        self.search.setPlaceholderText("search something...")
        root.addWidget(self.search)

        self.model_emoji = CharacterModel(characters=self.emoji_data)
        self.model_kaomoji = CharacterModel(characters=self.kaomoji_data)
        self.char_view_emoji = QListView()
        self.char_view_emoji.setModel(self.model_emoji)
        self.char_view_emoji.setSpacing(2)
        self.char_view_kaomoji = QListView()
        self.char_view_kaomoji.setModel(self.model_kaomoji)
        self.char_view_kaomoji.setSpacing(2)
        char_view_layout = QHBoxLayout()
        char_view_layout.addWidget(self.char_view_emoji)
        char_view_layout.addWidget(self.char_view_kaomoji)

        root.addLayout(char_view_layout)

        self.buffer_row = AccumulationBuffer()
        root.addWidget(self.buffer_row)

        self.search.textChanged.connect(lambda: self.model_emoji.filter(self.search.text()))
        self.search.textChanged.connect(lambda: self.model_kaomoji.filter(self.search.text()))
        self.char_view_emoji.clicked.connect(self._on_emoji_clicked)
        self.char_view_kaomoji.clicked.connect(self._on_kaomoji_clicked)

        self.set_style()
    
    def _on_emoji_clicked(self, index):
        char = self.model_emoji.data(index, Qt.ItemDataRole.UserRole)
        if char:
            self.buffer_row._on_emoji_click(char)
    def _on_kaomoji_clicked(self, index):
        char = self.model_kaomoji.data(index, Qt.ItemDataRole.UserRole)
        if char:
            self.buffer_row._on_emoji_click(char)

    def set_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border-radius: 10px;
            }
            """)
        self.char_view_emoji.setStyleSheet("font-size: 25px;")
        self.char_view_emoji.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.char_view_kaomoji.setStyleSheet("font-size: 21px;")
        self.char_view_kaomoji.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.search.setStyleSheet("font-size: 20px;")


