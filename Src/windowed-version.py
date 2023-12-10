from PyQt6.QtGui import (
    QIcon,
    QMovie,
)

from PyQt6.QtCore import (
    Qt, 
    QUrl,
)

from PyQt6.QtGui import (
    QDesktopServices,
)

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QLineEdit,
    QComboBox,
    QWidget,
    QDialog,
    QLabel,
    QTabWidget,
    QTextEdit,
)

from main import generate_filename, generate_image, get_font_paths

from constants import VALID_COLORS_BY_FONT

from theme import dark_theme

class InfoPopup(QDialog):
    def __init__(self, title, message, icon_path):
        super().__init__()

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        label = QLabel(message)
        layout.addWidget(label)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.setStyleSheet(dark_theme)

class ImageGenerator:
    @staticmethod
    def generate_and_display_image(text, font, color):
        try:
            if not text.strip():
                error_message = "Input text is empty. Please enter some text."
                InfoPopup("Error", error_message, "Assets/Icons/Raubtier.ico").exec()
                return

            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)

            img_path, error_message_generate = generate_image(text, filename, font_paths)

            if error_message_generate:
                error_message = f"Error: {error_message_generate}"
                InfoPopup("Error", error_message, "Assets/Icons/Raubtier.ico").exec()
            else:
                success_message = f"Image saved as: \n{img_path}"
                InfoPopup("Success", success_message, "Assets/Icons/Raubtier.ico").exec()

        except FileNotFoundError as e:
            error_message_generate = f"Font file not found: {e.filename}"
            InfoPopup("Error", error_message_generate, "Assets/Icons/Raubtier.ico").exec()
        except Exception as e:
            error_message_generate = f"An error occurred: {e}"
            InfoPopup("Error", error_message_generate, "Assets/Icons/Raubtier.ico").exec()

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

        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)

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

    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About MetalSlugFontReborn")

        layout = QVBoxLayout()

        icon_label = QLabel()
        movie = QMovie("Assets/Icons/Raubtier.gif")
        icon_label.setMovie(movie)
        movie.start()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        program_name_label = QLabel("<h1>MetalSlugFontReborn</h1>\n")
        program_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(program_name_label)

        version_label = QLabel("Version 0.6.5\n")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        author_label = QLabel("Developed by: VermeilChan\n")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

        description_label = QLabel("A tool for creating images with the Metal Slug font.\n")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description_label)

        license_label = QLabel("License: GPL-3.0 License\n")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(license_label)

        credits_label = QLabel(
            "Special thanks to <br>"
            "<a href='https://www.snk-corp.co.jp'>SNK Corporation</a> <br>"
            "<a href='https://github.com/SikroxMemer'>SikroxMemer</a> <br>"
            "<a href='https://6th-divisions-den.com/'>Division 六</a> <br>"
            "<a href='https://www.spriters-resource.com/submitter/Gussprint/'>GussPrint</a> <br>"
            "<a href='https://discord.com/users/477459550904254464/'>BinRich</a> <br>"
            "<a href='https://pyinstaller.org/en/stable/'>PyInstaller</a> <br>"
            "<a href='https://www.riverbankcomputing.com'>PyQt6</a> <br>"
            "<a href='https://upx.github.io'>UPX</a> <br>"
            "<a href='https://python-pillow.org/'>Pillow</a>\n"
        )
        credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits_label.setOpenExternalLinks(True)
        layout.addWidget(credits_label)

        release_date_label = QLabel("\nRelease: November 27, 2023\n")
        release_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(release_date_label)

        github_button = QPushButton("GitHub Repository")
        github_button.clicked.connect(self.open_github_repository)
        layout.addWidget(github_button)

        about_dialog.setLayout(layout)
        about_dialog.exec()

    def open_github_repository(self):
        QDesktopServices.openUrl(QUrl("https://github.com/VermeilChan/MetalSlugFontReborn"))

def main():
    app = QApplication([])
    window = MetalSlugFontReborn()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
