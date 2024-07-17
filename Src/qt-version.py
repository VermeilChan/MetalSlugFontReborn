from os import path
from PIL import Image
from time import time
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QIcon
from image_generation import generate_filename, generate_image, get_font_paths
from utils import set_theme, load_theme, about_section

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
    def generate_and_display_message(text, font, color, save_location, parent=None):
        if not text.strip():
            QMessageBox.critical(
                parent,
                "MetalSlugFontReborn",
                "Input text is empty. Please enter some text.",
            )
            return

        try:
            start_time = time()
            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)
            image_path_str, error_message_generate = generate_image(
                text, filename, font_paths, save_location
            )

            end_time = time()
            if error_message_generate:
                QMessageBox.critical(
                    parent,
                    "MetalSlugFontReborn",
                    f"Error: {error_message_generate}",
                )
            else:
                image_path = Path(image_path_str)
                with Image.open(image_path) as img:
                    width, height = img.size
                    size = path.getsize(image_path_str)
                    success_message = (
                        f"Successfully generated image :)\n"
                        f"Image path: {image_path}\n"
                        f"Width: {width}, Height: {height}\n"
                        f"Size: {size} bytes\n"
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
        self.font_combobox.addItems(list(map(str, sorted(valid_colors_by_font.keys()))))
        layout.addWidget(self.font_combobox)

        layout.addWidget(QLabel("Select Color:"))
        self.color_combobox = QComboBox()
        layout.addWidget(self.color_combobox)

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

        self.font_combobox.currentIndexChanged.connect(self.on_font_change)
        self.on_font_change()

        self.init_menubar()

    def init_menubar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(lambda: about_section(self))

        theme_menu = menubar.addMenu("Themes")
        theme_menu.addAction("Light Mode").triggered.connect(lambda: set_theme("Light"))
        theme_menu.addAction("Dark Mode").triggered.connect(lambda: set_theme("Dark"))

    def on_font_change(self):
        font = int(self.font_combobox.currentText())
        valid_colors = valid_colors_by_font.get(font, [])
        self.color_combobox.clear()
        self.color_combobox.addItems(valid_colors)
        self.color_combobox.setEnabled(bool(valid_colors))
        if valid_colors:
            self.color_combobox.setCurrentIndex(0)

    def generate_and_display_image(self):
        text = self.text_entry.text()
        font = int(self.font_combobox.currentText())
        color = self.color_combobox.currentText()
        save_location = self.save_location_entry.text()

        text = text.upper() if font == 5 else text
        ImageGenerator.generate_and_display_message(
            text, font, color, save_location, self
        )

    def browse_save_location(self):
        save_location = QFileDialog.getExistingDirectory(
            self, "Select Save Location", self.default_save_location
        )
        if save_location:
            self.save_location_entry.setText(save_location)


def main():
    app = QApplication([])
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(ImageGenerator.icon_path))
    window = MetalSlugFontReborn()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
