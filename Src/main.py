import random
import string
from pathlib import Path

from PIL import Image

from constants import SPACE_WIDTH, DESKTOP_PATH, SPECIAL_CHARACTERS

def generate_filename(_):
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    filename = f"{random_chars}.png"
    return filename

def get_font_paths(font, color):
    base_path = Path('Assets') / 'Fonts' / f'Font-{font}' / f'Font-{font}-{color}'
    return [base_path / folder for folder in ['Letters', 'Numbers', 'Symbols']]

def get_character_image_path(char, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if char.isalpha():
        folder = 'Lower-Case' if char.islower() else 'Upper-Case'
        char_img_path = CHARACTERS_FOLDER / folder / f"{char}.png"
    elif char.isdigit():
        char_img_path = NUMBERS_FOLDER / f"{char}.png"
    elif char == ' ':
        return None
    else:
        char_img_path = SYMBOLS_FOLDER / f"{SPECIAL_CHARACTERS.get(char, '')}.png"

    return char_img_path if char_img_path.is_file() else None

def generate_image(text, filename, font_paths):
    img_height = None
    char_images = {}
    img_path = Path(DESKTOP_PATH) / filename

    total_width = 0

    for char in text:
        if char == ' ':
            char_img = Image.new("RGBA", (SPACE_WIDTH, img_height or 1), (0, 0, 0, 0))
        else:
            char_img_path = get_character_image_path(char, font_paths)
            if not char_img_path or not char_img_path.is_file():
                return None, f"Error: Image not found for character '{char}'"

            char_img = Image.open(char_img_path).convert("RGBA")

        char_images[char] = char_img
        img_height = char_img.height if img_height is None else img_height
        total_width += char_img.width

    final_img = Image.new("RGBA", (total_width, img_height), (0, 0, 0, 0))
    x = 0

    for char in text:
        final_img.paste(char_images[char], (x, 0))
        x += char_images[char].width

    final_img.save(img_path)

    return str(img_path), None
