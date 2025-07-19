import sys
import platform
from time import time
from pathlib import Path
from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow, QWidget,
                               QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QSlider)
from utils import readable_size
from qt_utils import about_section, load_theme, set_theme
from image_generation import (compress_image, generate_filename, generate_image, get_font_paths)

FONT_COLORS = {
    1: ["Blue", "Orange", "Gold"],
    2: ["Blue", "Orange", "Gold"],
    3: ["Blue", "Orange"],
    4: ["Blue", "Orange", "Yellow"],
    5: ["Orange"],
}

class ImageProcessor:
    @staticmethod
    def process_image(text, font, color, save_path, compress, compress_level, parent, max_words=None):
        if not text.strip():
            QMessageBox.critical(parent, "Error", "Input text cannot be empty")
            return

        try:
            start = time()
            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)
            
            image_path, error = generate_image(text, filename, font_paths, save_path, max_words)
            if error:
                raise RuntimeError(error)

            if compress:
                compress_image(image_path, compress_level)

            ImageProcessor.show_success_message(image_path, start, parent)
        
        except Exception as e:
            QMessageBox.critical(parent, "Error", str(e))

    @staticmethod
    def show_success_message(image_path, start_time, parent):
        path = Path(image_path)
        with Image.open(path) as img:
            size = readable_size(path.stat().st_size)
            message = (
                "Successfully generated image :)\n\n"
                f"Path: {path}\n"
                f"Dimensions: {img.width} x {img.height}\n"
                f"Size: {size}\n"
                f"Time: {time() - start_time:.3f} seconds"
            )
            QMessageBox.information(parent, "Success", message)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MetalSlugFontReborn")
        self.setWindowIcon(QIcon("Assets/Icons/Raubtier.ico"))
        self.setup_ui()
        load_theme()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.add_text_input(layout)
        self.add_font_selector(layout)
        self.add_color_selector(layout)
        self.add_options(layout)
        self.add_action_buttons(layout)
        self.create_menubar()

        self.setMaximumSize(self.size())

    def add_text_input(self, layout):
        layout.addWidget(QLabel("Text to Generate:"))
        self.text_input = QLineEdit()
        self.text_input.setMinimumWidth(600)
        layout.addWidget(self.text_input)

    def add_font_selector(self, layout):
        layout.addWidget(QLabel("Select Font:"))
        self.font_select = QComboBox()
        self.font_select.addItems(map(str, sorted(FONT_COLORS)))
        self.font_select.currentIndexChanged.connect(self.update_colors)
        layout.addWidget(self.font_select)

    def add_color_selector(self, layout):
        layout.addWidget(QLabel("Select Color:"))
        self.color_select = QComboBox()
        layout.addWidget(self.color_select)
        self.update_colors()

    def add_options(self, layout):
        options_h_layout = QHBoxLayout()

        self.compress_option = QCheckBox("Compression")
        self.compress_option.setChecked(True)
        options_h_layout.addWidget(self.compress_option)

        self.compress_level_label = QLabel("Compression Level: 6")
        self.compress_level_slider = QSlider(Qt.Horizontal)
        self.compress_level_slider.setRange(0, 9)
        self.compress_level_slider.setValue(6)
        self.compress_level_slider.setTickPosition(QSlider.TicksBelow)
        self.compress_level_slider.setTickInterval(1)
        self.compress_level_slider.setFixedWidth(150)

        options_h_layout.addWidget(self.compress_level_label)
        options_h_layout.addWidget(self.compress_level_slider)

        self.compress_option.toggled.connect(self.toggle_compression_options)
        self.compress_level_slider.valueChanged.connect(self.update_compress_level_label)

        self.line_break_option = QCheckBox("Line Break")
        self.max_words_label = QLabel("Max Words Per Line:")
        self.max_words_input = QSpinBox()
        self.max_words_input.setRange(1, 100)
        self.max_words_input.setValue(10)
        self.max_words_input.setFixedWidth(50)
        
        self.line_break_option.toggled.connect(self.toggle_word_limit)
        self.toggle_word_limit(False)

        options_h_layout.addWidget(self.line_break_option)
        options_h_layout.addWidget(self.max_words_label)
        options_h_layout.addWidget(self.max_words_input)
        
        layout.addLayout(options_h_layout)
        self.toggle_compression_options(self.compress_option.isChecked())

    def add_action_buttons(self, layout):
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_save_path)
        
        generate_btn = QPushButton("Generate and Save Image")
        generate_btn.clicked.connect(self.generate_image)
        
        layout.addWidget(browse_btn)
        layout.addWidget(generate_btn)

    def create_menubar(self):
        menubar = self.menuBar()
        
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About").triggered.connect(lambda: about_section(self))

        theme_menu = menubar.addMenu("Themes")
        for theme in ["Light", "Dark", "Dracula", "Monokai", "Arc Dark"]:
            theme_menu.addAction(f"{theme} Mode").triggered.connect(
                lambda _, t=theme: set_theme(t)
            )

    def update_colors(self):
        self.color_select.clear()
        font = int(self.font_select.currentText())
        self.color_select.addItems(FONT_COLORS[font])

    def toggle_word_limit(self, visible):
        self.max_words_label.setVisible(visible)
        self.max_words_input.setVisible(visible)

    def toggle_compression_options(self, checked):
        self.compress_level_label.setVisible(checked)
        self.compress_level_slider.setVisible(checked)

    def update_compress_level_label(self, value):
        self.compress_level_label.setText(f"Compression Level: {value}")

    def select_save_path(self):
        if path := QFileDialog.getExistingDirectory(self, "Select Save Location", str(Path.home() / "Desktop")):
            self.save_path = Path(path)

    def generate_image(self):
        text = self.text_input.text()
        if (font := int(self.font_select.currentText())) == 5:
            text = text.upper()

        save_path = getattr(self, "save_path", Path.home() / "Desktop")

        compress_enabled = self.compress_option.isChecked()
        compress_level = self.compress_level_slider.value() if compress_enabled else 6

        ImageProcessor.process_image(
            text=text,
            font=font,
            color=self.color_select.currentText(),
            save_path=save_path,
            compress=compress_enabled,
            compress_level=compress_level,
            parent=self,
            max_words=self.max_words_input.value() if self.line_break_option.isChecked() else None
        )

def detect_windows_version():
    if platform.system() == "Windows":
        version = platform.version()
        build = int(version.split('.')[-1])
        if build >= 22000:
            return 11
        else:
            return 10
    return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    os_name = platform.system()
    if os_name == "Windows":
        win_ver = detect_windows_version()
        if win_ver == 11:
            app.setStyle("FluentWinUI3")
        else:
            app.setStyle("Fusion")
    elif os_name == "Darwin":
        app.setStyle("macOS")
    else:
        app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
