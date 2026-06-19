import platform
import sys
import tempfile
from pathlib import Path
from time import time

from PIL import Image as PILImage
from PySide6.QtCore import QObject, Qt, QThread, QTimer, QUrl, Signal, Slot
from PySide6.QtGui import (QColor, QDesktopServices, QIcon, QKeySequence,
                           QPainter, QPixmap, QShortcut)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                               QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                               QMainWindow, QMessageBox, QPlainTextEdit,
                               QPushButton, QSlider, QSpinBox, QVBoxLayout,
                               QWidget)

from image_generation import generate_filename, generate_image, get_font_paths
from qt_utils import about_section, load_config, save_config, set_theme
from utils import readable_size

DEFAULT_COMPRESS_LEVEL = 6
PREVIEW_COMPRESS_LEVEL = 1
DISABLE_COMPRESSION = 0

WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 550
INITIAL_PROMPT_DELAY = 100

MAIN_LAYOUT_SPACING = 15
MAIN_LAYOUT_MARGIN = 20
TEXT_INPUT_MAX_HEIGHT = 55
FORM_LAYOUT_H_SPACING = 20

PREVIEW_MIN_HEIGHT = 100
PREVIEW_TIMER_INTERVAL = 150
PREVIEW_MAX_DIMENSION = 32768
PREVIEW_SCALE_WIDTH = 400
PREVIEW_SCALE_HEIGHT = 80

COMPRESS_SLIDER_MIN = 0
COMPRESS_SLIDER_MAX = 9
COMPRESS_SLIDER_TICK_INTERVAL = 1
COMPRESS_LEVEL_LABEL_WIDTH = 20

MAX_WORDS_MIN = 1
MAX_WORDS_MAX = 100
MAX_WORDS_DEFAULT = 10
MAX_WORDS_INPUT_WIDTH = 80

TOOLTIP_DURATION = 5000

COLOR_ICON_SIZE = 16
COLOR_ICON_MARGIN = 1

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

class ImageWorker(QObject):
    finished = Signal(str, float)
    failed = Signal(str)

    @Slot(dict)
    def process(self, params):
        try:
            start = time()
            filename = generate_filename(params["text"])
            font_paths = get_font_paths(params["font"], params["color"])

            # FIX: Trust the compress_level sent by the UI instead of overriding it
            compress_lvl = params["compress_level"]
            
            image_path, error = generate_image(
                params["text"], 
                filename, 
                font_paths, 
                params["save_path"], 
                params["max_words"],
                compress_level=compress_lvl
            )
            
            if error:
                raise RuntimeError(error)

            self.finished.emit(image_path, start)
        except PILImage.DecompressionBombError:
            self.failed.emit(
                "Whoa, that's a massive image!\n\n"
                "The text you entered is so long that the generated image exceeds the system's maximum pixel limit. "
                "Computers have a hard cap on how wide or tall an image can be.\n\n"
                "To fix this, try shortening your text or turning on 'Automatic line breaks' to stack the text vertically."
            )
        except Exception as e:
            self.failed.emit(str(e))


class MainWindow(QMainWindow):
    trigger_generation = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metal Slug Font Reborn")
        self.setWindowIcon(QIcon("Assets/Icons/Raubtier.ico"))
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.save_path = Path.home() / "Desktop"
        
        self.setup_thread()
        self.setup_ui()
        set_theme()

        QTimer.singleShot(INITIAL_PROMPT_DELAY, self.prompt_save_location)

    def setup_thread(self):
        self._thread = QThread()
        self._worker = ImageWorker()
        self._worker.moveToThread(self._thread)
        
        self._worker.finished.connect(self.on_generation_finished)
        self._worker.failed.connect(self.on_generation_failed)
        self.trigger_generation.connect(self._worker.process)
        
        self._thread.start()

    def closeEvent(self, event):
        self._thread.quit()
        self._thread.wait()
        super().closeEvent(event)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(MAIN_LAYOUT_SPACING)
        main_layout.setContentsMargins(MAIN_LAYOUT_MARGIN, MAIN_LAYOUT_MARGIN, MAIN_LAYOUT_MARGIN, MAIN_LAYOUT_MARGIN)

        text_group = QGroupBox("Text to Generate")
        text_layout = QVBoxLayout(text_group)
        
        self.text_input = QPlainTextEdit()
        self.text_input.setPlaceholderText("Enter your text here...")
        self.text_input.setMaximumHeight(TEXT_INPUT_MAX_HEIGHT)
        self.text_input.textChanged.connect(self.update_character_count)
        text_layout.addWidget(self.text_input)
        
        self.text_info_layout = QHBoxLayout()
        self.char_count_label = QLabel("Characters: 0")
        self.char_count_label.setStyleSheet("color: #666; font-size: 10pt;")
        self.text_info_layout.addWidget(self.char_count_label)
        self.text_info_layout.addStretch()
        
        self.dimensions_label = QLabel("Resolution: -")
        self.dimensions_label.setStyleSheet("color: #666; font-size: 10pt;")
        self.text_info_layout.addWidget(self.dimensions_label)
        
        text_layout.addLayout(self.text_info_layout)
        
        main_layout.addWidget(text_group)

        style_group = QGroupBox("Font Settings")
        style_layout = QFormLayout(style_group)
        style_layout.setHorizontalSpacing(FORM_LAYOUT_H_SPACING)

        self.font_select = QComboBox()
        self.font_select.addItems(map(str, sorted(FONT_COLORS)))
        self.font_select.currentIndexChanged.connect(self.update_colors)

        self.color_select = QComboBox()

        style_layout.addRow("Font:", self.font_select)
        style_layout.addRow("Color:", self.color_select)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(PREVIEW_MIN_HEIGHT)
        self.preview_label.setText("Loading preview...")
        style_layout.addRow(self.preview_label)

        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.setInterval(PREVIEW_TIMER_INTERVAL)
        self.preview_timer.timeout.connect(self.update_preview)

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
        self.compress_level_slider.setRange(COMPRESS_SLIDER_MIN, COMPRESS_SLIDER_MAX)
        self.compress_level_slider.setValue(DEFAULT_COMPRESS_LEVEL)
        self.compress_level_slider.setTickPosition(QSlider.TicksBelow)
        self.compress_level_slider.setTickInterval(COMPRESS_SLIDER_TICK_INTERVAL)
        self.compress_level_slider.valueChanged.connect(
            self.update_compress_level_label
        )

        self.compress_level_label = QLabel(str(DEFAULT_COMPRESS_LEVEL))
        self.compress_level_label.setFixedWidth(COMPRESS_LEVEL_LABEL_WIDTH)

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
        self.max_words_input.setRange(MAX_WORDS_MIN, MAX_WORDS_MAX)
        self.max_words_input.setValue(MAX_WORDS_DEFAULT)
        self.max_words_input.setFixedWidth(MAX_WORDS_INPUT_WIDTH)

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

        self.text_input.textChanged.connect(self.schedule_preview_update)
        self.font_select.currentIndexChanged.connect(self.schedule_preview_update)
        self.color_select.currentTextChanged.connect(self.schedule_preview_update)
        self.line_break_option.toggled.connect(self.schedule_preview_update)
        self.max_words_input.valueChanged.connect(self.schedule_preview_update)
        self.schedule_preview_update()

        self.create_menubar()
        self.setup_shortcuts()

    def setup_shortcuts(self):
        enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_shortcut.activated.connect(self.generate_image)

        numpad_enter_shortcut = QShortcut(QKeySequence(Qt.Key_Enter), self)
        numpad_enter_shortcut.activated.connect(self.generate_image)

    def schedule_preview_update(self):
        self.preview_timer.start()

    def update_preview(self):
        if not self.font_select.currentText() or not self.color_select.currentText():
            return

        font = int(self.font_select.currentText())
        color = self.color_select.currentText()
        text = self.text_input.toPlainText().strip()

        if not text:
            text = "METAL SLUG IS PEAK!"

        if font == 5:
            text = text.upper()

        max_words = (
            self.max_words_input.value()
            if self.line_break_option.isChecked()
            else None
        )

        try:
            font_paths = get_font_paths(font, color)
            preview_dir = Path(tempfile.gettempdir()) / "msf_preview"
            preview_dir.mkdir(exist_ok=True)

            image_path, error = generate_image(
                text, "preview.png", font_paths, str(preview_dir), max_words, compress_level=PREVIEW_COMPRESS_LEVEL
            )

            if error:
                self.preview_label.setPixmap(QPixmap())
                self.preview_label.setText("Preview unavailable")
                self.dimensions_label.setText("Resolution: -")
                return

            with PILImage.open(image_path) as img:
                width, height = img.width, img.height
                self.dimensions_label.setText(f"Resolution: {width} x {height}")
                
                if width > PREVIEW_MAX_DIMENSION or height > PREVIEW_MAX_DIMENSION:
                    self.preview_label.setPixmap(QPixmap())
                    self.preview_label.setText(
                        "Preview is too large to display!\n"
                        "The image is perfectly fine, but it exceeds the 32,000 pixel width limit for live previews.\n"
                        "It will still generate successfully, but please be aware it may fail to open in some image viewers."
                    )
                    return

            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                self.preview_label.setPixmap(QPixmap())
                self.preview_label.setText("Preview unavailable")
                self.dimensions_label.setText("Resolution: -")
                return

            scaled = pixmap.scaled(
                PREVIEW_SCALE_WIDTH, PREVIEW_SCALE_HEIGHT, 
                Qt.KeepAspectRatio, 
                Qt.FastTransformation
            )

            self.preview_label.setPixmap(scaled)
        except PILImage.DecompressionBombError:
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("Image is too large to generate!")
            self.dimensions_label.setText("Resolution: -")
        except FileNotFoundError:
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("Preview: unsupported character in text")
            self.dimensions_label.setText("Resolution: -")
        except Exception:
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("Preview unavailable")
            self.dimensions_label.setText("Resolution: -")

    def update_character_count(self):
        text = self.text_input.toPlainText()
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
        self.save_location_label.setToolTipDuration(TOOLTIP_DURATION)

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
            size = COLOR_ICON_SIZE
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(COLORS[color_name]))

            margin = COLOR_ICON_MARGIN
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
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.critical(self, "Error", "Please enter some text to generate.")
            return

        font = int(self.font_select.currentText())
        if font == 5:
            text = text.upper()

        compress_enabled = self.compress_option.isChecked()
        compress_level = self.compress_level_slider.value() if compress_enabled else DISABLE_COMPRESSION

        max_words = self.max_words_input.value() if self.line_break_option.isChecked() else None

        params = {
            "text": text,
            "font": font,
            "color": self.color_select.currentText(),
            "save_path": str(self.save_path),
            "compress": compress_enabled,
            "compress_level": compress_level,
            "max_words": max_words
        }

        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("Generating...")

        self.trigger_generation.emit(params)

    @Slot(str, float)
    def on_generation_finished(self, image_path, start_time):
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("Generate Image")
        
        path = Path(image_path)
        try:
            with PILImage.open(path) as img:
                size = readable_size(path.stat().st_size)
                message = (
                    "Successfully generated image!\n\n"
                    f"Image saved at: {path}\n"
                    f"Dimensions: {img.width} x {img.height} pixels\n"
                    f"File size: {size}\n"
                    f"Time taken: {time() - start_time:.3f} seconds"
                )

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Success")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Information)

            open_button = msg_box.addButton("Open Image", QMessageBox.AcceptRole)
            ok_button = msg_box.addButton(QMessageBox.Ok)
            msg_box.setDefaultButton(ok_button)

            msg_box.exec()

            if msg_box.clickedButton() == open_button:
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read generated image:\n{str(e)}")

    @Slot(str)
    def on_generation_failed(self, error_msg):
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("Generate Image")
        QMessageBox.critical(self, "Error", error_msg)


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
