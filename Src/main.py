import os
import string
import secrets

from typing import final
from collections import namedtuple

import cv2
import numpy as np

from constants import SPACE_WIDTH, SPECIAL_CHARACTERS

class CharacterNotFound(Exception):
    def __init__(self, unsupported_characters: str) -> None:
        super().__init__(f"Unsupported Character '{unsupported_characters}', Try another font or ")
        self.errno = 10

@final
class ImageGeneration(object):
    state = False

    def __init__(self, user_input: str, font: int, color: str) -> None:
        self._user_input = user_input
        self._font = font
        self._color = color
        self._image = None
        self._font_paths = self._compute_font_paths()

    def _compute_font_paths(self):
        base = os.path.join('/home/Vermeil/MetalSlugFontReborn/Src/static/assets/fonts', f'font-{self._font}', f'Font-{self._font}-{self._color}')
        FontPaths = namedtuple('Font', ['Symbols', 'Letters', 'Numbers'])
        FontPaths.Symbols = os.path.join(base, 'Symbols')
        FontPaths.Letters = os.path.join(base, 'Letters')
        FontPaths.Numbers = os.path.join(base, 'Numbers')
        return FontPaths

# development server
#
#    def _compute_font_paths(self):
#        base = os.path.join('static', 'assets', 'fonts', f'font-{self._font}', f'Font-{self._font}-{self._color}')
#        FontPaths = namedtuple('Font', ['Symbols', 'Letters', 'Numbers'])
#        FontPaths.Symbols = os.path.join(base, 'Symbols')
#        FontPaths.Letters = os.path.join(base, 'Letters')
#        FontPaths.Numbers = os.path.join(base, 'Numbers')
#        return FontPaths

    def _get_character_image_path(self, char: str):
        try:
            letters_folder = self._font_paths.Letters
            numbers_folder = self._font_paths.Numbers
            symbol_folder = self._font_paths.Symbols

            if char.isalpha():
                folder = 'Lower-Case' if char.islower() else 'Upper-Case'
                char_img_path = os.path.join('src', letters_folder, folder, f"{char}.png")
            elif char.isdigit():
                char_img_path = os.path.join('src', numbers_folder, f"{char}.png")
            else:
                char_img_path = os.path.join('src', symbol_folder, f"{SPECIAL_CHARACTERS.get(char, '')}.png")
                if not os.path.exists(char_img_path):
                    raise CharacterNotFound(char)

            return os.path.abspath(char_img_path)

        except CharacterNotFound as error:
            raise error
        except Exception as error:
            return str(error)

    def generate_filename(self):
        random_characters = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(15))
        return f"{random_characters}.png"

    def generate_image(self):
        try:
            os.makedirs('/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images', exist_ok=True)
        except FileExistsError:
            pass

        filename = '/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images/' + self.generate_filename()
        images = []

# development server
#
#    def generate_image(self):
#        try:
#            os.mkdir(os.path.join('src', 'static', 'Generated-Images'))
#        except FileExistsError:
#            pass
#
#        filename = os.path.join('src', 'static', 'Generated-Images', self.generate_filename())
#        images = []

        zero_image = np.zeros((1, 1, 4), dtype=np.uint8)

        for character in self._user_input:
            try:
                if character == ' ':
                    space_image = np.zeros((zero_image.shape[0], SPACE_WIDTH, 4), dtype=np.uint8)
                    images.append(space_image)
                    continue

                char_image_path = self._get_character_image_path(character)
                char_image = cv2.imread(char_image_path, cv2.IMREAD_UNCHANGED)
                if char_image is None:
                    raise FileNotFoundError(f"Image not found for character '{character}'")

                images.append(char_image)

            except (cv2.error, FileNotFoundError) as error:
                return str(error)

        try:
            max_height = max(image.shape[0] for image in images)
            resized_images = [cv2.resize(image, (image.shape[1], max_height)) for image in images]

            horizontally = cv2.hconcat(resized_images)
            cv2.imwrite(filename, horizontally)
        except Exception as write_error:
            return str(write_error)

        self.state = True
        return filename
