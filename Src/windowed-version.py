from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QComboBox, 
    QPushButton, 
    QWidget, 
    QSizePolicy,
    QMessageBox
)

from main import generate_filename, generate_image, get_font_paths

from constants import VALID_COLORS_BY_FONT

from theme import dark_theme

class ImageGenerator:
    def generate_and_display_image(self, text, font, color):
        try:
            if not text.strip():
                QMessageBox.critical(None, "Error", "Input text is empty. Please enter some text.")
                return

            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)

            img_path, error_message_generate = generate_image(text, filename, font_paths)

            if error_message_generate:
                QMessageBox.critical(None, "Error", f"Error: {error_message_generate}")
            else:
                QMessageBox.information(None, "Success", f"Image successfully generated and saved as: {img_path}")

        except FileNotFoundError as e:
            error_message_generate = f"Font file not found: {e.filename}"
            QMessageBox.critical(None, "Error", error_message_generate)
        except Exception as e:
            error_message_generate = f"An error occurred: {e}"
            QMessageBox.critical(None, "Error", error_message_generate)

class MetalSlugFontReborn(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MetalSlugFontReborn")

        icon_path = 'Assets/Icons/Raubtier.ico'
        self.setWindowIcon(QIcon(icon_path))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        text_label = QLabel("Text to Generate:")
        layout.addWidget(text_label)
        self.text_entry = QLineEdit()
        self.text_entry.setMinimumWidth(600)
        self.text_entry.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.text_entry)

        font_label = QLabel("Select Font:")
        layout.addWidget(font_label)
        self.font_combobox = QComboBox()
        self.font_combobox.addItems(["1", "2", "3", "4", "5"])
        self.font_combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.font_combobox)

        color_label = QLabel("Select Color:")
        layout.addWidget(color_label)
        self.color_combobox = QComboBox()
        self.color_combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.color_combobox)

        generate_button = QPushButton("Generate and Save Image", self)
        generate_button.clicked.connect(self.generate_and_display_image)
        generate_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(generate_button)

        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(self.text_entry.clear)
        clear_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(clear_button)

        self.color_combobox.setEnabled(False)
        self.font_combobox.currentIndexChanged.connect(self.on_font_change)

        self.on_font_change()

        self.setStyleSheet(dark_theme)

    def on_font_change(self):
        font = int(self.font_combobox.currentText())
        valid_colors = VALID_COLORS_BY_FONT.get(font, [])
        self.color_combobox.clear()
        self.color_combobox.addItems(valid_colors)
        self.color_combobox.setEnabled(bool(valid_colors))
        if valid_colors:
            self.color_combobox.setCurrentIndex(0)

    def generate_and_display_image(self):
        text = self.text_entry.text()
        font = int(self.font_combobox.currentText())
        color = self.color_combobox.currentText()

        ImageGenerator.generate_and_display_image(text, font, color)

def main():
    app = QApplication([])
    window = MetalSlugFontReborn()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
