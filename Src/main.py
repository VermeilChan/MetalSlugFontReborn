from uuid import uuid4
from pathlib import Path
from PIL import Image
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
        return Image.new("RGBA", (30, 1), (0, 0, 0, 0))

    character_image_path = get_character_image_path(character, font_paths)
    if not character_image_path or not character_image_path.is_file():
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

    image_path = Path.home() / 'Desktop' / filename
    final_image.save(image_path, optimize=True)

    return str(image_path), None
