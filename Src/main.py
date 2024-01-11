from typing import final
from pathlib import Path
from secrets import choice
from os import path, makedirs
from collections import namedtuple
from string import ascii_letters, digits
from PIL import Image
from constants import SPECIAL_CHARACTERS

SPACE_WIDTH = 30

def clean_url(url):
    new_url = url.split('/')[5:]
    output_url = '/'.join(new_url) + '/'
    return output_url

class CharacterNotFound(Exception):
    def __init__(self, unsupported_character: str) -> None:
        super().__init__(f"Unsupported Character '{unsupported_character}', Try another font or ")
        self.errno = 10

@final
class ImageGeneration(object):
    state = False

    def __init__(self, user_input: str, font: int, color: str) -> None:
        self._user_input = user_input
        self._font = font
        self._color = color
        self._font_paths = self._compute_font_paths()
        self._character_images_cache = {}

    def _compute_font_paths(self):
        base = path.join('/home/Vermeil/MetalSlugFontReborn/Src/static/assets/fonts', f'font-{self._font}', f'Font-{self._font}-{self._color}')
        FontPaths = namedtuple('Font', ['Symbols', 'Letters', 'Numbers'])
        FontPaths.Letters = path.join(base, 'Letters')
        FontPaths.Numbers = path.join(base, 'Numbers')
        FontPaths.Symbols = path.join(base, 'Symbols')
        return FontPaths

    def _get_character_image_path(self, character: str):
        try:
            letters_folder = self._font_paths.Letters
            numbers_folder = self._font_paths.Numbers
            symbol_folder = self._font_paths.Symbols

            if character.isalpha():
                folder = 'Lower-Case' if character.islower() else 'Upper-Case'
                character_image_path = path.join('src', letters_folder, folder, f"{character}.png")
            elif character.isdigit():
                character_image_path = path.join('src', numbers_folder, f"{character}.png")
            else:
                character_image_path = path.join('src', symbol_folder, f"{SPECIAL_CHARACTERS.get(character, '')}.png")
                if not path.exists(character_image_path):
                    raise CharacterNotFound(character)

            return Path(character_image_path)

        except CharacterNotFound as error:
            raise error
        except Exception as error:
            return str(error)

    def _load_character_image(self, character: str):
        if character not in self._character_images_cache:
            character_image_path = self._get_character_image_path(character)
            image = Image.open(str(character_image_path)).convert("RGBA")
            if image is None:
                raise FileNotFoundError(f"Image not found for character '{character}'")
            self._character_images_cache[character] = image

        return self._character_images_cache[character]

    def generate_filename(self):
        random_filename = ''.join(choice(ascii_letters + digits) for _ in range(15))
        return f"{random_filename}.png"

    def generate_image(self):
        try:
            makedirs(path.join('/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images'), exist_ok=True)
        except OSError as e:
            return str(e)

        filename = path.join('/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images/', self.generate_filename())
        total_width, max_height = self.calculate_total_width_and_max_height()
        final_image = self.paste_character_images_to_final_image(total_width, max_height)

        try:
            final_image.save(filename)
        except Exception as write_error:
            return str(write_error)

        relative_path = clean_url(filename)

        self.state = True
        return relative_path

    def get_or_create_character_image(self, character):
        if character.isspace():
            return self.create_character_image(character)

        character_image_path = self._get_character_image_path(character)
        if character_image_path is None or not character_image_path.is_file():
            raise FileNotFoundError(f"Image not found for character '{character}'")

        image = Image.open(str(character_image_path)).convert("RGBA")
        return image

    def create_character_image(self, character):
        if character.isspace():
            return Image.new("RGBA", (SPACE_WIDTH, 1), (0, 0, 0, 0))

    def calculate_total_width_and_max_height(self):
        total_width = 0
        max_height = 0

        for character in self._user_input:
            character_image = self.get_or_create_character_image(character)
            max_height = max(max_height, character_image.height)
            total_width += character_image.width

        return total_width, max_height

    def paste_character_images_to_final_image(self, total_width, max_height):
        x_position = 0
        final_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

        for character in self._user_input:
            character_image = self.get_or_create_character_image(character)

            y_position = max_height - character_image.height

            final_image.paste(character_image, (x_position, y_position))
            x_position += character_image.width

        return final_image
