# Import necessary libraries
import random, string, os, sys

from collections import namedtuple
from typing import final

import cv2, numpy

# Prevent the generation of .pyc (Python bytecode) files
sys.dont_write_bytecode = True

# Import necessary constants from the constants module
from constants import SPACE_WIDTH, SPECIAL_CHARACTERS

class CharacterNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.errno = 10

    def add_note(self, __note: str) -> None:
        return super().add_note("Unsupported Character")

@final
class ImageGeneration(object):

    def __init__(self, user_input: str, font: int, color: str) -> None:
        # Initialize the ImageGeneration object with user input, font, and color
        self._user_input = user_input
        self._font = font
        self._color = color
    
    def GenerateFilename(self):
        # Generate a random filename for the image
        self.character = ""
        for _ in range(0, 15):
            random_character = random.choice(string.ascii_letters + string.digits)        
            self.character += random_character

        return f"{self.character}.png"

    def GetFontPath(self):
        # Get the paths for different font components (symbols, letters, numbers)
        self.base = os.path.join('static', 'assets', 'fonts', f'font-{self._font}', f'Font-{self._font}-{self._color}')
        self.container = namedtuple('Font', ['Symbols', 'Letters', 'Numbers'])
        self.container.Symbols = os.path.join(self.base, 'Symbols')
        self.container.Letters = os.path.join(self.base, 'Letters')
        self.container.Numbers = os.path.join(self.base, 'Numbers')

        return self.container

    def GetCharacterImagePath(self, char: str):
        # Get the image path for a specific character based on its type
        try:
            letters_folder = self.GetFontPath().Letters
            numbers_folder = self.GetFontPath().Numbers
            symbol_folder = self.GetFontPath().Symbols

            if char.isalpha():
                folder = 'Lower-Case' if char.islower() else 'Upper-Case'
                self.char_img_path = os.path.join('src', letters_folder, folder, f"{char}.png")

            elif char.isdigit():
                self.char_img_path = os.path.join('src', numbers_folder, f"{char}.png")
                
            else:
                self.char_img_path = os.path.join('src', symbol_folder, f"{SPECIAL_CHARACTERS.get(char, '')}.png")
            return os.path.abspath(self.char_img_path)
        
        except Exception as error:
            return error

    def GenerateImage(self): 
        # Generate the final image based on user input
        try:
            os.mkdir('src/static/Generated-Images')
        except Exception:
            pass

        self.filename = os.path.join('src', 'static', 'Generated-Images', self.GenerateFilename())
        self.images = []
        for character in self._user_input:

            try:
                if character == " ":
                    # Create an image for space and append it to the list
                    space_image = numpy.zeros((self._image.shape[0], SPACE_WIDTH, 4), dtype=numpy.uint8)
                    self.images.append(space_image)
                    continue

                self._image = cv2.imread(self.GetCharacterImagePath(character), cv2.IMREAD_UNCHANGED)
                self.images.append(self._image)

            except cv2.error as error:
                return error

        try:
            # Concatenate the images horizontally and save the final image
            self.horizontally = cv2.hconcat(self.images)
            cv2.imwrite(self.filename, self.horizontally)

        except Exception as error:
            # Print an error message if an exception occurs
            return error

        return self.filename
