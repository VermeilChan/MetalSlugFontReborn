def GenerateImage(self):

        self.__character_map   = {}
        self.__image_height    = None
        self.__image_path      = ""
        self.__character_image = ""

        self.filename = self.GenerateFilename()

        try:

            self.__image_path = lambda : os.path.join('static' , 'assets' , 'output' , self.filename)
            os.mkdir('Src/static/assets/output')
            self.__image_path()

        except Exception:
            self.__image_path()

  
        for character in self._user_input:
            self.image_width = 0
            if character == " ":

                self.__character_image = Image.new("RGBA", (SPACE_WIDTH, self.__image_height or 1), (0, 0, 0, 0))
            
            else:

                self.__character_image_path = self.GetCharacterImagePath(character)
                self.__character_image = Image.open(self.__character_image_path).convert("RGBA")
        
        
            self.__character_map[character] = self.__character_image
            self.__image_height = self.__character_image.height if self.__image_height is None else self.__image_height
            self.image_width   += self.__character_image.width

            print(f"{self.image_width} : {character}")
        
        self.final = Image.new("RGBA", (self.image_width, self.__image_height), (0, 0, 0, 0))
        _ = 0

        for character in self._user_input:
            self.final.paste(self.__character_map[character] , (_ , 0))
            _ += self.__character_map[character].width

        self.final.save(os.path.join('Src' , self.__image_path()))

        return (self.filename , None)