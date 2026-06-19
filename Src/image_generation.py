from pathlib import Path
from uuid import uuid4

from PIL import Image

from special_characters import special_characters

MAX_IMAGE_PIXELS = 220434240

SPACE_CHARACTER_WIDTH = 25
SPACE_CHARACTER_HEIGHT = 1
EMPTY_LINE_HEIGHT = 50

TRANSPARENT_COLOR = (0, 0, 0, 0)

DEFAULT_COMPRESS_LEVEL = 6
DEFAULT_MAX_WORDS = None

IMAGE_MODE = "RGBA"
IMAGE_EXTENSION = ".png"

FONTS_BASE_DIR = Path("Assets/Fonts")

Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


def generate_filename(_=None):
    return f"{uuid4().hex}{IMAGE_EXTENSION}"


def get_font_paths(font, color):
    base = FONTS_BASE_DIR / f"Font-{font}" / f"MS-{color}"
    return {
        "letters": base / "Letters",
        "numbers": base / "Numbers",
        "symbols": base / "Symbols",
    }

def get_character_path(character, font_paths):
    if character.isspace():
        return None
    elif character.islower():
        return font_paths["letters"] / "Lower-Case" / f"{character}.png"
    elif character.isupper():
        return font_paths["letters"] / "Upper-Case" / f"{character}.png"
    elif character.isdigit():
        return font_paths["numbers"] / f"{character}.png"

    if character not in special_characters:
        raise FileNotFoundError(
            f"The character '{character}' is not supported. Please check SUPPORTED.txt"
        )

    return font_paths["symbols"] / f"{special_characters[character]}.png"

def create_character_image(character, font_paths):
    if character.isspace():
        return Image.new(
            IMAGE_MODE,
            (SPACE_CHARACTER_WIDTH, SPACE_CHARACTER_HEIGHT),
            TRANSPARENT_COLOR,
        )

    path = get_character_path(character, font_paths)
    if path and path.is_file():
        return Image.open(path)

    raise FileNotFoundError(
        f"The character '{character}' is not supported. Please check SUPPORTED.txt"
    )

def split_into_lines(text, max_words):
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split()
        if max_words and words:
            lines.extend(
                [
                    " ".join(words[i : i + max_words])
                    for i in range(0, len(words), max_words)
                ]
            )
        elif not words:
            lines.append("\n")
        else:
            lines.append(paragraph)
    return lines

def generate_image(
    text,
    filename,
    font_paths,
    save_dir,
    max_words=DEFAULT_MAX_WORDS,
    compress_level=DEFAULT_COMPRESS_LEVEL,
):
    lines = split_into_lines(text, max_words)
    all_chars = {c for line in lines for c in line if c != "\n"}
    char_images = {char: create_character_image(char, font_paths) for char in all_chars}

    line_images = []
    max_width = total_height = 0

    for line in lines:
        if line == "\n":
            line_height = EMPTY_LINE_HEIGHT
            line_img = Image.new(IMAGE_MODE, (1, line_height), TRANSPARENT_COLOR)
            line_images.append(line_img)
            total_height += line_height
            continue

        line_width = sum(char_images[c].width for c in line)
        line_height = max(char_images[c].height for c in line) if line else 0
        line_img = Image.new(IMAGE_MODE, (line_width, line_height), TRANSPARENT_COLOR)

        x = 0
        for char in line:
            img = char_images[char]
            line_img.paste(img, (x, line_height - img.height), img)
            x += img.width

        line_images.append(line_img)
        max_width = max(max_width, line_width)
        total_height += line_height

    final_image = Image.new(IMAGE_MODE, (max_width, total_height), TRANSPARENT_COLOR)
    y = 0
    for img in line_images:
        final_image.paste(img, (0, y), img)
        y += img.height

    save_path = Path(save_dir) / filename
    final_image.save(save_path, compress_level=compress_level)
    return str(save_path), None
