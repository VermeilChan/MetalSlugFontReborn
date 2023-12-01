import string
import secrets
from pathlib import Path

from PIL import Image

from constants import SPACE_WIDTH, DESKTOP_PATH, SPECIAL_CHARACTERS

def generate_filename(_):
    random_chars = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(15))
    filename = f"{random_chars}.png"
    return filename

def get_font_paths(font, color):
    base_path = Path('Assets') / 'Fonts' / f'Font-{font}' / f'Font-{font}-{color}'
    return [base_path / folder for folder in ['Letters', 'Numbers', 'Symbols']]

def get_character_image_path(character, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if character.isalpha():
        folder = 'Lower-Case' if character.islower() else 'Upper-Case'
        character_image_path = CHARACTERS_FOLDER / folder / f"{character}.png"
    elif character.isdigit():
        character_image_path = NUMBERS_FOLDER / f"{character}.png"
    elif character.isspace():
        return None
    else:
        character_image_path = SYMBOLS_FOLDER / f"{SPECIAL_CHARACTERS.get(character, '')}.png"

    return character_image_path if character_image_path.is_file() else None

def create_character_image(character, font_paths):
    if character.isspace():
        return Image.new("RGBA", (SPACE_WIDTH, 1), (0, 0, 0, 0))

    character_image_path = get_character_image_path(character, font_paths)
    if not character_image_path or not character_image_path.is_file():
        raise FileNotFoundError(f"Error: Image not found for character '{character}'")

    return Image.open(character_image_path).convert("RGBA")

def calculate_total_width_and_max_height(text, font_paths):
    total_width = 0
    max_height = 0

    for character in text:
        character_image = create_character_image(character, font_paths)
        max_height = max(max_height, character_image.height)
        total_width += character_image.width

    return total_width, max_height

def paste_character_images_to_final_image(text, character_images, final_image):
    x_position = 0

    for character in text:
        final_image.paste(character_images[character], (x_position, 0))
        x_position += character_images[character].width

def generate_image(text, filename, font_paths):
    image_path = Path(DESKTOP_PATH) / filename
    total_width, max_height = calculate_total_width_and_max_height(text, font_paths)
    character_images = {character: create_character_image(character, font_paths) for character in text}
    final_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    paste_character_images_to_final_image(text, character_images, final_image)
    final_image.save(image_path)

    return str(image_path), None
