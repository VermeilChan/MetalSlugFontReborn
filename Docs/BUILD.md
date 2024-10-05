# Table of contents

- [Platforms](#platforms)
- [Get the source code](#get-the-source-code)
- [Dependencies](#dependencies)
   - [Windows dependencies](#dependencies)
   - [Linux dependencies](#linux-dependencies)
   - [MacOS dependencies](#dependencies)
- [Compiling](#compiling)
   - [Windows details](#windows-details)
   - [Linux details](#linux-and-macOS-details)
   - [MacOS details](#linux-and-macOS-details)

# Platforms

You should be able to compile MetalSlugFontReborn successfully on the following
platforms:

| Operating System | Supported Versions                                         | Architecture |
|------------------|------------------------------------------------------------|--------------|
| Windows          | 11, 10                                                     | 64-bit       |
| GNU/Linux        | Debian 12, Ubuntu 22.04, Fedora 40, Arch Linux, OpenSUSE   | 64-bit       |
| macOS            | 15, 14, 13, 12, 11, 10.15                                  | 64-bit       |

# Get the source code

You can get the source code by downloading the archive `MetalSlugFontReborn-v1.x-Source.zip` from the [latest release](https://github.com/VermeilChan/MetalSlugFontReborn/releases/latest).

Or you can clone the repository using the following command:
```sh
git clone https://github.com/VermeilChan/MetalSlugFontReborn.git
```
To update an existing clone you can use the following commands:
```sh
cd MetalSlugFontReborn
git pull
```
# Dependencies

To compile MetalSlugFontReborn you will need the following:

- [Python](https://www.python.org/) 3.9 or later
- [PyInstaller](https://pyinstaller.org/en/stable/) 6.10.0 or later
- [PySide6-Essentials](https://pypi.org/project/PySide6/) 6.7.3 or later
- [Pillow](https://pillow.readthedocs.io/en/stable/) 10.4.0 or later
- [Python Prompt Toolkit 3.0](https://python-prompt-toolkit.readthedocs.io/en/master/) 3.0.48 or later

# Compiling

## Windows details

Open a the command prompt (`cmd.exe`) and run:

```sh
cd MetalSlugFontReborn
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
```sh
pyinstaller --noconfirm --onedir --windowed --optimize "2" --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets;Assets/" --add-data "Src/special_characters.py;." --add-data "Src/image_generation.py;." --add-data "Src/themes.py;." --add-data "Src/qt_utils.py;." --add-data "Src/info.py;." --add-data "Docs/SUPPORTED.txt;."  "Src/qt-version.py"
```

- Move the `Assets` folder and `SUPPORTED.txt` out of `_internal` folder to `dist/MetalSlugFontReborn`.
- The executable will be located at `dist/MetalSlugFontReborn/MetalSlugFontReborn.exe`

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
cd MetalSlugFontReborn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```sh
pyinstaller --noconfirm --onedir --windowed --optimize "2" --strip --name "MetalSlugFontReborn" --clean --add-data "Assets:Assets/" --add-data "Src/special_characters.py:." --add-data "Src/image_generation.py:." --add-data "Src/themes.py:." --add-data "Src/qt_utils.py:." --add-data "Src/info.py:." --add-data "Docs/SUPPORTED.txt:."  "Src/qt-version.py"
```

- Move the `Assets` folder and `SUPPORTED.txt` out of `_internal` folder to `dist/MetalSlugFontReborn`.
- The executable will be located at `dist/MetalSlugFontReborn/MetalSlugFontReborn`
