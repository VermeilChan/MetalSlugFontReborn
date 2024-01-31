from uuid import uuid4
from pathlib import Path
from PIL import Image
from constants import SPECIAL_CHARACTERS

def generate_filename(_):
    unique_id = uuid4()
    return f"{unique_id}.png"

def get_font_paths(font, color):
    base_path = Path('Assets') / 'Fonts' / f'Font-{font}' / f'Font-{font}-{color}'
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
    if character_image_path is None:
        raise FileNotFoundError(f"Unsupported character '{character}'")

    return Image.open(character_image_path)

def generate_image(text, filename, font_paths):
    character_images = [get_or_create_character_image(c, font_paths) for c in text]

    total_width = sum(image.width for image in character_images)
    max_height = max(image.height for image in character_images)

    images_to_combine = []

    x_position = 0
    for _, character_image in zip(text, character_images):
        y_position = max_height - character_image.height
        images_to_combine.append((character_image, (x_position, y_position)))
        x_position += character_image.width

    final_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    for character_image, position in images_to_combine:
        final_image.paste(character_image, position)

    image_path = Path.home() / 'Desktop' / filename

    with final_image as image:
        image.save(image_path)
    
    return str(image_path), None
