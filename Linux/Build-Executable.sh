#!/bin/bash

cd ..

echo "MetalSlugFontReborn Builder"

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

build_qt() {
    echo "Building Qt version..."
    pyinstaller --noconfirm --onedir --windowed --name "MetalSlugFontReborn" --clean \
                --add-data "Assets:Assets/" --add-data "Src/special_characters.py:." \
                --add-data "Src/image_generation.py:." --add-data "Src/themes.py:." \
                --add-data "Src/utils.py:." --add-data "Docs/SUPPORTED.txt:." \
                "Src/qt-version.py"

    mv dist/MetalSlugFontReborn/_internal/Assets dist/MetalSlugFontReborn/
    mv dist/MetalSlugFontReborn/_internal/SUPPORTED.txt dist/MetalSlugFontReborn/
}

build_console() {
    echo "Building console version..."
    pyinstaller --noconfirm --onedir --console --name "MetalSlugFontReborn" --clean \
                --add-data "Assets:Assets/" --add-data "Src/special_characters.py:." \
                --add-data "Src/image_generation.py:." --add-data "Docs/SUPPORTED.txt:." \
                "Src/console-version.py"

    mv dist/MetalSlugFontReborn/_internal/Assets dist/MetalSlugFontReborn/
    mv dist/MetalSlugFontReborn/_internal/SUPPORTED.txt dist/MetalSlugFontReborn/
}

while true; do
    echo "Select the version to build:"
    echo "1. Qt Version"
    echo "2. Console Version"
    echo ""
    echo "Type 'exit' or press CTRL+C to close."
    
    read -p "Enter your choice (1 or 2, or 'exit' to quit): " choice
    
    case $choice in
        1)
            build_qt
            ;;
        2)
            build_console
            ;;
        exit|EXIT)
            echo "Exiting..."
            deactivate
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter 1 or 2."
            ;;
    esac
done
