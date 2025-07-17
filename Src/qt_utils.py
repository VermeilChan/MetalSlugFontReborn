from configparser import ConfigParser
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, 
                            QHBoxLayout, QGroupBox, QDialog)
from cv2 import __version__ as opencv_version
from PySide6 import __version__ as pyside6_version
from PyInstaller import __version__ as pyinstaller_version
from utils import msfr_version, build_date, get_os_info
from themes import light_mode, dark_mode, dracula_mode, arc_dark_mode, monokai_mode

theme_list = {
    "Light": light_mode,
    "Dark": dark_mode,
    "Dracula": dracula_mode,
    "Arc Dark": arc_dark_mode,
    "Monokai": monokai_mode
}

def set_theme(theme_name):
    palette = theme_list.get(theme_name, dark_mode)()
    QApplication.setPalette(palette)
    save_theme(theme_name)

def save_theme(theme_name):
    config = ConfigParser()
    config["Settings"] = {"theme": theme_name}
    with open("config.ini", "w", encoding="utf-8") as f:
        config.write(f)

def load_theme():
    config = ConfigParser()
    config.read("config.ini", encoding="utf-8")
    if theme_name := config.get("Settings", "theme", fallback=""):
        set_theme(theme_name)

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
    
    github = QLabel('<a href="https://github.com/Mitra-88/MetalSlugFontReborn">GitHub Repository</a>')
    github.setOpenExternalLinks(True)
    info.addWidget(github)

    header.addWidget(icon)
    header.addLayout(info)
    layout.addLayout(header)

    os_layout = QVBoxLayout()
    os_layout.addWidget(QLabel(f"OS: {get_os_info()}"))
    layout.addWidget(create_group("Operating System:", os_layout))

    build_info = QVBoxLayout()
    for text in [
        f"Version: {msfr_version}",
        f"Pyinstaller: {pyinstaller_version}",
        f"PySide6: {pyside6_version}",
        f"OpenCV: {opencv_version}",
        f"Build date: {build_date}"
    ]:
        build_info.addWidget(QLabel(text))
    
    layout.addWidget(create_group("Build Information:", build_info))
    dialog.setLayout(layout)
    dialog.exec()
