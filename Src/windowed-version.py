# Import necessary libraries
import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QWidget, QRadioButton, QMessageBox
from PyQt6.QtGui import QPalette, QColor, QIcon

# Prevent the generation of .pyc (Python bytecode) files
sys.dont_write_bytecode = True

# Import necessary functions from the main module
from main import generate_filename, generate_image, get_font_paths

# Import necessary constants from the constants module
from constants import VALID_COLORS_BY_FONT

class ImageGenerator:
    @staticmethod
    def generate_and_display_image(text, font, color):
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

class ThemeToggle:
    @staticmethod
    def toggle_theme(is_dark_mode):
        palette = QPalette()
        if is_dark_mode:
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        return palette

class MetalSlugFontReborn(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MetalSlugFontReborn")

        # Set the window icon
        icon_path = os.path.join(os.getcwd(), 'Assets', 'Icon', 'Raven.ico')
        self.setWindowIcon(QIcon(icon_path))

        # Create central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Text input
        text_label = QLabel("Text to Generate:")
        layout.addWidget(text_label)
        self.text_entry = QLineEdit()
        layout.addWidget(self.text_entry)

        # Font selection
        font_label = QLabel("Select Font:")
        layout.addWidget(font_label)
        self.font_combobox = QComboBox()
        self.font_combobox.addItems(["1", "2", "3", "4", "5"])
        layout.addWidget(self.font_combobox)

        # Color selection
        color_label = QLabel("Select Color:")
        layout.addWidget(color_label)
        self.color_combobox = QComboBox()
        layout.addWidget(self.color_combobox)

        # Theme toggle buttons
        theme_label = QLabel("Select Theme:")
        layout.addWidget(theme_label)
        self.light_mode_button = QRadioButton("Light Mode")
        self.dark_mode_button = QRadioButton("Dark Mode")
        self.light_mode_button.setChecked(True)
        self.light_mode_button.toggled.connect(self.toggle_theme)
        self.dark_mode_button.toggled.connect(self.toggle_theme)
        layout.addWidget(self.light_mode_button)
        layout.addWidget(self.dark_mode_button)

        # Generate button
        generate_button = QPushButton("Generate and Save Image", self)
        generate_button.clicked.connect(self.generate_and_display_image)
        layout.addWidget(generate_button)

        # Clear button
        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(self.text_entry.clear)
        layout.addWidget(clear_button)

        # Set up default values
        self.color_combobox.setEnabled(False)
        self.font_combobox.currentIndexChanged.connect(self.on_font_change)

        # Initialize the UI
        self.on_font_change()

    def on_font_change(self):
        font = int(self.font_combobox.currentText())
        valid_colors = VALID_COLORS_BY_FONT.get(font, [])
        self.color_combobox.clear()
        self.color_combobox.addItems(valid_colors)
        self.color_combobox.setEnabled(bool(valid_colors))
        if valid_colors:
            self.color_combobox.setCurrentIndex(0)

    def toggle_theme(self):
        is_dark_mode = self.dark_mode_button.isChecked()
        palette = ThemeToggle.toggle_theme(is_dark_mode)
        self.setPalette(palette)

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
