import sys
from time import time
from PIL import Image
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from image_generation import generate_filename, generate_image, get_font_paths, compress_image
from utils import msfr_version, build_date, readable_size, get_os_info

valid_colors_by_font = {
    1: ["Blue", "Orange", "Gold"],
    2: ["Blue", "Orange", "Gold"],
    3: ["Blue", "Orange"],
    4: ["Blue", "Orange", "Yellow"],
    5: ["Orange"],
}

save_locations = {
    "Home": Path.home(),
    "Desktop": Path.home() / "Desktop",
    "Downloads": Path.home() / "Downloads",
    "Documents": Path.home() / "Documents",
    "Pictures": Path.home() / "Pictures",
}

def startup_message():
    print(f"MetalSlugFontReborn {msfr_version}, {get_os_info()}.")
    print(f"Build Date: {build_date}.\nSupported characters in SUPPORTED.txt.")
    print("Type 'exit' or press CTRL+C to close.")

def get_valid_input(prompt_text, valid_options):
    completer = WordCompleter(valid_options, ignore_case=True)
    while True:
        user_input = prompt(prompt_text, completer=completer).title()
        if user_input == "Exit":
            sys.exit("Closing...")
        if user_input in valid_options: 
            return user_input
        print("Invalid input. Please try again.")

def select_font():
    return int(get_valid_input("\nChoose a font (1-5): ", [str(n) for n in range(1, 6)]))

def select_color(font_number):
    colors = valid_colors_by_font[font_number]
    return get_valid_input(f"Available colors: {', '.join(colors)}\nChoose color: ", colors)

def select_save_location():
    options = list(save_locations.keys()) + ["Custom"]
    while True:
        choice = get_valid_input(f"Save location ({', '.join(options)}): ", options)
        if choice != "Custom":
            return save_locations[choice]
        
        custom_path = Path(prompt("Enter custom path: "))
        try:
            custom_path.mkdir(parents=True, exist_ok=True)
            return custom_path
        except (OSError, PermissionError) as error:
            print(f"Path creation failed: {error}")

def get_yes_no(prompt_text):
    return get_valid_input(prompt_text, ["Yes", "No"]) == "Yes"

def get_positive_integer(prompt_text):
    while True:
        try:
            value = int(prompt(prompt_text))
            return value if value > 0 else print("Enter positive number.")
        except ValueError:
            print("Invalid number. Try again.")

def get_compression_level():
    levels = [str(i) for i in range(10)]
    completer = WordCompleter(levels, ignore_case=False)
    while True:
        user_input = prompt("Compression level (0-9): ", completer=completer)
        if user_input in levels:
            return int(user_input)
        print("Invalid input. Use a number from 0 to 9.")

def handle_image_creation(text, font_number, color, save_path, max_words):
    filename = generate_filename(text)
    font_paths = get_font_paths(font_number, color)
    image_path, error = generate_image(text, filename, font_paths, save_path, max_words)
    if image_path:
        image_path = Path(image_path)
    return image_path, error

def display_image_info(image_path, start_time):
    end_time = time()
    image_path = Path(image_path)
    with Image.open(image_path) as img:
        size = readable_size(image_path.stat().st_size)
        print(f"Image path: {image_path}\n"
              f"Dimensions: {img.width}x{img.height} | Size: {size} | "
              f"Time: {end_time - start_time:.3f}s\n")

def process_text(text, font_number, color, save_path, compress, compression_level, max_words):
    if not text:
        print("Empty input. Please enter text.")
        return

    processed_text = text.upper() if font_number == 5 else text
    start_time = time()

    try:
        image_path, error = handle_image_creation(
            processed_text, font_number, color, save_path, max_words
        )
        if error:
            print(f"Generation error: {error}")
            return

        if compress:
            compress_image(image_path, compression_level)

        display_image_info(image_path, start_time)
    except Exception as error:
        print(f"Processing error: {error}")

def main():
    startup_message()
    font = select_font()
    color = select_color(font)
    save_path = select_save_location()
    compress = get_yes_no("Compress image? (Yes/No): ")
    compression_level = 6

    if compress:
        compression_level = get_compression_level()

    max_words = None
    if get_yes_no("Enable line breaks? (Yes/No): "):
        max_words = get_positive_integer("Enter max words per line: ")

    try:
        while True:
            text = prompt("Enter text to generate: ")
            process_text(text, font, color, save_path, compress, compression_level, max_words)
    except KeyboardInterrupt:
        sys.exit("Closing...")

if __name__ == "__main__":
    main()
