import platform

from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import ( 
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QGroupBox,
    QComboBox,
    QWidget,
    QDialog,
    QLabel,
)

from main import generate_filename, generate_image, get_font_paths
from constants import VALID_COLORS_BY_FONT

class InfoPopup(QDialog):
    def __init__(self, title, message, ICON_PATH):
        super().__init__()

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(ICON_PATH))

        layout = QVBoxLayout()

        label = QLabel(message)
        layout.addWidget(label)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

class ImageGenerator:
    ICON_PATH = f"Assets/Icons/Raubtier.ico"

    @staticmethod
    def generate_and_display_image(text, font, color):
        try:
            if not text.strip():
                error_message = f"\nInput text is empty. Please enter some text.\n"
                InfoPopup(f"Error", error_message, ImageGenerator.ICON_PATH).exec()
                return

            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)

            img_path, error_message_generate = generate_image(text, filename, font_paths)

            if error_message_generate:
                error_message = f"Error: {error_message_generate}"
                InfoPopup(f"Error", error_message, ImageGenerator.ICON_PATH).exec()
            else:
                success_message = f"Image saved as: \n{img_path}"
                InfoPopup(f"Success", success_message, ImageGenerator.ICON_PATH).exec()

        except FileNotFoundError as e:
            error_message_generate = f"Font file not found: {e.filename}"
            InfoPopup(f"Error", error_message_generate, ImageGenerator.ICON_PATH).exec()

        except Exception as e:
            error_message_generate = f"An error occurred: {e}"
            InfoPopup(f"Error", error_message_generate, ImageGenerator.ICON_PATH).exec()

class MetalSlugFontReborn(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"MetalSlugFontReborn")

        self.setWindowIcon(QIcon(ImageGenerator.ICON_PATH))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        text_label = QLabel(f"Text to Generate:")
        layout.addWidget(text_label)
        self.text_entry = QLineEdit()
        self.text_entry.setMinimumWidth(600)
        layout.addWidget(self.text_entry)

        font_label = QLabel(f"Select Font:")
        layout.addWidget(font_label)
        self.font_combobox = QComboBox()
        self.font_combobox.addItems([f"1", "2", "3", "4", "5"])
        layout.addWidget(self.font_combobox)

        color_label = QLabel(f"Select Color:")
        layout.addWidget(color_label)
        self.color_combobox = QComboBox()
        layout.addWidget(self.color_combobox)

        generate_button = QPushButton(f"Generate and Save Image", self)
        generate_button.clicked.connect(self.generate_and_display_image)
        layout.addWidget(generate_button)

        self.color_combobox.setEnabled(False)
        self.font_combobox.currentIndexChanged.connect(self.on_font_change)

        self.on_font_change()

        menubar = self.menuBar()
        help_menu = menubar.addMenu(f"Help")

        about_action = help_menu.addAction(f"About...")
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
        about_dialog.setWindowTitle(f"About")

        layout = QVBoxLayout()

        top_left_layout = QHBoxLayout()

        icon_label = QLabel()
        movie = QMovie(f"Assets/Icons/Raubtier.gif")
        movie.setScaledSize(QSize(84, 108))
        icon_label.setMovie(movie)
        movie.start()
        top_left_layout.addWidget(icon_label)

        metadata_layout = QVBoxLayout()
        metadata_layout.addWidget(QLabel(f"MetalSlugFontReborn (64-bit)"))
        metadata_layout.addWidget(QLabel(f"GPL-3.0 License"))
        
        github_link_label = QLabel(f'<a href="https://github.com/VermeilChan/MetalSlugFontReborn">GitHub Repository</a>')
        github_link_label.setOpenExternalLinks(True)
        metadata_layout.addWidget(github_link_label)

        top_left_layout.addLayout(metadata_layout)
        layout.addLayout(top_left_layout)

        build_info_box = QGroupBox(f"Build Information")
        build_info_layout = QVBoxLayout()

        build_info_layout.addWidget(QLabel(f"Version: 1.x.x (Dev)"))
        build_info_layout.addWidget(QLabel(f"Pyinstaller: 6.3.0"))
        build_info_layout.addWidget(QLabel(f"PyQt6: 6.6.1"))
        build_info_layout.addWidget(QLabel(f"Build date: Dec 27 2023"))

        os_info_box = QGroupBox(f"Operating System")
        os_info_layout = QVBoxLayout()

        os_info_layout.addWidget(QLabel(f"OS: {platform.system()}"))
        os_info_layout.addWidget(QLabel(f"Version: {platform.version()}"))

        os_info_box.setLayout(os_info_layout)
        layout.addWidget(os_info_box)

        build_info_box.setLayout(build_info_layout)
        layout.addWidget(build_info_box)

        about_dialog.setLayout(layout)
        about_dialog.exec()

def main():
    app = QApplication([])
    app.setStyle(f'Fusion')
    window = MetalSlugFontReborn()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
