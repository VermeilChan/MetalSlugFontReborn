from configparser import ConfigParser
from platform import system, version, release, architecture
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QDialog,
)
from themes import light_mode, dark_mode
from info import (
    msfr_version,
    pyinstaller_version,
    pyside2_version,
    pillow_version,
    build_date,
    config_file,
)


def set_theme(theme_name):
    palette = light_mode() if theme_name == "Light" else dark_mode()
    QApplication.setPalette(palette)
    save_theme(theme_name)


def save_theme(theme_name):
    config = ConfigParser()
    config["Settings"] = {
        "theme": theme_name,
    }
    with open(config_file, "w", encoding="utf-8") as f:
        config.write(f)


def load_theme():
    config = ConfigParser()
    try:
        config.read(config_file, encoding="utf-8")
        theme_name = config.get("Settings", "theme", fallback=None)
        if theme_name:
            set_theme(theme_name)
    except FileNotFoundError:
        pass


def get_linux_info():
    os_info = {}
    with open("/etc/os-release", "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            os_info[key] = value.strip('"')

    pretty_name = os_info.get("PRETTY_NAME") or system()
    os_version = os_info.get("VERSION") or release()

    return pretty_name, os_version


def get_os_info():
    if system() == "Linux":
        return get_linux_info()
    elif system() == "Windows":
        return f"{system()} {release()}", version()

    return system(), release()


def about_section(parent):
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
    info_layout.addWidget(QLabel("GPL-3.0 Licensed"))

    github_link = QLabel(
        '<a href="https://github.com/VermeilChan/MetalSlugFontReborn">GitHub Repository</a>'
    )
    github_link.setOpenExternalLinks(True)
    info_layout.addWidget(github_link)

    header_layout.addLayout(info_layout)
    main_layout.addLayout(header_layout)

    os_name, os_version = get_os_info()
    os_info_layout = QVBoxLayout()
    os_info_layout.addWidget(QLabel(f"OS: {os_name}"))
    os_info_layout.addWidget(QLabel(f"Version: {os_version}"))

    os_info_group = QGroupBox("Operating System:")
    os_info_group.setLayout(os_info_layout)
    main_layout.addWidget(os_info_group)

    build_info_layout = QVBoxLayout()
    build_info_layout.addWidget(QLabel(f"Version: {msfr_version}"))
    build_info_layout.addWidget(QLabel(f"Pyinstaller: {pyinstaller_version}"))
    build_info_layout.addWidget(QLabel(f"PySide2: {pyside2_version}"))
    build_info_layout.addWidget(QLabel(f"Pillow: {pillow_version}"))
    build_info_layout.addWidget(QLabel(f"Build date: {build_date}"))

    build_info_group = QGroupBox("Build Information:")
    build_info_group.setLayout(build_info_layout)
    main_layout.addWidget(build_info_group)

    about_window.setLayout(main_layout)
    about_window.exec_()
