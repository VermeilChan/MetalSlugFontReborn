from uuid import uuid4
from pathlib import Path
from PIL import Image
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
        return Image.new("RGBA", (30, 0), (0, 0, 0, 0))

    character_image_path = get_character_image_path(character, font_paths)
    if not character_image_path or not character_image_path.is_file():
        raise FileNotFoundError(
            f"The character '{character}' is not supported, please check SUPPORTED.txt"
        )

    return Image.open(character_image_path)


def compress_image(image_path):
    with Image.open(image_path) as image:
        image.save(image_path, optimize=True)


def apply_line_breaks(text, max_words_per_line):
    words = text.split()
    return [
        " ".join(words[i : i + max_words_per_line])
        for i in range(0, len(words), max_words_per_line)
    ]


def generate_image(text, filename, font_paths, save_location, max_words_per_line=None):
    lines = (
        apply_line_breaks(text, max_words_per_line) if max_words_per_line else [text]
    )

    line_images = []
    max_width = total_height = 0

    for line in lines:
        font_images = {
            character: get_character_image(character, font_paths)
            for character in set(line)
        }
        line_width = sum(font_images[character].width for character in line)
        line_height = max(font_images[character].height for character in line)

        line_image = Image.new("RGBA", (line_width, line_height), (0, 0, 0, 0))
        x_position = 0

        for character in line:
            character_image = font_images[character]
            y_position = line_height - character_image.height
            line_image.paste(character_image, (x_position, y_position))
            x_position += character_image.width

        line_images.append(line_image)
        max_width = max(max_width, line_width)
        total_height += line_height

    final_image = Image.new("RGBA", (max_width, total_height), (0, 0, 0, 0))
    y_position = 0

    for line_image in line_images:
        final_image.paste(line_image, (0, y_position))
        y_position += line_image.height

    image_path = Path(save_location) / filename
    final_image.save(image_path)

    return str(image_path), None
