import os
from typing import final
from secrets import choice
from string import ascii_letters, digits
from collections import namedtuple, deque

import cv2
import numpy as np

from constants import SPECIAL_CHARACTERS

SPACE_WIDTH = 30

def clean_url(url):
    x = deque()
    x.appendleft('/')
    new_url = url.split('/')[5:]
    for item in new_url:
        x.append(f'{item}/')
    output_url = ""
    for item in x:
        output_url += item
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
        base = os.path.join('/home/Vermeil/MetalSlugFontReborn/Src/static/assets/fonts', f'font-{self._font}', f'Font-{self._font}-{self._color}')
        FontPaths = namedtuple('Font', ['Symbols', 'Letters', 'Numbers'])
        FontPaths.Symbols = os.path.join(base, 'Symbols')
        FontPaths.Letters = os.path.join(base, 'Letters')
        FontPaths.Numbers = os.path.join(base, 'Numbers')
        return FontPaths

    def _get_character_image_path(self, character: str):
        try:
            letters_folder = self._font_paths.Letters
            numbers_folder = self._font_paths.Numbers
            symbol_folder = self._font_paths.Symbols

            if character.isalpha():
                folder = 'Lower-Case' if character.islower() else 'Upper-Case'
                character_img_path = os.path.join('src', letters_folder, folder, f"{character}.png")
            elif character.isdigit():
                character_img_path = os.path.join('src', numbers_folder, f"{character}.png")
            else:
                character_img_path = os.path.join('src', symbol_folder, f"{SPECIAL_CHARACTERS.get(character, '')}.png")
                if not os.path.exists(character_img_path):
                    raise CharacterNotFound(character)

            return os.path.abspath(character_img_path)

        except CharacterNotFound as error:
            raise error
        except Exception as error:
            return str(error)

    def _load_character_image(self, character: str):
        if character not in self._character_images_cache:
            character_image_path = self._get_character_image_path(character)
            image = cv2.imread(character_image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise FileNotFoundError(f"Image not found for character '{character}'")
            self._character_images_cache[character] = image

        return self._character_images_cache[character]

    def generate_filename(self):
        random_filename = ''.join(choice(ascii_letters + digits) for _ in range(15))
        return f"{random_filename}.png"

    def generate_image(self):
        try:
            os.makedirs(os.path.join('/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images'), exist_ok=True)
        except OSError as e:
            return str(e)

        filename = os.path.join('/home/Vermeil/MetalSlugFontReborn/Src/static/Generated-Images/', self.generate_filename())
        images = []

        zero_image = np.zeros((1, SPACE_WIDTH, 4), dtype=np.uint8)

        for character in self._user_input:
            try:
                if character.isspace():
                    images.append(np.zeros_like(zero_image))
                    continue

                character_image = self._load_character_image(character)
                images.append(character_image)

            except (cv2.error, FileNotFoundError) as error:
                return str(error)

        try:
            max_height = max(image.shape[0] for image in images)
            resized_images = []

            for image in images:
                y_offset = max_height - image.shape[0]
                padded_image = cv2.copyMakeBorder(image, y_offset, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))
                resized_images.append(padded_image)

            horizontally = np.hstack(resized_images)
            cv2.imwrite(filename, horizontally)
        except Exception as write_error:
            return str(write_error)

        relative_path = clean_url(filename)

        self.state = True
        return relative_path
