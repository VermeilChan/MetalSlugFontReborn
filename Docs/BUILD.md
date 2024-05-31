# Table of contents

- [Platforms](#platforms)
- [Get the source code](#get-the-source-code)
- [Dependencies](#dependencies)
   - [Windows dependencies](#windows-dependencies)
   - [Linux dependencies](#linux-dependencies)
- [Compiling](#compiling)
   - [Windows details](#windows-details)
   - [Linux details](#linux-details)

# Platforms

You should be able to compile Aseprite successfully on the following
platforms:

- Windows 11 and 10 (Qt), Windows 11, 10, 8.1 (Console) x86-64.
- GNU/Linux Debian 12.5, Ubuntu 24.04, Fedora 40, Arch Linux, OpenSUSE x86-64.

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

- [Python](https://www.python.org/)
- [PyInstaller](https://pyinstaller.org/en/stable/)
- [PySide6](https://pypi.org/project/PySide6/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [Python Prompt Toolkit 3.0](https://python-prompt-toolkit.readthedocs.io/en/master/)

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
# Qt Version
pyinstaller --noconfirm --onedir --windowed --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets;Assets/" --add-data "Src/special_characters.py;." --add-data "Src/image_generation.py;." --add-data "Src/themes.py;." --add-data "Src/utils.py;." --add-data "Src/info.py;." --add-data "Docs/SUPPORTED.txt;."  "Src/qt-version.py"
```
```sh
# Console Version
pyinstaller --noconfirm --onedir --console --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets;Assets/" --add-data "Src/special_characters.py;." --add-data "Src/image_generation.py;." --add-data "Src/info.py;." --add-data "Docs/SUPPORTED.txt;."  "Src/console-version.py"
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

## Linux details

Open the terminal and run:

```sh
cd MetalSlugFontReborn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```sh
# Qt Version
pyinstaller --noconfirm --onedir --windowed --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets:Assets/" --add-data "Src/special_characters.py:." --add-data "Src/image_generation.py:." --add-data "Src/themes.py:." --add-data "Src/utils.py:." --add-data "Src/info.py:." --add-data "Docs/SUPPORTED.txt:."  "Src/qt-version.py"
```
```sh
# Console Version
pyinstaller --noconfirm --onedir --console --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets:Assets/" --add-data "Src/special_characters.py:." --add-data "Src/image_generation.py:." --add-data "Src/info.py:." --add-data "Docs/SUPPORTED.txt:."  "Src/console-version.py"
```

- Move the `Assets` folder and `SUPPORTED.txt` out of `_internal` folder to `dist/MetalSlugFontReborn`.
- The executable will be located at `dist/MetalSlugFontReborn/MetalSlugFontReborn`
