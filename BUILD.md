# Table of contents

- [Platforms](#platforms)
- [Dependencies](#dependencies)
   - [Windows dependencies](#dependencies)
   - [Linux dependencies](#linux-dependencies)
   - [macOS dependencies](#dependencies)
- [Compiling](#compiling)
   - [Windows details](#windows-details)
   - [Linux details](#linux-and-macOS-details)
   - [macOS details](#linux-and-macOS-details)

# Platforms

You should be able to compile MetalSlugFontReborn successfully on the following
platforms:

| Operating System | Supported Versions                                 | Architecture   |
|------------------|----------------------------------------------------|----------------|
| Windows          | 11, 10, 8.1, 7                                     | 64-bit, 32-bit |
| GNU/Linux        | Ubuntu 18.04, Fedora 38, Arch Linux, OpenSUSE 15.4 | 64-bit, 32-bit |
| macOS            | 15, 14, 13, 12, 11, 10.13                          | 64-bit, 32-bit |

# Dependencies

To compile MetalSlugFontReborn you will need the following:

- [Python](https://www.python.org/) 3.10.11
- [PyInstaller](https://pyinstaller.org/en/stable/) 6.11.0 or later
- [PySide2](https://pypi.org/project/PySide2/) 5.15.2.1 or later
- [Pillow](https://pillow.readthedocs.io/en/stable/) 11.0.0 or later

# Compiling

## Windows details

Open a the command prompt (`cmd.exe`) and run:

```sh
pyinstaller --noconfirm --onedir --windowed --optimize "2" --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets;Assets/" --add-data "Src/special_characters.py;." --add-data "Src/image_generation.py;." --add-data "Src/themes.py;." --add-data "Src/qt_utils.py;." --add-data "Src/info.py;."  "Src/qt-version.py"
```

---

## Linux dependencies

You will need the following dependencies on Ubuntu/Debian:
```sh
sudo apt install -y python3 python3-pip python3-venv libxcb-cursor0
```
On Fedora:
```sh
sudo dnf install -y python3 python3-pip python3-virtualenv xcb-util-cursor
```
On Arch:
```sh
sudo pacman -Syu --noconfirm python-pip python-virtualenv xcb-util-cursor
```
On SUSE:
```sh
sudo zypper install -y python3 python3-pip python3-virtualenv libxcb-cursor0
```

## Linux and MacOS details

Open the terminal and run:

```sh
pyinstaller --noconfirm --onedir --windowed --optimize "2" --strip --name "MetalSlugFontReborn" --clean --add-data "Assets:Assets/" --add-data "Src/special_characters.py:." --add-data "Src/image_generation.py:." --add-data "Src/themes.py:." --add-data "Src/qt_utils.py:." --add-data "Src/info.py:." --add-data "Docs/SUPPORTED.txt:."  "Src/qt-version.py"
```
