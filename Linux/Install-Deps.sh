#!/bin/bash

echo "MetalSlugFontReborn dependencies installer"
echo "This script will download the required dependencies for MetalSlugFontReborn."

read -p "Which package manager do you use? (apt, dnf, pacman, zypper): " package_manager

case $package_manager in
    apt)
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv
        ;;
    dnf)
        sudo dnf update
        sudo dnf install -y python3 python3-pip python3-virtualenv
        ;;
    pacman)
        sudo pacman -Syu --noconfirm python-pip python-virtualenv
        ;;
    zypper)
        sudo zypper refresh
        sudo zypper install -y python3 python3-pip python3-virtualenv
        ;;
    *)
        echo "Invalid package manager."
        exit 1
        ;;
esac

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

deactivate

echo "Dependencies installed successfully :)"
echo "Run the program with `bash Run.sh`"
