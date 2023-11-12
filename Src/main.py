import random, string, os, sys

from collections import namedtuple
from typing import final

import cv2, numpy

sys.dont_write_bytecode = True

from constants import SPACE_WIDTH, SPECIAL_CHARACTERS

@final
class ImageGeneration(object):

    def __init__(self , user_input:str , font:int , color:str) -> None:

        self._user_input = user_input
        self._font = font
        self._color = color
    
    def GenerateFilename(self):
        self.character = ""
        for i in range(0 , 15):
            random_character = random.choice(string.ascii_letters + string.digits)        
            self.character += random_character

        return f"{self.character}.png"

    def GetFontPath(self):
        self.base = os.path.join('static' , 'assets' , 'fonts' , f'font-{self._font}' , f'Font-{self._font}-{self._color}')

        self.container = namedtuple('Font' , ['Symbols' , 'Letters' , 'Numbers'])

        self.container.Symbols = os.path.join(self.base, 'Symbols')
        self.container.Letters = os.path.join(self.base, 'Letters')
        self.container.Numbers = os.path.join(self.base, 'Numbers')

        return self.container

    def GetCharacterImagePath(self , char:str):
        letters_folder   = self.GetFontPath().Letters
        numbers_folder   = self.GetFontPath().Numbers
        symbol_folder    = self.GetFontPath().Symbols

        if char.isalpha():
            folder = 'Lower-Case' if char.islower() else 'Upper-Case'

            self.char_img_path = os.path.join('src' , letters_folder, folder, f"{char}.png")

        elif char.isdigit():
            self.char_img_path = os.path.join('src' , numbers_folder, f"{char}.png")
        else:
            self.char_img_path = os.path.join('src' , symbol_folder, f"{SPECIAL_CHARACTERS.get(char, '')}.png")

        return os.path.abspath(self.char_img_path)

    def GenerateImage(self): 

        try:
            os.mkdir('src/static/Generated-Images')
        except Exception:
            pass

        self.filename = os.path.join('src' , 'static' , 'Generated-Images' , self.GenerateFilename())
        self.images = []
        for character in self._user_input:

            if character == " ":
                space_image = numpy.zeros((self._image.shape[0], SPACE_WIDTH, 4), dtype=numpy.uint8)
                self.images.append(space_image)
                continue

            self._image = cv2.imread(self.GetCharacterImagePath(character) , cv2.IMREAD_UNCHANGED)
            self.images.append(self._image)

        try:
            self.horizentaly = cv2.hconcat(self.images)
            cv2.imwrite(self.filename , self.horizentaly)

        except Exception as error:
            print(error)

        return self.filename
