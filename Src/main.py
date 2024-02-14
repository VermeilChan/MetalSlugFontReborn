import os
from uuid import uuid4
from pathlib import Path
from PIL import Image
from constants import SPECIAL_CHARACTERS

def generate_filename():
    unique_id = uuid4()
    return f"{unique_id}.png"

def get_font_paths(font, color):
    base_path = Path('src') / 'static' / 'assets' / 'fonts' / f'Font-{font}' / f'Font-{font}-{color}'
    return [base_path / folder for folder in ['Letters', 'Numbers', 'Symbols']]

def get_character_image_path(character, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if character.isspace():
        return None
    elif character.islower():
        character_image_path = CHARACTERS_FOLDER / 'Lower-Case' / f"{character}.png"
    elif character.isupper():
        character_image_path = CHARACTERS_FOLDER / 'Upper-Case' / f"{character}.png"
    elif character.isdigit():
        character_image_path = NUMBERS_FOLDER / f"{character}.png"
    else:
        character_image_path = SYMBOLS_FOLDER / f"{SPECIAL_CHARACTERS.get(character, '')}.png"

    return character_image_path

def get_or_create_character_image(character, font_paths):
    if character.isspace():
        return Image.new("RGBA", (30, 1), (0, 0, 0, 0))

    character_image_path = get_character_image_path(character, font_paths)
    if character_image_path is None or not character_image_path.is_file():
        raise FileNotFoundError(f"Unsupported character '{character}'")

    return Image.open(character_image_path)

def generate_image(text, filename, font_paths):
    font_images = {c: get_or_create_character_image(c, font_paths) for c in set(text)}

    total_width = sum(font_images[c].width for c in text)
    max_height = max(font_images[c].height for c in text)

    final_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    x_position = 0
    for c in text:
        character_image = font_images[c]
        y_position = max_height - character_image.height
        final_image.paste(character_image, (x_position, y_position))
        x_position += character_image.width

    image_directory = Path('src') / 'static'/ 'Generated-Images'
    os.makedirs(image_directory, exist_ok=True)

    image_path = image_directory / filename
    final_image.save(image_path)

    image_url = f'/static/Generated-Images/{filename}'

    return image_url, None
