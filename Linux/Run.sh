#!/bin/bash

echo "MetalSlugFontReborn Runner"

source .venv/bin/activate

while true; do
    echo "Select an option:"
    echo "1. Run the Qt version"
    echo "2. Run the console version"
    echo "3. Exit"

    read -p "Enter your choice (1, 2, or 3): " choice

    case $choice in
        1)
            echo "Running the Qt version..."
            python Src/windowed-version.py
            ;;
        2)
            echo "Running the console version..."
            python Src/console-version.py
            ;;
        3)
            echo "Ok :("
            deactivate
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter 1, 2, or 3."
            ;;
    esac
done
