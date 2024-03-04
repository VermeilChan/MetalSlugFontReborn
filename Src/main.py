from uuid import uuid4
from pathlib import Path
from numpy import zeros, uint8
from cv2 import imread, imwrite, cvtColor, IMREAD_UNCHANGED, IMWRITE_PNG_COMPRESSION, COLOR_BGR2BGRA
from constants import special_characters

def generate_filename(_):
    unique_id = uuid4().hex
    return f"{unique_id}.png"

def get_font_paths(font, color):
    base_path = Path('Assets') / 'Fonts' / f'Font-{font}' / f'Font-{font}-{color}'
    return [base_path / folder for folder in ('Letters', 'Numbers', 'Symbols')]

def get_character_image_path(character, font_paths):
    characters_folder, numbers_folder, symbols_folder = font_paths

    if character.isspace():
        return None
    elif character.islower():
        character_image_path = characters_folder / 'Lower-Case' / f"{character}.png"
    elif character.isupper():
        character_image_path = characters_folder / 'Upper-Case' / f"{character}.png"
    elif character.isdigit():
        character_image_path = numbers_folder / f"{character}.png"
    else:
        character_image_path = symbols_folder / f"{special_characters.get(character, '')}.png"

    return character_image_path

def get_or_create_character_image(character, font_paths):
    if character.isspace():
        return zeros((1, 30, 4), dtype=uint8)

    image_path = get_character_image_path(character, font_paths)
    if not image_path or not image_path.is_file():
        raise FileNotFoundError(f"Unsupported character '{character}'")

    return cvtColor(imread(str(image_path), IMREAD_UNCHANGED), COLOR_BGR2BGRA)

def generate_image(text, filename, font_paths):
    font_images = {character: get_or_create_character_image(character, font_paths) for character in set(text)}

    total_width = sum(font_images[character].shape[1] for character in text)
    max_height = max(font_images[char].shape[0] for char in text)

    final_image = zeros((max_height, total_width, 4), dtype=uint8)

    x_position = 0
    for character in text:
        character_image = font_images[character]
        y_position = max_height - character_image.shape[0]
        final_image[y_position:y_position + character_image.shape[0], x_position:x_position + character_image.shape[1]] = character_image
        x_position += character_image.shape[1]

    image_path = Path.home() / 'Desktop' / filename
    imwrite(str(image_path), final_image, [IMWRITE_PNG_COMPRESSION, 9])

    return str(image_path), None
