from platform import system, version, release, architecture
from semantic_version import Version
from requests import get, RequestException
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
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
    4: ["Blue", "Orange-1", "Yellow"],
    5: ["Orange-1"]
}

class ImageGenerator:
    icon_path = "Assets/Icons/Raubtier.ico"

    @staticmethod
    def generate_and_display_image(text, font, color):
        if not text.strip():
            QMessageBox.critical(None, "MetalSlugFontReborn", "Input text is empty. Please enter some text.")
            return

        try:
            filename = generate_filename(text)
            font_paths = get_font_paths(font, color)
            image_path, error_message_generate = generate_image(text, filename, font_paths)

            if error_message_generate:
                QMessageBox.critical(None, "MetalSlugFontReborn", f"Error: {error_message_generate}")
            else:
                QMessageBox.information(None, "MetalSlugFontReborn", f"Image saved as:\n\n{image_path}\n")
        except Exception as e:
            QMessageBox.critical(None, "MetalSlugFontReborn", str(e))

class UpdaterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Updater")
        self.setWindowIcon(QIcon("Assets/Icons/Raubtier.ico"))

        layout = QVBoxLayout()

        self.status_label = QLabel("Checking for updates...")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.check_for_updates()

    def check_for_updates(self):
        owner = "VermeilChan"
        repo = "MetalSlugFontReborn"
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

        try:
            response = get(url)
            response.raise_for_status()
            latest_release = response.json()

            tag_name = "1.7.0"
            latest_version_str = latest_release['tag_name']
            latest_version_str = latest_version_str.lstrip('v')
            latest_version = Version(latest_version_str)
            current_version = Version(tag_name)

            if latest_version == current_version:
                self.status_label.setText("You are already using the latest version.")
            elif latest_version > current_version:
                self.status_label.setText(f"A new version (v{latest_version}) is available!")
            else:
                self.status_label.setText("Your version is newer than the latest version.")

        except RequestException as e:
            self.status_label.setText("Failed to check for updates.")
            print(f"Error: {e}")

class MetalSlugFontReborn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MetalSlugFontReborn")
        self.setWindowIcon(QIcon(ImageGenerator.icon_path))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel("Text to Generate:"))
        self.text_entry = QLineEdit()
        self.text_entry.setMinimumWidth(600)
        layout.addWidget(self.text_entry)

        layout.addWidget(QLabel("Select Font:"))
        self.font_combobox = QComboBox()
        self.font_combobox.addItems(map(str, sorted(VALID_COLORS_BY_FONT.keys())))
        layout.addWidget(self.font_combobox)

        layout.addWidget(QLabel("Select Color:"))
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

        self.updater_action = help_menu.addAction("Check for Updates")
        self.updater_action.triggered.connect(self.open_updater)

        self.setMaximumSize(self.size())

    def open_updater(self):
        updater_dialog = UpdaterDialog(self)
        updater_dialog.exec()

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

        text = text.upper() if font == 5 else text

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

        build_info_layout.addWidget(QLabel("Version: 1.7.0 (Dev)"))
        build_info_layout.addWidget(QLabel("Pyinstaller: 6.4.0"))
        build_info_layout.addWidget(QLabel("PySide6: 6.6.2"))
        build_info_layout.addWidget(QLabel("Build date: Feb XX 2024"))

        os_info_box = QGroupBox("Operating System")
        os_info_layout = QVBoxLayout()

        os_info_layout.addWidget(QLabel(f"OS: {system()} {release()} ({architecture()[0]})"))
        os_info_layout.addWidget(QLabel(f"Version: {version()}"))

        os_info_box.setLayout(os_info_layout)
        layout.addWidget(os_info_box)

        build_info_box.setLayout(build_info_layout)
        layout.addWidget(build_info_box)

        about_dialog.setLayout(layout)
        about_dialog.exec()

def main():
    app = QApplication([])
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon(ImageGenerator.icon_path))
    window = MetalSlugFontReborn()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
