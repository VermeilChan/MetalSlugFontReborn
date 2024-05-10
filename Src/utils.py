from json import load, dump
from platform import system, version, release, architecture
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QDialog
from themes import light_mode, dark_mode
from info import msfr_version, pyinstaller_version, pyside6_version, pillow_version, build_date

def set_theme(theme_name):
    palette = light_mode() if theme_name == "Light" else dark_mode()
    QApplication.setPalette(palette)
    save_theme(theme_name)

def save_theme(theme_name):
    with open('config.json', 'w', encoding='utf-8') as f:
        dump({"theme": theme_name}, f)

def load_theme():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            data = load(f)
            theme_name = data.get("theme")
            if theme_name:
                set_theme(theme_name)
    except FileNotFoundError:
        pass

def linux_info():
    os_info = {}
    with open('/etc/os-release', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            os_info[key] = value.strip('"')

    pretty_name = os_info.get('PRETTY_NAME') or system()
    os_version = os_info.get('VERSION') or release()

    return pretty_name, os_version

def about_msfr(parent):
    about_window = QDialog(parent)
    about_window.setWindowTitle("About")

    main_layout = QVBoxLayout()

    header_layout = QHBoxLayout()

    icon_label = QLabel()
    pixmap = QPixmap("Assets/Icons/Raubtier.png")
    icon_label.setPixmap(pixmap)
    header_layout.addWidget(icon_label)

    info_layout = QVBoxLayout()
    info_layout.addWidget(QLabel(f"MetalSlugFontReborn ({architecture()[0]})"))
    info_layout.addWidget(QLabel("GPL-3.0 License"))

    github_link = QLabel('<a href="https://github.com/VermeilChan/MetalSlugFontReborn">GitHub Repository</a>')
    github_link.setOpenExternalLinks(True)
    info_layout.addWidget(github_link)

    header_layout.addLayout(info_layout)
    main_layout.addLayout(header_layout)

    os_info_layout = QVBoxLayout()

    if system() == 'Linux':
        os_name, os_version = linux_info()
        os_info_layout.addWidget(QLabel(f"OS: {os_name}"))
        os_info_layout.addWidget(QLabel(f"Version: {os_version}"))
    elif system() == 'Windows':
        os_info_layout.addWidget(QLabel(f"OS: {system()} {release()}"))
        os_info_layout.addWidget(QLabel(f"Version: {version()}"))

    os_info_group = QGroupBox("Operating System:")
    os_info_group.setLayout(os_info_layout)
    main_layout.addWidget(os_info_group)

    build_info_layout = QVBoxLayout()

    build_info_layout.addWidget(QLabel(f"Version: {msfr_version}"))
    build_info_layout.addWidget(QLabel(f"Pyinstaller: {pyinstaller_version}"))
    build_info_layout.addWidget(QLabel(f"PySide6: {pyside6_version}"))
    build_info_layout.addWidget(QLabel(f"Pillow: {pillow_version}"))
    build_info_layout.addWidget(QLabel(f"Build date: {build_date}"))

    build_info_group = QGroupBox("Build Information:")
    build_info_group.setLayout(build_info_layout)
    main_layout.addWidget(build_info_group)

    about_window.setLayout(main_layout)
    about_window.exec()
