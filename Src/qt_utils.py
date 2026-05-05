from configparser import ConfigParser

from PIL import __version__ as pillow_version
from PyInstaller import __version__ as pyinstaller_version
from PySide6 import __version__ as pyside6_version
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
                               QLabel, QVBoxLayout)

from themes import dark_mode, light_mode, tokyo_night
from utils import build_date, get_system_info, msfr_version

theme_list = {
    "Light": light_mode,
    "Dark": dark_mode,
    "Tokyo Night": tokyo_night,
}

CONFIG_FILE = "config.ini"

def save_config(key, value):
    config = ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    if "Settings" not in config:
        config["Settings"] = {}
    config["Settings"][key] = str(value)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)

def load_config(key, fallback=None):
    config = ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    return config.get("Settings", key, fallback=fallback)

def set_theme(theme_name=None):
    theme_name = theme_name or load_config("theme")
    if theme_name not in theme_list:
        return
    palette = theme_list[theme_name]()
    QApplication.setPalette(palette)
    save_config("theme", theme_name)

def create_group(title, content):
    group = QGroupBox(title)
    group.setLayout(content)
    return group

def about_section(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle("About")
    layout = QVBoxLayout()

    header = QHBoxLayout()
    icon = QLabel()
    icon.setPixmap(QPixmap("Assets/Icons/Raubtier.png"))

    info = QVBoxLayout()
    info.addWidget(QLabel("MetalSlugFontReborn"))
    info.addWidget(QLabel("GPL-3.0 Licensed"))

    github = QLabel(
        '<a href="https://github.com/Mitra-88/MetalSlugFontReborn">GitHub Repository</a>'
    )
    github.setOpenExternalLinks(True)
    info.addWidget(github)

    header.addWidget(icon)
    header.addLayout(info)
    layout.addLayout(header)

    os_layout = QVBoxLayout()
    os_layout.addWidget(QLabel(f"OS: {get_system_info()}"))
    layout.addWidget(create_group("Operating System:", os_layout))

    build_info = QVBoxLayout()
    for text in [
        f"Version: {msfr_version}",
        f"Pyinstaller: {pyinstaller_version}",
        f"PySide6: {pyside6_version}",
        f"Pillow: {pillow_version}",
        f"Build date: {build_date}",
    ]:
        build_info.addWidget(QLabel(text))

    layout.addWidget(create_group("Build Information:", build_info))
    dialog.setLayout(layout)
    dialog.exec()
