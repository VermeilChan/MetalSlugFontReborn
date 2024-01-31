import os
from pathlib import Path
from secrets import choice
from string import ascii_letters, digits
from PIL import Image
from constants import SPECIAL_CHARACTERS

# def clean_url(url):
#     new_url = url.split('/')[5:]
#     output_url = '/'.join(new_url) + '/'
#     return output_url

class CharacterNotFound(Exception):
    def __init__(self, unsupported_character: str) -> None:
        message = f"Unsupported Character '{unsupported_character}', Try another font or Check out the list of supported characters"
        super().__init__(message)

def generate_filename():
    random_characters = ''.join(choice(ascii_letters + digits) for _ in range(15))
    return f"{random_characters}.png"

def get_font_paths(font, color):
    # /home/Vermeil/MetalSlugFontReborn/Src/static/assets/fonts
    base_path = Path('src') / 'static' / 'assets' / 'fonts' / f'Font-{font}' / f'Font-{font}-{color}'
    return [base_path / folder for folder in ['Letters', 'Numbers', 'Symbols']]

def get_character_image_path(character, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if character.isspace():
        return None
    if character.isalpha():
        folder = 'Lower-Case' if character.islower() else 'Upper-Case'
        character_image_path = CHARACTERS_FOLDER / folder / f"{character}.png"
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

def calculate_total_width_and_max_height(user_input, font_paths):
    total_width = 0
    max_height = 0

    for character in user_input:
        character_image = get_or_create_character_image(character, font_paths)
        max_height = max(max_height, character_image.height)
        total_width += character_image.width

    return total_width, max_height

def paste_character_images_to_final_image(user_input, total_width, max_height, font_paths):
    x_position = 0
    final_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    for character in user_input:
        character_image = get_or_create_character_image(character, font_paths)

        y_position = max_height - character_image.height

        final_image.paste(character_image, (x_position, y_position))
        x_position += character_image.width

    return final_image

def generate_image(user_input: str, font: int, color: str) -> str:
    font_paths = get_font_paths(font, color)

    # /home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images
    os.makedirs(os.path.join('src/static/Generated-Images'), exist_ok=True)

    # /home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images/
    filename = os.path.join('src/static/Generated-Images/', generate_filename())
    total_width, max_height = calculate_total_width_and_max_height(user_input, font_paths)
    final_image = paste_character_images_to_final_image(user_input, total_width, max_height, font_paths)

    try:
        final_image.save(filename)
    except Exception as write_error:
        return str(write_error)

    # relative_path = clean_url(filename)

    return filename
