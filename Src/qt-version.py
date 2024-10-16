from PIL import Image
from time import time
from pathlib import Path
from PySide2.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, QFileDialog, QMessageBox, QCheckBox, QSpinBox, QHBoxLayout
from PySide2.QtGui import QIcon
from qt_utils import set_theme, load_theme, about_section, readable_size
from image_generation import generate_filename, generate_image, get_font_paths, compress_image

valid_colors_by_font = {
    1: ["Blue", "Orange", "Gold"],
    2: ["Blue", "Orange", "Gold"],
    3: ["Blue", "Orange"],
    4: ["Blue", "Orange", "Yellow"],
    5: ["Orange"],
}


class ImageGenerator:
    icon_path = "Assets/Icons/Raubtier.ico"

    @staticmethod
    def generate_and_display_message(
        text, font, color, save_location, compress, parent=None, max_words_per_line=None
    ):
        if not text.strip():
            return QMessageBox.critical(parent,"MetalSlugFontReborn", "Input text is empty. Please enter some text.")


        try:
            start_time = time()
            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)
            image_path, error_message = generate_image(
                text, filename, font_paths, save_location, max_words_per_line
            )

            if error_message:
                return QMessageBox.critical(parent, "MetalSlugFontReborn", f"Error: {error_message}")

            if compress:
                compress_image(image_path)

            end_time = time()
            image_path = Path(image_path)
            with Image.open(image_path) as image:
                width, height = image.size
                size_bytes = image_path.stat().st_size
                size_human_readable = readable_size(size_bytes)
                success_message = (
                    f"Successfully generated image :)\n"
                    f"Image path: {image_path}\n"
                    f"Width: {width}, Height: {height}\n"
                    f"Size: {size_human_readable}\n"
                    f"Generation time: {end_time - start_time:.3f}s"
                )
            QMessageBox.information(parent, "MetalSlugFontReborn", success_message)

        except FileNotFoundError as e:
            QMessageBox.critical(parent, "MetalSlugFontReborn", str(e))


class MetalSlugFontReborn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MetalSlugFontReborn")
        self.setWindowIcon(QIcon(ImageGenerator.icon_path))
        load_theme()

        self.default_save_location = str(Path.home() / "Desktop")
        self.init_ui()
        self.setMaximumSize(self.size())

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel("Text to Generate:"))
        self.text_entry = QLineEdit()
        self.text_entry.setMinimumWidth(600)
        layout.addWidget(self.text_entry)

        layout.addWidget(QLabel("Select Font:"))
        self.font_combobox = QComboBox()
        self.font_combobox.addItems(map(str, sorted(valid_colors_by_font.keys())))
        layout.addWidget(self.font_combobox)

        layout.addWidget(QLabel("Select Color:"))
        self.color_combobox = QComboBox()
        layout.addWidget(self.color_combobox)

        options_layout = QHBoxLayout()
        self.compress_checkbox = QCheckBox("Compression")
        self.compress_checkbox.setToolTip(
            "Reduces image size, but may increase processing time."
        )
        options_layout.addWidget(self.compress_checkbox)

        self.line_break_checkbox = QCheckBox("Line Break")
        self.line_break_checkbox.setToolTip(
            "Insert line breaks after a number of words, but may increase processing time."
        )
        options_layout.addWidget(self.line_break_checkbox)

        self.words_per_line_label = QLabel("Max Words Per Line:")
        self.words_per_line_spinbox = QSpinBox()
        self.words_per_line_spinbox.setRange(1, 100)
        self.words_per_line_spinbox.setFixedWidth(50)
        self.words_per_line_label.setVisible(False)
        self.words_per_line_spinbox.setVisible(False)

        options_layout.addWidget(self.words_per_line_label)
        options_layout.addWidget(self.words_per_line_spinbox)
        layout.addLayout(options_layout)

        self.line_break_checkbox.stateChanged.connect(self.toggle_words_per_line_spinbox)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_save_location)
        layout.addWidget(browse_button)

        generate_button = QPushButton("Generate and Save Image", self)
        generate_button.clicked.connect(self.generate_and_display_image)
        layout.addWidget(generate_button)

        self.save_location_label = QLabel("Image Save Location:")
        self.save_location_entry = QLineEdit()
        self.save_location_entry.setReadOnly(True)
        self.save_location_entry.setText(self.default_save_location)
        self.save_location_label.setVisible(False)
        self.save_location_entry.setVisible(False)

        layout.addWidget(self.save_location_label)
        layout.addWidget(self.save_location_entry)

        self.font_combobox.currentIndexChanged.connect(self.update_color_combobox)
        self.update_color_combobox()
        self.init_menubar()

    def init_menubar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(lambda: about_section(self))

        theme_menu = menubar.addMenu("Themes")
        theme_menu.addAction("Light Mode").triggered.connect(lambda: set_theme("Light"))
        theme_menu.addAction("Dark Mode").triggered.connect(lambda: set_theme("Dark"))
        theme_menu.addAction("Dracula Mode").triggered.connect(lambda: set_theme("Dracula"))
        theme_menu.addAction("Monokai Mode").triggered.connect(lambda: set_theme("Monokai"))
        theme_menu.addAction("Arc Dark Mode").triggered.connect(lambda: set_theme("Arc Dark"))

    def update_color_combobox(self):
        font = int(self.font_combobox.currentText())
        self.color_combobox.clear()
        self.color_combobox.addItems(valid_colors_by_font[font])

    def toggle_words_per_line_spinbox(self):
        is_checked = self.line_break_checkbox.isChecked()
        self.words_per_line_label.setVisible(is_checked)
        self.words_per_line_spinbox.setVisible(is_checked)

    def browse_save_location(self):
        save_location = QFileDialog.getExistingDirectory(
            self, "Select Image Save Location", self.default_save_location
        )
        if save_location:
            self.save_location_entry.setText(save_location)

    def generate_and_display_image(self):
        text = self.text_entry.text()
        font = int(self.font_combobox.currentText())
        color = self.color_combobox.currentText()
        save_location = self.save_location_entry.text()
        compress = self.compress_checkbox.isChecked()

        max_words_per_line = self.words_per_line_spinbox.value() if self.line_break_checkbox.isChecked() else None

        text = text.upper() if font == 5 else text
        ImageGenerator.generate_and_display_message(text, font, color, save_location, compress, self, max_words_per_line)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MetalSlugFontReborn()
    window.show()
    app.exec_()
