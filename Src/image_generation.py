from uuid import uuid4
from pathlib import Path
from numpy import zeros, uint8
from cv2 import imread, IMREAD_UNCHANGED, cvtColor, COLOR_BGR2BGRA, IMWRITE_PNG_COMPRESSION, imwrite
from special_characters import special_characters

def generate_filename(_):
    return f"{uuid4().hex}.png"

def get_font_paths(font, color):
    base = Path("Assets/Fonts") / f"Font-{font}" / f"MS-{color}"
    return {
        "letters": base / "Letters",
        "numbers": base / "Numbers",
        "symbols": base / "Symbols",
    }

def get_character_path(character, font_paths):
    if character.isspace():
        return None
    elif character.islower():
        return font_paths["letters"] / "Lower-Case" / f"{character}.png"
    elif character.isupper():
        return font_paths["letters"] / "Upper-Case" / f"{character}.png"
    elif character.isdigit():
        return font_paths["numbers"] / f"{character}.png"
    return font_paths["symbols"] / f"{special_characters.get(character, '')}.png"

def create_character_image(character, font_paths):
    if character.isspace():
        return zeros((1, 25, 4), dtype=uint8)

    path = get_character_path(character, font_paths)
    if path and path.is_file():
        img = imread(str(path), IMREAD_UNCHANGED)
        if img.shape[2] == 3:
            img = cvtColor(img, COLOR_BGR2BGRA)
        return img

    raise FileNotFoundError(f"The character '{character}' is not supported. Please check SUPPORTED.txt")

def compress_image(image_path):
    img = imread(str(image_path), IMREAD_UNCHANGED)
    imwrite(str(image_path), img, [IMWRITE_PNG_COMPRESSION, 9])

def split_into_lines(text, max_words):
    words = text.split()
    return [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ] if max_words else [text]

def generate_image(text, filename, font_paths, save_dir, max_words=None):
    lines = split_into_lines(text, max_words)
    all_chars = {c for line in lines for c in line}
    char_images = {char: create_character_image(char, font_paths) for char in all_chars}

    line_images = []
    max_width = total_height = 0

    for line in lines:
        if not line:
            continue

        char_imgs = [char_images[c] for c in line]
        line_height = max(img.shape[0] for img in char_imgs)
        line_width = sum(img.shape[1] for img in char_imgs)
        line_img = zeros((line_height, line_width, 4), dtype=uint8)

        x = 0
        for char in line:
            img = char_images[char]
            y_offset = line_height - img.shape[0]
            line_img[y_offset:y_offset + img.shape[0], x:x + img.shape[1]] = img
            x += img.shape[1]

        line_images.append(line_img)
        max_width = max(max_width, line_width)
        total_height += line_height

    final_image = zeros((total_height, max_width, 4), dtype=uint8)
    y = 0
    for img in line_images:
        final_image[y:y + img.shape[0], 0:img.shape[1]] = img
        y += img.shape[0]

    save_path = Path(save_dir) / filename
    imwrite(str(save_path), final_image)
    return str(save_path), None
