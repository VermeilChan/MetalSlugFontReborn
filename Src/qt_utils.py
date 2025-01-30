from configparser import ConfigParser
from platform import system, architecture, win32_ver, win32_edition, freedesktop_os_release, mac_ver, machine
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, 
                            QHBoxLayout, QGroupBox, QDialog)
from PIL import __version__ as pillow_version
from PySide6 import __version__ as pyside6_version
from PyInstaller import __version__ as pyinstaller_version
from info import msfr_version, build_date
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

def readable_size(size_bytes):
    units = ["bytes", "KB", "MB"]
    size = size_bytes
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024

def normalize_architecture(arch):
    return {
        "x86_64": "64-Bit",
        "64bit": "64-Bit",
        "arm64": "ARM64",
        "aarch64": "ARM64",
    }.get(arch, arch)

def get_windows_info():
    try:
        version = win32_ver()[0]
        edition = win32_edition()
        arch = normalize_architecture(architecture()[0])
        return f"Windows {version} {edition} {arch}"
    except Exception as error:
        return f"Windows (Error: {error})"

def get_linux_info():
    try:
        distro = freedesktop_os_release()
        name = distro.get("NAME", "Linux")
        pretty_name = distro.get("PRETTY_NAME", "")
        version = distro.get("VERSION", "")
        version_id = distro.get("VERSION_ID", "")
        arch = normalize_architecture(architecture()[0])

        if pretty_name:
            return f"{pretty_name} {arch}"
        if version:
            return f"{version} {arch}"
        
        components = [name]
        if version_id:
            components.append(version_id)
        return f"{' '.join(components)} {arch}"

    except OSError:
        return f"Linux {normalize_architecture(architecture()[0])}"
    except Exception as error:
        return f"Linux (Error: {error})"

def get_macos_info():
    try:
        version = mac_ver()[0]
        arch = normalize_architecture(machine())
        return f"macOS {version} {arch}"
    except Exception as error:
        return f"macOS (Error: {error})"

def get_os_info():
    system_name = system()
    handlers = {
        "Windows": get_windows_info,
        "Linux": get_linux_info,
        "Darwin": get_macos_info,
    }
    handler = handlers.get(system_name)
    return handler() if handler else f"Unknown OS (System: {system_name})"

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
    
    github = QLabel('<a href="https://github.com/VermeilChan/MetalSlugFontReborn">GitHub Repository</a>')
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
        f"Pillow: {pillow_version}",
        f"Build date: {build_date}"
    ]:
        build_info.addWidget(QLabel(text))
    
    layout.addWidget(create_group("Build Information:", build_info))
    dialog.setLayout(layout)
    dialog.exec()
