from pathlib import Path
from uuid import uuid4

from PIL import Image

from special_characters import special_characters

Image.MAX_IMAGE_PIXELS = 220434240

SPACE_CHARACTER_WIDTH = 25
SPACE_CHARACTER_HEIGHT = 1
EMPTY_LINE_HEIGHT = 50
LINE_SPACING = 15

TRANSPARENT_COLOR = (0, 0, 0, 0)

DEFAULT_COMPRESS_LEVEL = 6

IMAGE_MODE = "RGBA"
IMAGE_EXTENSION = ".png"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONTS_BASE_DIR = PROJECT_ROOT / "Assets" / "Fonts"


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
            f"Character '{character}' is not supported. Click on the view supported characters button for the list of allowed characters"
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
    if path.is_file():
        return Image.open(path)

    raise FileNotFoundError(
        f"Character '{character}' is not supported. Click on the view supported characters button for the list of allowed characters"
    )


def split_into_lines(text):
    return text.split("\n")


def generate_image(
    text,
    filename,
    font_paths,
    save_dir,
    compress_level=DEFAULT_COMPRESS_LEVEL,
    return_image=False,
    scale=1,
):
    lines = split_into_lines(text)
    all_chars = {c for line in lines for c in line}
    char_images = {char: create_character_image(char, font_paths) for char in all_chars}

    line_images = []
    max_width = total_height = 0

    for i, line in enumerate(lines):
        if not line:
            line_height = EMPTY_LINE_HEIGHT
            line_img = Image.new(IMAGE_MODE, (1, line_height), TRANSPARENT_COLOR)
            line_images.append(line_img)
            total_height += line_height
            if i < len(lines) - 1:
                total_height += LINE_SPACING
            continue

        line_width = sum(char_images[c].width for c in line)
        line_height = max(char_images[c].height for c in line)
        line_img = Image.new(IMAGE_MODE, (line_width, line_height), TRANSPARENT_COLOR)

        x = 0
        for char in line:
            img = char_images[char]
            line_img.paste(img, (x, line_height - img.height), img)
            x += img.width

        line_images.append(line_img)
        max_width = max(max_width, line_width)
        total_height += line_height

        if i < len(lines) - 1:
            total_height += LINE_SPACING

    final_image = Image.new(IMAGE_MODE, (max_width, total_height), TRANSPARENT_COLOR)
    y = 0
    for i, img in enumerate(line_images):
        final_image.paste(img, (0, y), img)
        y += img.height
        if i < len(line_images) - 1:
            y += LINE_SPACING

    if scale > 1:
        final_image = final_image.resize(
            (final_image.width * scale, final_image.height * scale),
            Image.Resampling.NEAREST,
        )

    width, height = final_image.size

    if return_image:
        return final_image, width, height

    save_path = Path(save_dir) / filename
    final_image.save(save_path, compress_level=compress_level)
    return str(save_path), width, height
