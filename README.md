# MetalSlugFontReborn

<p align="center">
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn/graphs/contributors">
    <img alt="Contributors" src="https://img.shields.io/github/contributors/VermeilChan/MetalSlugFontReborn?color=green" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn/releases">
    <img alt="Latest Release" src="https://img.shields.io/github/release/VermeilChan/MetalSlugFontReborn?color=blue" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn/releases">
    <img alt="Downloads" src="https://img.shields.io/github/downloads/VermeilChan/MetalSlugFontReborn/total?color=orange" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/VermeilChan/MetalSlugFontReborn?color=purple" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn/issues">
    <img alt="Open Issues" src="https://img.shields.io/github/issues/VermeilChan/MetalSlugFontReborn?color=red" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn/pulls">
    <img alt="Open Pull Requests" src="https://img.shields.io/github/issues-pr/VermeilChan/MetalSlugFontReborn?color=yellow" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn/commits">
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/VermeilChan/MetalSlugFontReborn?color=darkcyan" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/VermeilChan/MetalSlugFontReborn?color=yellowgreen" />
  </a>
  <a href="https://github.com/VermeilChan/MetalSlugFontReborn">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/VermeilChan/MetalSlugFontReborn?color=lightcoral" />
  </a>
</p>

_This Branch Is For PySide2 (Qt 5.15.2.1), Python 3.10.11_<br>
_Why Does It Exist?, To Support Older PC'S :)_

A tool for creating images with the Metal Slug font.

<p style="font-size: medium">
If you have a GitHub account and have found this repository helpful, please consider starring ★ it.
</p>

## Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installing MetalSlugFontReborn](#installing-metalslugfontreborn)
- [Examples and Supported Characters](#examples-and-supporteds-characters)
- [How to Contribute](#how-to-contribute)
- [License](#license)
- [Credits](#credits)

## Features

- Easily transform text into images using the Metal Slug font.
- Supports uppercase and lowercase letters (A-Z, a-z), digits (0-9), symbols (♥-★), and multiple colors.
- Supports operating systems, including Windows, Linux, macOS.

## System Requirements

#### Operating Systems

| Operating System | Supported Versions                                 | Architecture   |
|------------------|----------------------------------------------------|----------------|
| Windows          | 11, 10, 8.1, 7                                     | 64-bit, 32-bit |
| GNU/Linux        | Ubuntu 18.04, Fedora 38, Arch Linux, OpenSUSE 15.4 | 64-bit, 32-bit |
| macOS            | 15, 14, 13, 12, 11, 10.13                          | 64-bit, 32-bit |

_Uhh, I don't think pyinstaller supports some of the versions here because they reached EOL.<br>_
_So you might want to use an older version of pyinstaller._

## Installing MetalSlugFontReborn

To download and use MetalSlugFontReborn, refer to the [docs](Docs/INSTALL-SELECT.md) here.

## Examples and Supported Characters

See examples of the [images generated](Docs/EXAMPLES.md) and the [supported characters](Docs/SUPPORTED.md).

## How to Contribute

If you find issues or have ideas for improvements, please:

- [Report an issue](https://github.com/VermeilChan/MetalSlugFontReborn/issues)
- [Submit a pull request](https://github.com/VermeilChan/MetalSlugFontReborn/pulls)

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Credits

I want to say a big thank you to the individuals who helped me.

- [SNK Corporation](https://www.snk-corp.co.jp): Used some of their assets.
- [SikroxMemer](https://github.com/SikroxMemer): for assisting in the development of the program and webapp.
- [Division 六](https://6th-divisions-den.com): inspiring me to create the program in the first place and providing assets for fonts 1 to 4.
- [GussPrint](https://www.spriters-resource.com/submitter/Gussprint): for providing assets for font 5.
- [BinRich](https://discord.com/users/477459550904254464): for providing diacritic marks.

### Third-party

- [PySide2](https://pypi.org/project/PySide2/): For the GUI
- [Pillow](https://python-pillow.org): For image processing
- [PyInstaller](https://pyinstaller.org/en/stable): For compiling the program
