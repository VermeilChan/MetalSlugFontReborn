from uuid import uuid4
from numpy import zeros, uint8
from cv2 import imread, imwrite ,IMWRITE_PNG_COMPRESSION, IMREAD_UNCHANGED, COLOR_BGR2BGRA, cvtColor
from pathlib import Path
from special_characters import special_characters


def generate_filename(_):
    return f"{uuid4().hex}.png"


def get_font_paths(font, color):
    base_path = Path("Assets") / "Fonts" / f"Font-{font}" / f"MS-{color}"
    return [base_path / folder for folder in ("Letters", "Numbers", "Symbols")]


def get_character_image_path(character, font_paths):
    characters_folder, numbers_folder, symbols_folder = font_paths

    if character.isspace():
        return None
    elif character.islower():
        return characters_folder / "Lower-Case" / f"{character}.png"
    elif character.isupper():
        return characters_folder / "Upper-Case" / f"{character}.png"
    elif character.isdigit():
        return numbers_folder / f"{character}.png"
    else:
        return symbols_folder / f"{special_characters.get(character, '')}.png"


def get_character_image(character, font_paths):
    if character.isspace():
        return zeros((1, 0, 4), dtype=uint8)

    character_image_path = get_character_image_path(character, font_paths)
    if not character_image_path or not character_image_path.is_file():
        raise FileNotFoundError(
            f"The character '{character}' is not supported, please check SUPPORTED.txt"
        )

    return cvtColor(imread(str(character_image_path), IMREAD_UNCHANGED), COLOR_BGR2BGRA)


def compress_image(image_path):
    image = imread(image_path, IMREAD_UNCHANGED)
    imwrite(image_path, image, [IMWRITE_PNG_COMPRESSION, 9])


def apply_line_breaks(text, max_words_per_line):
    words = text.split()
    return [" ".join(words[i: i + max_words_per_line]) for i in range(0, len(words), max_words_per_line)]


def generate_image(text, filename, font_paths, save_location, max_words_per_line=None):
    lines = (apply_line_breaks(text, max_words_per_line) if max_words_per_line else [text])

    line_images = []
    max_width = total_height = 0

    for line in lines:
        font_images = {character: get_character_image(character, font_paths) for character in set(line)}
        line_width = sum(font_images[character].shape[1] for character in line)
        line_height = max(font_images[character].shape[0] for character in line)

        line_image = zeros((line_height, line_width, 4), dtype=uint8)
        x_position = 0

        for character in line:
            character_image = font_images[character]
            y_position = line_height - character_image.shape[0]
            line_image[y_position:y_position + character_image.shape[0], 
                       x_position:x_position + character_image.shape[1]] = character_image
            x_position += character_image.shape[1]

        line_images.append(line_image)
        max_width = max(max_width, line_width)
        total_height += line_height

    final_image = zeros((total_height, max_width, 4), dtype=uint8)
    y_position = 0

    for line_image in line_images:
        final_image[y_position:y_position + line_image.shape[0], :line_image.shape[1]] = line_image
        y_position += line_image.shape[0]

    image_path = Path(save_location) / filename
    imwrite(str(image_path), final_image)

    return str(image_path), None
