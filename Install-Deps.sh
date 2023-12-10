#!/bin/bash

echo "This script will download the required dependencies to use MetalSlugFontReborn."
echo "It will automatically download Python 3, pip, venv, and optionally, xcb for GUI support."
echo

read -p "Do you want to continue? (y/n): " install_dependencies
echo

if [ "$install_dependencies" != "y" ]; then
    echo "Exiting script. No dependencies will be installed."
    exit 0
fi
echo

read -p "Do you want to use the GUI version? (y/n): " install_xcb_libraries
echo

if [ "$install_xcb_libraries" != "y" ]; then
    echo "Skipping installation of libraries for GUI support."
else
    read -p "Enter your package manager (apt/dnf/pacman/zypper): " package_manager
    echo

    case $package_manager in
        apt | dnf | pacman | zypper)
            ;;
        *)
            echo "Error: Invalid package manager. Please enter one of the following: apt, dnf, pacman, zypper."
            exit 1
            ;;
    esac
    echo

    echo "Please wait, downloading dependencies..."

    case $package_manager in
        apt)
            sudo apt update -y
            ;;
        dnf)
            sudo dnf update -y
            ;;
        pacman)
            sudo pacman -Syu --noconfirm
            ;;
        zypper)
            sudo zypper update -y
            ;;
    esac

    echo "Installing necessary libraries for GUI support..."
    case $package_manager in
        apt)
            sudo apt install libxcb-cursor0 -y
            ;;
        dnf)
            sudo dnf install xcb-util-cursor -y
            ;;
        pacman)
            sudo pacman -S xcb-util-cursor --noconfirm
            ;;
        zypper)
            sudo zypper install -y libxcb-cursor0
            ;;
    esac
fi

echo "Installing Python 3, pip, and venv..."
case $package_manager in
    apt | dnf)
        sudo $package_manager install python3 python3-pip python3-venv -y
        ;;
    pacman)
        sudo $package_manager -S python python-pip python-virtualenv --noconfirm
        ;;
    zypper)
        sudo $package_manager install -y python3 python3-pip python3-virtualenv
        ;;
esac

echo "Creating and activating virtual environment..."
python3 -m venv metalslugfontreborn
source metalslugfontreborn/bin/activate

echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

echo "Deactivating virtual environment..."
deactivate

echo "|-----------------------------------------|"
echo "| Now, please run the following command:  |"
echo "|             bash Run.sh                 |"
echo "|-----------------------------------------|"
echo
