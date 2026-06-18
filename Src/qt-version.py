import platform
import sys
from pathlib import Path
from time import time

from PIL import Image
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QIcon, QShortcut, QKeySequence, QColor, QPixmap, QPainter, QDesktopServices 
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                               QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QMainWindow, QMessageBox,
                               QPushButton, QSlider, QSpinBox, QVBoxLayout,
                               QWidget)

from image_generation import (compress_image, generate_filename,
                              generate_image, get_font_paths)
from qt_utils import about_section, load_config, save_config, set_theme
from utils import readable_size

FONT_COLORS = {
    1: ["Blue", "Orange", "Gold"],
    2: ["Blue", "Orange", "Gold"],
    3: ["Blue", "Orange"],
    4: ["Blue", "Orange", "Yellow"],
    5: ["Orange"],
}

COLORS = {
    "Blue": "#2596be",
    "Orange": "#f89000", 
    "Gold": "#f99010",
    "Yellow": "#f8f900",
}

class ImageProcessor:
    @staticmethod
    def process_image(
        text, font, color, save_path, compress, compress_level, parent, max_words=None
    ):
        if not text.strip():
            QMessageBox.critical(parent, "Error", "Input text cannot be empty")
            return

        try:
            start = time()
            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)

            image_path, error = generate_image(
                text, filename, font_paths, save_path, max_words
            )
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
                "Successfully generated image!\n\n"
                f"Image saved at: {path}\n"
                f"Dimensions: {img.width} x {img.height} pixels\n"
                f"File size: {size}\n"
                f"Time taken: {time() - start_time:.3f} seconds"
            )

        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)

        open_button = msg_box.addButton("Open Image", QMessageBox.AcceptRole)
        ok_button = msg_box.addButton(QMessageBox.Ok)
        msg_box.setDefaultButton(ok_button)

        msg_box.exec()

        if msg_box.clickedButton() == open_button:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metal Slug Font Reborn")
        self.setWindowIcon(QIcon("Assets/Icons/Raubtier.ico"))
        self.setMinimumSize(600, 450)
        self.save_path = Path.home() / "Desktop"
        self.setup_ui()
        set_theme()

        QTimer.singleShot(100, self.prompt_save_location)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        text_group = QGroupBox("Text to Generate")
        text_layout = QVBoxLayout(text_group)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter your text here...")
        self.text_input.textChanged.connect(self.update_character_count)
        text_layout.addWidget(self.text_input)
        
        self.char_count_layout = QHBoxLayout()
        self.char_count_label = QLabel("Characters: 0")
        self.char_count_label.setStyleSheet("color: #666; font-size: 10pt;")
        self.char_count_layout.addWidget(self.char_count_label)
        self.char_count_layout.addStretch()
        text_layout.addLayout(self.char_count_layout)
        
        main_layout.addWidget(text_group)

        style_group = QGroupBox("Font Settings")
        style_layout = QFormLayout(style_group)
        style_layout.setHorizontalSpacing(20)

        self.font_select = QComboBox()
        self.font_select.addItems(map(str, sorted(FONT_COLORS)))
        self.font_select.currentIndexChanged.connect(self.update_colors)

        self.color_select = QComboBox()

        style_layout.addRow("Font:", self.font_select)
        style_layout.addRow("Color:", self.color_select)
        main_layout.addWidget(style_group)

        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)

        compress_layout = QVBoxLayout()
        self.compress_option = QCheckBox("Enable compression")
        self.compress_option.setChecked(True)
        self.compress_option.toggled.connect(self.toggle_compression_options)
        compress_layout.addWidget(self.compress_option)

        self.level_layout = QHBoxLayout()
        self.level_layout.addWidget(QLabel("Compression level:"))
        self.compress_level_slider = QSlider(Qt.Horizontal)
        self.compress_level_slider.setRange(0, 9)
        self.compress_level_slider.setValue(6)
        self.compress_level_slider.setTickPosition(QSlider.TicksBelow)
        self.compress_level_slider.setTickInterval(1)
        self.compress_level_slider.valueChanged.connect(
            self.update_compress_level_label
        )

        self.compress_level_label = QLabel("6")
        self.compress_level_label.setFixedWidth(20)

        self.level_layout.addWidget(self.compress_level_slider)
        self.level_layout.addWidget(self.compress_level_label)
        self.level_layout.addStretch()
        compress_layout.addLayout(self.level_layout)
        options_layout.addLayout(compress_layout)

        line_break_layout = QHBoxLayout()
        self.line_break_option = QCheckBox("Automatic line breaks")
        self.line_break_option.toggled.connect(self.toggle_word_limit)

        line_break_layout.addWidget(self.line_break_option)
        line_break_layout.addStretch()

        self.max_words_label = QLabel("Max words per line:")
        self.max_words_input = QSpinBox()
        self.max_words_input.setRange(1, 100)
        self.max_words_input.setValue(10)
        self.max_words_input.setFixedWidth(80)

        line_break_layout.addWidget(self.max_words_label)
        line_break_layout.addWidget(self.max_words_input)
        options_layout.addLayout(line_break_layout)

        main_layout.addWidget(options_group)

        button_layout = QHBoxLayout()
        self.browse_btn = QPushButton("Change Save Location")
        self.browse_btn.clicked.connect(self.select_save_path)

        self.generate_btn = QPushButton("Generate Image")
        self.generate_btn.clicked.connect(self.generate_image)

        button_layout.addWidget(self.browse_btn)
        button_layout.addWidget(self.generate_btn)
        main_layout.addLayout(button_layout)

        self.save_location_label = QLabel("Save location: Desktop (default)")
        self.save_location_label.setStyleSheet("color: #666; font-style: italic;")
        self.update_save_location_display()
        main_layout.addWidget(self.save_location_label)

        self.update_colors()
        self.toggle_word_limit(False)
        self.toggle_compression_options(True)

        self.create_menubar()
        self.setup_shortcuts()

    def setup_shortcuts(self):
        enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_shortcut.activated.connect(self.generate_image)

        numpad_enter_shortcut = QShortcut(QKeySequence(Qt.Key_Enter), self)
        numpad_enter_shortcut.activated.connect(self.generate_image)

    def update_character_count(self):
        text = self.text_input.text()
        char_count = len(text)
        self.char_count_label.setText(f"Characters: {char_count}")
        self.char_count_label.setStyleSheet("color: #666; font-size: 10pt;")

    def update_save_location_display(self):
        folder_name = self.save_path.name if self.save_path.name else str(self.save_path)
        display_text = f"Save location: {folder_name}"
        if self.save_path == Path.home() / "Desktop":
            display_text += " (default)"
        
        self.save_location_label.setText(display_text)
        self.save_location_label.setToolTip(f"Full path: {self.save_path}")
        self.save_location_label.setToolTipDuration(5000)

    def prompt_save_location(self):
        if load_config("skip_location_prompt", fallback="False") == "True":
            return

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Welcome to Metal Slug Font Reborn!")
        msg_box.setText(
            "Your images will be saved to your Desktop by default.\n\n"
            "Would you like to choose a different folder?"
        )
        msg_box.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No
        )
        msg_box.setDefaultButton(QMessageBox.No)

        cb = QCheckBox("Don't ask me again")
        msg_box.setCheckBox(cb)

        reply = msg_box.exec()

        if cb.isChecked():
            save_config("skip_location_prompt", "True")

        if reply == QMessageBox.Yes:
            self.select_save_path()

    def create_menubar(self):
        menubar = self.menuBar()

        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About MetalSlugFontReborn").triggered.connect(
            lambda: about_section(self)
        )
        help_menu.addAction("About Qt").triggered.connect(QApplication.aboutQt)

        theme_menu = menubar.addMenu("Themes")
        for theme in ["Light", "Dark", "Tokyo Night"]:
            theme_menu.addAction(f"{theme} Mode").triggered.connect(
                lambda _, t=theme: set_theme(t)
            )

    def update_colors(self):
        self.color_select.clear()
        font = int(self.font_select.currentText())

        for color_name in FONT_COLORS[font]:
            size = 16
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(COLORS[color_name]))

            margin = 1
            painter.drawEllipse(margin, margin, size - 2 * margin, size - 2 * margin)
            painter.end()

            self.color_select.addItem(QIcon(pixmap), color_name)

    def toggle_word_limit(self, visible):
        self.max_words_label.setVisible(visible)
        self.max_words_input.setVisible(visible)

    def toggle_compression_options(self, checked):
        for i in range(self.level_layout.count()):
            widget = self.level_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(checked)

    def update_compress_level_label(self, value):
        self.compress_level_label.setText(str(value))

    def select_save_path(self):
        if path := QFileDialog.getExistingDirectory(
            self, "Select Save Location", str(self.save_path)
        ):
            self.save_path = Path(path)
            self.update_save_location_display()
            QMessageBox.information(
                self, "Save Location Updated", f"Images will now be saved to:\n{path}"
            )

    def generate_image(self):
        text = self.text_input.text().strip()
        if not text:
            QMessageBox.critical(self, "Error", "Please enter some text to generate.")
            return

        font = int(self.font_select.currentText())
        if font == 5:
            text = text.upper()

        compress_enabled = self.compress_option.isChecked()
        compress_level = self.compress_level_slider.value() if compress_enabled else 6

        ImageProcessor.process_image(
            text=text,
            font=font,
            color=self.color_select.currentText(),
            save_path=self.save_path,
            compress=compress_enabled,
            compress_level=compress_level,
            parent=self,
            max_words=self.max_words_input.value()
            if self.line_break_option.isChecked()
            else None,
        )

def detect_windows_version():
    system = platform.system()
    if system == "Windows":
        release = platform.release()
        return f"{release}".strip()
    return platform.system()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    os_name = platform.system()
    if os_name == "Windows" and detect_windows_version() == "11":
        app.setStyle("FluentWinUI3")
    elif os_name == "Darwin":
        app.setStyle("macOS")
    else:
        app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
