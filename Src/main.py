from PIL import Image, UnidentifiedImageError
from collections import namedtuple
from constants import SPACE_WIDTH, SPECIAL_CHARACTERS
import random , string , os
from typing import final
from rich import console
import cv2

conosle = console.Console()

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

            self.char_img_path = os.path.join('Src' , letters_folder, folder, f"{char}.png")


        elif char.isdigit():

            self.char_img_path = os.path.join('Src' , numbers_folder, f"{char}.png")


        elif char == ' ':

            ...

        else:

            self.char_img_path = os.path.join('Src' , symbol_folder, f"{SPECIAL_CHARACTERS.get(char, '')}.png")

        return self.char_img_path

    def GenerateImage(self): 

        self.images = [
            cv2.imread(self.GetCharacterImagePath(character)) for character in self._user_input
        ]

        self.horizentaly = cv2.hconcat(self.images)


        cv2.imshow('Horizentaly' , self.horizentaly)
        cv2.waitKey(0)

        cv2.destroyAllWindows()



    

        

o = ImageGeneration('Hello World' , 1 , 'Orange-1')


try:
    o.GenerateImage()
except:
    conosle.print_exception()