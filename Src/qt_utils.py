from configparser import ConfigParser
from platform import system ,architecture, win32_ver, win32_edition, freedesktop_os_release, mac_ver, machine
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QDialog
from themes import light_mode, dark_mode, dracula_mode, arc_dark_mode, monokai_mode
from info import msfr_version,pyinstaller_version,pyside6_version,pillow_version,build_date


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
    size_units = ["bytes", "KB", "MB"]
    index = 0
    size = size_bytes
    while size >= 1024 and index < len(size_units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {size_units[index]}"

def normalize_architecture(architecture):
    arch_map = {
        "x86_64": "64-bit",
        "64bit": "64-bit",
        "arm64": "Arm64"
    }
    return arch_map.get(architecture, architecture)


def get_os_info():
    sys = system()

    if sys == "Windows":
        win_version, win_release, _, _ = win32_ver()
        win_edition = win32_edition()
        arch = normalize_architecture(architecture()[0])
        return f"Windows {win_version} {win_edition} {arch}"

    elif sys == "Linux":
        try:
            distro_info = freedesktop_os_release()
            pretty_name = distro_info.get("PRETTY_NAME", "")
            version = distro_info.get("VERSION", "")
            version_id = distro_info.get("VERSION_ID", "")
            arch = normalize_architecture(architecture()[0])

            if pretty_name:
                return f"{pretty_name} {arch}"
            elif version:
                return f"{version} {arch}"
            else:
                name = distro_info.get("NAME", "Linux")
                if version_id:
                    return f"{name} {version_id} {arch}"
                else:
                    return f"{name} {arch}"

        except OSError:
            return f"Linux {normalize_architecture(architecture()[0])}"

    elif sys == "Darwin":
        mac_version = mac_ver()[0]
        arch = normalize_architecture(machine())
        return f"macOS {mac_version} {arch}"

    else:
        return "Unable to get OS information (っ °Д °;)っ"

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
    info_layout.addWidget(QLabel(f"MetalSlugFontReborn"))
    info_layout.addWidget(QLabel("GPL-3.0 Licensed"))

    github_link = QLabel(
        '<a href="https://github.com/VermeilChan/MetalSlugFontReborn">GitHub Repository</a>'
    )
    github_link.setOpenExternalLinks(True)
    info_layout.addWidget(github_link)

    header_layout.addWidget(icon_label)
    header_layout.addLayout(info_layout)
    main_layout.addLayout(header_layout)

    os_info = get_os_info()
    os_info_layout = QVBoxLayout()
    os_info_layout.addWidget(QLabel(f"OS: {os_info}"))

    main_layout.addWidget(group_box("Operating System:", os_info_layout))

    build_info_layout = QVBoxLayout()
    build_info_layout.addWidget(QLabel(f"Version: {msfr_version}"))
    build_info_layout.addWidget(QLabel(f"Pyinstaller: {pyinstaller_version}"))
    build_info_layout.addWidget(QLabel(f"PySide6: {pyside6_version}"))
    build_info_layout.addWidget(QLabel(f"Pillow: {pillow_version}"))
    build_info_layout.addWidget(QLabel(f"Build date: {build_date}"))

    main_layout.addWidget(group_box("Build Information:", build_info_layout))

    about_window.setLayout(main_layout)
    about_window.exec()
