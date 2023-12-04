from pathlib import Path

def remove_images(directory_path):
    directory = Path(directory_path)

    if directory.exists():
        for file_path in directory.glob("*.png"):
            file_path.unlink()
            print(f"Removed: {file_path}")
    else:
        print(f"Directory not found: {directory}")

wsgi_directory_path = "/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images/"
local_directory_path = "Src/static/Generated-Images/"

remove_images(wsgi_directory_path)

if not Path(wsgi_directory_path).exists():
    remove_images(local_directory_path)
