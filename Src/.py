self.image_height = None
        self.character_map = {}
        
        try:
            image_path = lambda:os.path.join('static' , 'assets' , 'output' , self.GenerateFilename())
            image_path()

        except OSError as error:

            os.mkdir('static/assets/output')
            
        finally:
            image_path()
        try:
            total_width = 0

            for char in self._user_input:

                if char == ' ':

                    char_img = Image.new("RGBA", (SPACE_WIDTH, self.image_height or 1), (0, 0, 0, 0))

                else:
                    
                    char_img_path = self.GetCharacterImagePath(char)

                    if not char_img_path:
                        raise FileNotFoundError(f"Image not found for character '{char}'")

                    char_img = Image.open(char_img_path).convert("RGBA")

                character_map[char] = char_img
                img_height = char_img.height if img_height is None else img_height
                total_width += char_img.width

            # Create the final image and paste character images into it
            final_img = Image.new("RGBA", (total_width, img_height), (0, 0, 0, 0))
            x = 0

            for char in text:
                final_img.paste(character_map[char], (x, 0))
                x += character_map[char].width

            # Save the final image
            final_img.save(img_path)

            return (filename, None)

        except FileNotFoundError:
            return (None, f"Error: Image not found for character '{char}'")
        
        except UnidentifiedImageError:
            return (None, "Error: Unable to identify image")
        
        except ValueError as e:
            return (None, f"Error: Invalid value - {str(e)}")
        
        except Exception as e:
            return (None, f"An unexpected error occurred: {str(e)}")
