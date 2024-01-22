from pathlib import Path
from secrets import choice
from string import ascii_letters, digits
from PIL import Image
from constants import SPECIAL_CHARACTERS

SPACE_WIDTH = 30
DESKTOP_PATH = Path.home() / 'Desktop'

SPACE_IMAGE = Image.new("RGBA", (SPACE_WIDTH, 1), (0, 0, 0, 0))

def generate_filename(_):
    random_characters = ''.join(choice(ascii_letters + digits) for _ in range(15))
    return f"{random_characters}.png"

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

def get_or_create_character_image(character, font_paths):
    if character.isspace():
        return SPACE_IMAGE

    character_image_path = get_character_image_path(character, font_paths)
    if character_image_path is None or not character_image_path.is_file():
        raise FileNotFoundError(f"Unsupported character '{character}'")

    image = Image.open(character_image_path).convert("RGBA")
    return image

def generate_image(text, filename, font_paths):
    total_width = sum(get_or_create_character_image(c, font_paths).width for c in text)
    max_height = max(get_or_create_character_image(c, font_paths).height for c in text)

    final_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    x_position = 0
    for character in text:
        character_image = get_or_create_character_image(character, font_paths)
        y_position = max_height - character_image.height

        final_image.paste(character_image, (x_position, y_position))
        x_position += character_image.width

    image_path = Path(DESKTOP_PATH) / filename
    final_image.save(image_path)

    return str(image_path), None
