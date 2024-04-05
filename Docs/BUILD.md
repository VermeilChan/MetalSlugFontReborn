# Building MetalSlugFontReborn

## Windows

### Requirements

- [Python](https://www.python.org/downloads/).
- [Git](https://gitforwindows.org/).

### Steps

- Clone the repository

```sh
git clone https://github.com/VermeilChan/MetalSlugFontReborn.git
```

- Navigate to the MetalSlugFontReborn folder

```sh
cd MetalSlugFontReborn
```

- Create a virtual environment and activate it

```sh
py -m venv .venv
.venv\Scripts\activate
```

- Install dependencies

```sh
pip install -r requirements.txt
```

- Build MetalSlugFontReborn with PyInstaller

```sh
# GUI VERSION
pyinstaller --noconfirm --onedir --windowed --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets;Assets/" --add-data "Src/constants.py;." --add-data "Src/main.py;."  "Src/windowed-version.py"

# CLI VERSION
pyinstaller --noconfirm --onedir --console --icon "Assets/Icons/Raubtier.ico" --name "MetalSlugFontReborn" --clean --version-file "versionfile.txt" --add-data "Assets;Assets/" --add-data "Src/constants.py;." --add-data "Src/main.py;." "Src/console-version.py"
```

- Move the `Assets` out of `_internal` to `dist/MetalSlugFontReborn`.
- Run the program: `dist/MetalSlugFontReborn/MetalSlugFontReborn.exe`.

## Linux

_Note: Some distributions require other packages to be installed._

### Steps

- Clone the repository

```sh
git clone https://github.com/VermeilChan/MetalSlugFontReborn.git
```

- Navigate to the MetalSlugFontReborn folder

```sh
cd MetalSlugFontReborn
```

- Install required packages

```sh
# DEPENDS ON YOUR DISTRIBUTION
sudo apt install python3 python3-pip python3-venv
```

- Create a virtual environment and activate it

```sh
python3 -m venv .venv
source .venv/bin/activate
```

- Install python dependencies

```sh
pip install -r requirements.txt
```

- Build MetalSlugFontReborn with PyInstaller

```sh
# GUI VERSION
pyinstaller --noconfirm --onedir --windowed --name "MetalSlugFontReborn" --clean --add-data "Assets:Assets/" --add-data "Src/constants.py:." --add-data "Src/main.py:."  "Src/windowed-version.py"

# CLI VERSION
pyinstaller --noconfirm --onedir --console --name "MetalSlugFontReborn" --clean --add-data "Assets:Assets/" --add-data "Src/constants.py:." --add-data "Src/main.py:." "Src/console-version.py"
```

- Move the `Assets` out of `_internal` to `dist/MetalSlugFontReborn`.
- Run the program: `dist/MetalSlugFontReborn/MetalSlugFontReborn.exe`.

## macOS

- Idk :(