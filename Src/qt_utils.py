from configparser import ConfigParser
from platform import system, version, release, architecture
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QDialog
from themes import light_mode, dark_mode, dracula_mode, arc_dark_mode, monokai_mode
from info import msfr_version, pyinstaller_version, pyside2_version, pillow_version, build_date


def set_theme(theme_name):
    if theme_name == "Light":
        palette = light_mode()
    elif theme_name == "Dark":
        palette = dark_mode()
    elif theme_name == "Dracula":
        palette = dracula_mode()
    elif theme_name == "Monokai":
        palette = monokai_mode()
    elif theme_name == "Arc Dark":
        palette = arc_dark_mode()
    else:
        palette = dark_mode()

    QApplication.setPalette(palette)
    save_theme(theme_name)


def save_theme(theme_name):
    config = ConfigParser()
    config["Settings"] = {"theme": theme_name}
    with open("config.ini", "w", encoding="utf-8") as f:
        config.write(f)


def load_theme():
    config = ConfigParser()
    try:
        config.read("config.ini", encoding="utf-8")
        theme_name = config.get("Settings", "theme", fallback=None)
        if theme_name:
            set_theme(theme_name)
    except FileNotFoundError:
        pass


def readable_size(size_bytes):
    for unit in ["bytes", "KB", "MB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024


def get_linux_info():
    os_info = {}
    with open("/etc/os-release", "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            os_info[key] = value.strip('"')

    return os_info.get("PRETTY_NAME") or system(), os_info.get("VERSION") or release()


def get_os_info():
    os_name = system()
    os_release = release()
    os_version = version()

    if os_name == "Linux":
        return get_linux_info()
    return f"{os_name} {os_release}", os_version


def group_box(title, layout):
    group_box = QGroupBox(title)
    group_box.setLayout(layout)
    return group_box


def about_section(parent):
    about_window = QDialog(parent)
    about_window.setWindowTitle("About")

    main_layout = QVBoxLayout()

    header_layout = QHBoxLayout()
    icon_label = QLabel()
    pixmap = QPixmap("Assets/Icons/Raubtier.png")
    icon_label.setPixmap(pixmap)

    info_layout = QVBoxLayout()
    info_layout.addWidget(QLabel(f"MetalSlugFontReborn ({architecture()[0]})"))
    info_layout.addWidget(QLabel("GPL-3.0 Licensed"))

    github_link = QLabel(
        '<a href="https://github.com/VermeilChan/MetalSlugFontReborn">GitHub Repository</a>'
    )
    github_link.setOpenExternalLinks(True)
    info_layout.addWidget(github_link)

    header_layout.addWidget(icon_label)
    header_layout.addLayout(info_layout)
    main_layout.addLayout(header_layout)

    os_name, os_version = get_os_info()
    os_info_layout = QVBoxLayout()
    os_info_layout.addWidget(QLabel(f"OS: {os_name}"))
    os_info_layout.addWidget(QLabel(f"Version: {os_version}"))

    main_layout.addWidget(group_box("Operating System:", os_info_layout))

    build_info_layout = QVBoxLayout()
    build_info_layout.addWidget(QLabel(f"Version: {msfr_version}"))
    build_info_layout.addWidget(QLabel(f"Pyinstaller: {pyinstaller_version}"))
    build_info_layout.addWidget(QLabel(f"PySide2: {pyside2_version}"))
    build_info_layout.addWidget(QLabel(f"Pillow: {pillow_version}"))
    build_info_layout.addWidget(QLabel(f"Build date: {build_date}"))

    main_layout.addWidget(group_box("Build Information:", build_info_layout))

    about_window.setLayout(main_layout)
    about_window.exec_()
