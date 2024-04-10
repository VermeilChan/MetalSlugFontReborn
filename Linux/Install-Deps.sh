#!/bin/bash

cd ..
echo "MetalSlugFontReborn dependencies installer"
echo "This script will download the required dependencies for MetalSlugFontReborn."

read -p "Which package manager do you use? (apt, dnf, pacman, zypper): " package_manager

echo "Installing dependencies..."
case $package_manager in
    apt)
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv libxcb-cursor0
        ;;
    dnf)
        sudo dnf update
        sudo dnf install -y python3 python3-pip python3-virtualenv xcb-util-cursor
        ;;
    pacman)
        sudo pacman -Syu --noconfirm python-pip python-virtualenv xcb-util-cursor
        ;;
    zypper)
        sudo zypper refresh
        sudo zypper install -y python3 python3-pip python3-virtualenv libxcb-cursor0
        ;;
    *)
        echo "Invalid package manager."
        exit 1
        ;;
esac

echo "Creating and activating a virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

echo "Deactivating the virtual environment..."
deactivate

cat <<EOF

|-----------------------------------------|
|     Setup completed successfully.       |
| Now, please run the following command:  |
|             bash Run.sh                 |
|-----------------------------------------|

EOF
