#!/bin/bash

source metalslugfontreborn/bin/activate

echo "Choose a version to run:"
echo "1. Windowed Version"
echo "2. Console Version"

read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        python3 Src/windowed-version.py
        ;;
    2)
        python3 Src/console-version.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        deactivate
        exit 1
        ;;
esac

if [ $? -ne 0 ]; then
    echo ""
    echo "If the GUI version isn't working for you, even after installing xcb."
    echo "please refer to the discussions on GitHub at https://github.com/NVlabs/instant-ngp/discussions/300."
    echo ""
    echo "Or, check if a new Qt6 update has been released."
    echo "If so, you may need to wait until PyQt6 updates or use the CLI version."
    echo ""
fi

deactivate
