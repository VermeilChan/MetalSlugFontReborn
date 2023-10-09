# Import necessary libraries
import os
from datetime import datetime

from PIL import Image, UnidentifiedImageError

# Constants
SPACE_WIDTH = 30
MAX_FILENAME_LENGTH = 255
DESKTOP_PATH = os.path.expanduser("~/Desktop")
SPECIAL_CHARACTERS = {
    '!': 'Exclamation', '?': 'Question', "'": 'Apostrophe', '*': 'Asterisk',
    ')': 'Bracket-Left', '}': 'Bracket-Left-2', ']': 'Bracket-Left-3',
    '(': 'Bracket-Right', '{': 'Bracket-Right-2', '[': 'Bracket-Right-3',
    '^': 'Caret', ':': 'Colon', '$': 'Dollar', '=': 'Equals', '>': 'Greater-than',
    '-': 'Hyphen', '∞': 'Infinity', '<': 'Less-than', '#': 'Number', '%': 'Percent',
    '.': 'Period', '+': 'Plus', '"': 'Quotation', ';': 'Semicolon', '/': 'Slash',
    '~': 'Tilde', '_': 'Underscore', '|': 'Vertical-bar', ',': 'Comma', '&': 'Ampersand',
    '♥': 'Heart', '©': 'Copyright', '⛶': 'Square', 'Ⅰ': 'One', 'Ⅱ': 'Two', 'Ⅲ': 'Three',
    'Ⅳ': 'Four', 'Ⅴ': 'Five', '◀': 'Left', '▲': 'Up', '▶': 'Right', '▼': 'Down',
    '★': 'Star', '⋆': 'Mini-Star', '☞': 'Hand', '¥': 'Yen', '♪': 'Musical-Note', '︷': 'Up-Arrow'
}

# Function to generate a filename based on user input and timestamp
def generate_filename(user_input):
    try:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        sanitized_input = '-'.join(filter(str.isalnum, user_input.split()))
        filename = f"{sanitized_input}-{timestamp}.png"
        return filename if len(filename) <= MAX_FILENAME_LENGTH else f"{timestamp}.png"
    except Exception as e:
        raise RuntimeError(f"Error generating filename: {str(e)}")

# Function to get paths to font assets based on font and color.
def get_font_paths(font, color):
    try:
        base_path = os.path.join('Assets', 'Fonts', f'Font-{font}', f'Font-{font}-{color}')
        return (
            os.path.join(base_path, 'Letters'),
            os.path.join(base_path, 'Numbers'),
            os.path.join(base_path, 'Symbols')
        )
    except Exception as e:
        raise RuntimeError(f"Error getting font paths: {str(e)}")

# Function to get the image path for a specific character based on its type
def get_character_image_path(char, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if char.isalpha():
        folder = 'Lower-Case' if char.islower() else 'Upper-Case'
        char_img_path = os.path.join(CHARACTERS_FOLDER, folder, f"{char}.png")
    elif char.isdigit():
        char_img_path = os.path.join(NUMBERS_FOLDER, f"{char}.png")
    elif char == ' ':
        return None
    else:
        char_img_path = os.path.join(SYMBOLS_FOLDER, f"{SPECIAL_CHARACTERS.get(char, '')}.png")

    if not os.path.isfile(char_img_path):
        return None
    return char_img_path

# Generates an image from the given text using character images from specified fonts.
def generate_image(text, filename, font_paths):
    img_height = None
    char_images = {}
    img_path = os.path.join(DESKTOP_PATH, filename)

    try:
        total_width = 0

        # Iterate through each character in the input text
        for char in text:
            if char == ' ':
                # Create an empty space character image
                char_img = Image.new("RGBA", (SPACE_WIDTH, img_height or 1), (0, 0, 0, 0))

            else:
                # Get the path to the character image based on the font
                char_img_path = get_character_image_path(char, font_paths)
                if not char_img_path:

                    raise FileNotFoundError(f"Image not found for character '{char}'")

                char_img = Image.open(char_img_path).convert("RGBA")

            char_images[char] = char_img
            img_height = char_img.height if img_height is None else img_height
            total_width += char_img.width

        # Create the final image and paste character images into it
        final_img = Image.new("RGBA", (total_width, img_height), (0, 0, 0, 0))
        x = 0

        for char in text:
            final_img.paste(char_images[char], (x, 0))
            x += char_images[char].width

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
