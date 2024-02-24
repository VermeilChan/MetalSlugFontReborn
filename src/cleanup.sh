#!/bin/bash

remove_images() {
    directory_path="$1"
    start_time=$(date +%s)

    if [ -d "$directory_path" ]; then
        for file_path in "$directory_path"/*.png; do
            rm "$file_path"
            echo "Removed: $file_path"
        done
    fi

    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "Time taken to remove images: $duration seconds"
}

wsgi_directory="/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images/"
local_directory="Src/static/Generated-Images/"

remove_images "$wsgi_directory"
remove_images "$local_directory"
