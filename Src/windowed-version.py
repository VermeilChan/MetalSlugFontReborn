from platform import system, version, release, architecture

from PyQt6.QtGui import QIcon, QPixmap
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

VALID_COLORS_BY_FONT = {
    1: ["Blue", "Orange-1", "Orange-2"],
    2: ["Blue", "Orange-1", "Orange-2"],
    3: ["Blue", "Orange-1"],
    4: ["Blue", "Orange-1"],
    5: ["Orange-1"]
}

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
    ICON_PATH = "Assets/Icons/Raubtier.ico"

    @staticmethod
    def generate_and_display_image(text, font, color):
        try:
            if not text.strip():
                error_message = "\nInput text is empty. Please enter some text.\n"
                InfoPopup("Error", error_message, ImageGenerator.ICON_PATH).exec()
                return

            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)

            img_path, error_message_generate = generate_image(text, filename, font_paths)

            if error_message_generate:
                error_message = f"Error: {error_message_generate}"
                InfoPopup("Error", error_message, ImageGenerator.ICON_PATH).exec()
            else:
                success_message = f"Image saved as: \n{img_path}"
                InfoPopup("Success", success_message, ImageGenerator.ICON_PATH).exec()

        except (FileNotFoundError, Exception) as e:
            error_message_generate = str(e)
            InfoPopup("Error", error_message_generate, ImageGenerator.ICON_PATH).exec()

class MetalSlugFontReborn(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MetalSlugFontReborn")

        self.setWindowIcon(QIcon(ImageGenerator.ICON_PATH))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        text_label = QLabel("Text to Generate:")
        layout.addWidget(text_label)
        self.text_entry = QLineEdit()
        self.text_entry.setMinimumWidth(600)
        layout.addWidget(self.text_entry)

        font_label = QLabel("Select Font:")
        layout.addWidget(font_label)
        self.font_combobox = QComboBox()
        self.font_combobox.addItems(map(str, range(1, 6)))
        layout.addWidget(self.font_combobox)

        color_label = QLabel("Select Color:")
        layout.addWidget(color_label)
        self.color_combobox = QComboBox()
        layout.addWidget(self.color_combobox)

        generate_button = QPushButton("Generate and Save Image", self)
        generate_button.clicked.connect(self.generate_and_display_image)
        layout.addWidget(generate_button)

        self.color_combobox.setEnabled(False)
        self.font_combobox.currentIndexChanged.connect(self.on_font_change)

        self.on_font_change()

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
        about_dialog.setWindowTitle("About")

        layout = QVBoxLayout()

        top_left_layout = QHBoxLayout()

        icon_label = QLabel()
        pixmap = QPixmap("Assets/Icons/Raubtier.png")
        icon_label.setPixmap(pixmap)
        top_left_layout.addWidget(icon_label)

        metadata_layout = QVBoxLayout()
        metadata_layout.addWidget(QLabel("MetalSlugFontReborn (64-bit)"))
        metadata_layout.addWidget(QLabel("GPL-3.0 License"))

        github_link_label = QLabel('<a href="https://github.com/VermeilChan/MetalSlugFontReborn">GitHub Repository</a>')
        github_link_label.setOpenExternalLinks(True)
        metadata_layout.addWidget(github_link_label)

        top_left_layout.addLayout(metadata_layout)
        layout.addLayout(top_left_layout)

        build_info_box = QGroupBox("Build Information")
        build_info_layout = QVBoxLayout()

        build_info_layout.addWidget(QLabel("Version: 1.x.x (Dev)"))
        build_info_layout.addWidget(QLabel("Pyinstaller: 6.3.0"))
        build_info_layout.addWidget(QLabel("PyQt6: 6.6.1"))
        build_info_layout.addWidget(QLabel("Build date: Dec 27 2023"))

        os_info_box = QGroupBox("Operating System")
        os_info_layout = QVBoxLayout()

        os_name = system()
        os_version = version()
        os_release = release()
        os_architecture = architecture()[0]

        os_info_layout.addWidget(QLabel(f"OS: {os_name} {os_release} ({os_architecture})"))
        os_info_layout.addWidget(QLabel(f"Version: {os_version}"))

        os_info_box.setLayout(os_info_layout)
        layout.addWidget(os_info_box)

        build_info_box.setLayout(build_info_layout)
        layout.addWidget(build_info_box)

        about_dialog.setLayout(layout)
        about_dialog.exec()

def main():
    app = QApplication([])
    app.setStyle('Fusion')
    window = MetalSlugFontReborn()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
