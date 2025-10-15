import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class CodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Номерная панель
        self.number_bar = QTextEdit()
        self.number_bar.setReadOnly(True)
        self.number_bar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.number_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.number_bar.setFixedWidth(40)
        
        # Редактор кода
        self.text_edit = QTextEdit()
        
        layout.addWidget(self.number_bar)
        layout.addWidget(self.text_edit)
        
        self.update_line_numbers()
        self.text_edit.textChanged.connect(self.update_line_numbers)
        self.text_edit.verticalScrollBar().valueChanged.connect(
            self.number_bar.verticalScrollBar().setValue)
    
    def update_line_numbers(self):
        block_count = self.text_edit.document().blockCount()
        numbers = '\n'.join(str(i) for i in range(1, block_count + 1))
        self.number_bar.setPlainText(numbers)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IDE Simulator")
        self.setFixedSize(1000, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Левая панель - IDE
        self.ide_container = QWidget()
        ide_layout = QVBoxLayout(self.ide_container)
        ide_layout.setContentsMargins(20, 20, 20, 20)
        ide_layout.setSpacing(10)
        
        ide_header = QLabel("IDE")
        ide_header.setAlignment(Qt.AlignCenter)
        
        self.code_editor = CodeEditor()
        
        ide_layout.addWidget(ide_header)
        ide_layout.addWidget(self.code_editor)
        
        # Правая панель - Настройки
        self.settup_container = QWidget()
        settup_layout = QVBoxLayout(self.settup_container)
        settup_layout.setContentsMargins(20, 20, 20, 20)
        settup_layout.setSpacing(10)
        
        settup_header = QLabel("Settup")
        settup_header.setAlignment(Qt.AlignCenter)
        
        # Верхние кнопки
        top_info_widget = QWidget()
        top_info_layout = QVBoxLayout(top_info_widget)
        top_info_layout.setSpacing(10)
        
        self.run_btn = self.create_button("Run Script", "▶")
        self.save_btn = self.create_button("Save", "💾")
        self.show_btn = self.create_button("Show headless", "👁️")
        
        top_info_layout.addWidget(self.run_btn)
        top_info_layout.addWidget(self.save_btn)
        top_info_layout.addWidget(self.show_btn)
        
        # Нижние настройки
        bottom_info_widget = QWidget()
        bottom_info_layout = QVBoxLayout(bottom_info_widget)
        
        # Toggle для автосохранения
        self.auto_save_toggle = QCheckBox("Auto Save")
        
        # Поле для горячих клавиш
        shortcut_widget = QWidget()
        shortcut_layout = QHBoxLayout(shortcut_widget)
        self.shortcut_input = QLineEdit("ctrl+c")
        self.shortcut_input.setReadOnly(True)
        self.registrate_btn = QPushButton("Registrate")
        shortcut_layout.addWidget(self.shortcut_input)
        shortcut_layout.addWidget(self.registrate_btn)
        
        # Поле пути сохранения
        path_widget = QWidget()
        path_layout = QHBoxLayout(path_widget)
        self.path_input = QLineEdit("C:/Documents/scripts/script.botc")
        self.path_input.setReadOnly(True)
        self.select_path_btn = QPushButton("📁")
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.select_path_btn)
        
        bottom_info_layout.addWidget(self.auto_save_toggle)
        bottom_info_layout.addWidget(shortcut_widget)
        bottom_info_layout.addWidget(path_widget)
        
        settup_layout.addWidget(settup_header)
        settup_layout.addWidget(top_info_widget)
        settup_layout.addStretch()
        settup_layout.addWidget(bottom_info_widget)
        
        # Добавляем обе панели в главный layout
        main_layout.addWidget(self.ide_container)
        main_layout.addWidget(self.settup_container)
        
        self.apply_styles()
        self.connect_signals()
    
    def create_button(self, text, icon):
        btn = QPushButton(f"{icon} {text}")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return btn
    
    def connect_signals(self):
        self.run_btn.clicked.connect(self.run_script)
        self.save_btn.clicked.connect(self.save_file)
        self.show_btn.clicked.connect(self.toggle_headless)
        self.registrate_btn.clicked.connect(self.registrate_shortcut)
        self.select_path_btn.clicked.connect(self.select_path)
    
    def run_script(self):
        print("Running script...")
    
    def save_file(self):
        print("Saving file...")
    
    def toggle_headless(self):
        print("Toggling headless mode...")
    
    def registrate_shortcut(self):
        print("Registering shortcut...")
    
    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Save Path")
        if path:
            self.path_input.setText(path)
    
    def apply_styles(self):
        self.setStyleSheet("""
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Courier New', Courier, monospace;
            }
            QMainWindow {
                background-color: #2F2F2F;
            }
            QWidget {
                background-color: transparent;
            }
            /* Стили для IDE контейнера */
            #ide_container {
                background-color: #282828;
                border-radius: 0px;
            }
            #ide_container QLabel {
                padding: 5px;
                border-radius: 10px;
                border: 2px solid #F4F4F4;
                color: #F4F4F4;
                font-size: 16px;
                font-weight: bold;
            }
            /* Стили для номерной панели */
            QTextEdit#number_bar {
                background-color: #282828;
                color: #F87E7B;
                font-weight: bold;
                border: none;
                border-right: 1px solid #444;
                padding: 10px 5px;
            }
            /* Стили для редактора кода */
            QTextEdit#text_edit {
                background-color: #282828;
                color: #F4F4F4;
                font-weight: bold;
                border: none;
                padding: 10px;
                selection-background-color: #3F3F3F;
            }
            /* Стили для контейнера настроек */
            #settup_container {
                background-color: #2F2F2F;
                border-radius: 0px;
            }
            #settup_container QLabel {
                padding: 5px;
                border-radius: 10px;
                border: 2px solid #F4F4F4;
                color: #F4F4F4;
                font-size: 16px;
                font-weight: bold;
            }
            /* Стили для кнопок */
            QPushButton {
                background-color: #F4F4F4;
                color: #282828;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E4E4E4;
            }
            QPushButton:pressed {
                background-color: #D4D4D4;
            }
            /* Стили для полей ввода */
            QLineEdit {
                background-color: transparent;
                border: none;
                color: #F4F4F4;
                font-weight: bold;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:disabled {
                color: #888;
            }
            /* Стили для контейнеров полей ввода */
            QWidget#shortcut_widget, QWidget#path_widget {
                border: 2px solid #F4F4F4;
                border-radius: 16px;
                padding: 5px;
            }
            /* Стили для чекбокса */
            QCheckBox {
                color: #F4F4F4;
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #F4F4F4;
            }
            QCheckBox::indicator:checked {
                background-color: #F87E7B;
            }
        """)
        
        # Устанавливаем object names для стилизации
        self.ide_container.setObjectName("ide_container")
        self.settup_container.setObjectName("settup_container")
        self.code_editor.number_bar.setObjectName("number_bar")
        self.code_editor.text_edit.setObjectName("text_edit")
        
        shortcut_widget = self.registrate_btn.parent()
        path_widget = self.select_path_btn.parent()
        shortcut_widget.setObjectName("shortcut_widget")
        path_widget.setObjectName("path_widget")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())