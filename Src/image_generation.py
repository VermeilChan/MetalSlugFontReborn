from uuid import uuid4
from pathlib import Path
from PIL import Image
from special_characters import special_characters

Image.MAX_IMAGE_PIXELS = 220434240

def generate_filename(_):
    return f"{uuid4().hex}.png"

def get_font_paths(font, color):
    base = Path("Assets/Fonts") / f"Font-{font}" / f"MS-{color}"
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
    return font_paths["symbols"] / f"{special_characters.get(character, '')}.png"

def create_character_image(character, font_paths):
    if character.isspace():
        return Image.new("RGBA", (30, 0), (0, 0, 0, 0))
    
    if (path := get_character_path(character, font_paths)) and path.is_file():
        return Image.open(path)
    
    raise FileNotFoundError(
        f"The character '{character}' is not supported. Please check SUPPORTED.txt"
    )

def compress_image(image_path):
    with Image.open(image_path) as img:
        img.save(image_path, optimize=True)

def split_into_lines(text, max_words):
    words = text.split()
    return [
        " ".join(words[i:i+max_words])
        for i in range(0, len(words), max_words)
    ] if max_words else [text]

def generate_image(text, filename, font_paths, save_dir, max_words=None):
    lines = split_into_lines(text, max_words)
    all_chars = {c for line in lines for c in line}
    char_images = {char: create_character_image(char, font_paths) for char in all_chars}

    line_images = []
    max_width = total_height = 0

    for line in lines:
        if not line:
            continue
            
        line_width = sum(char_images[c].width for c in line)
        line_height = max(char_images[c].height for c in line) if line else 0
        line_img = Image.new("RGBA", (line_width, line_height), (0, 0, 0, 0))
        
        x = 0
        for char in line:
            img = char_images[char]
            line_img.paste(img, (x, line_height - img.height))
            x += img.width
        
        line_images.append(line_img)
        max_width = max(max_width, line_width)
        total_height += line_height

    final_image = Image.new("RGBA", (max_width, total_height))
    y = 0
    for img in line_images:
        final_image.paste(img, (0, y))
        y += img.height

    save_path = Path(save_dir) / filename
    final_image.save(save_path)
    return str(save_path), None
