import sys
from time import time
from PIL import Image
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from image_generation import (
    generate_filename,
    generate_image,
    get_font_paths,
    compress_image,
)
from info import msfr_version, build_date

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
    print(f"\nMetalSlugFontReborn {msfr_version}")
    print(f"Build Date: {build_date}")
    print("Maintained by VermeilChan")
    print("GPL-3.0 Licensed")
    print("Repository: https://github.com/VermeilChan/MetalSlugFontReborn\n")
    print("You can check the supported characters in SUPPORTED.txt.")
    print("Type 'exit' or press CTRL+C to close the program.")


def get_valid_input(prompt_text, valid_values):
    completer = WordCompleter(valid_values)
    while True:
        user_input = prompt(prompt_text, completer=completer).title()
        if user_input == "Exit":
            sys.exit("Closing...")
        elif user_input in valid_values:
            return user_input
        else:
            print("Invalid input. Please try again.")


def select_font():
    return int(get_valid_input("\nChoose a font (1-5): ", list(map(str, range(1, 6)))))


def select_color(font):
    valid_colors = valid_colors_by_font.get(font, [])
    return get_valid_input(
        f"Available colors: {', '.join(valid_colors)}\nChoose a color: ", valid_colors
    )


def select_save_location():
    default_locations = list(save_locations.keys()) + ["Custom"]
    save_location_choice = get_valid_input(
        f"Select save location:\n{', '.join(default_locations)}: ", default_locations
    )

    if save_location_choice == "Custom":
        custom_path = Path(prompt("Enter a custom path for saving: "))
        if not custom_path.exists():
            try:
                custom_path.mkdir(parents=True)
            except Exception as e:
                print(f"Could not create the specified path. Error: {e}")
                return select_save_location()
        return custom_path
    else:
        return save_locations[save_location_choice]


def ask_compression():
    compress_completer = WordCompleter(["yes", "no", "y", "n"])
    compress_input = prompt(
        "Do you want to compress the image? (Y/n): ", completer=compress_completer
    ).lower()
    return bool(compress_input in {"yes", "y"})


def ask_line_breaks():
    line_break_completer = WordCompleter(["yes", "no", "y", "n"])
    line_break_input = prompt(
        "Do you want to enable line breaks? (Y/n): ", completer=line_break_completer
    ).lower()
    if line_break_input in {"yes", "y"}:
        max_words_per_line = int(prompt("Enter the maximum number of words per line: "))
        return max_words_per_line
    return None


def human_readable_size(size_bytes):
    if size_bytes == 0:
        return "0 bytes"
    size_units = ["bytes", "KB", "MB"]
    i = 0
    size = size_bytes
    while size >= 1024 and i < len(size_units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {size_units[i]}"


def generate_and_info(
    text, font, color, save_location, compress=False, max_words_per_line=None
):
    if text.lower() == "exit":
        sys.exit("Closing...")

    if not text:
        return print("Input text is empty. Please enter some text.")

    text = text.upper() if font == 5 else text

    try:
        start_time = time()
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        image_path_str, error_message_generate = generate_image(
            text, filename, font_paths, save_location, max_words_per_line
        )

        if error_message_generate:
            print(f"Error generating image: {error_message_generate}")
            return

        if compress:
            compress_image(image_path_str)

        end_time = time()
        image_path = Path(image_path_str)
        with Image.open(image_path) as img:
            width, height = img.size
            size_bytes = image_path.stat().st_size
            size_human_readable = human_readable_size(size_bytes)
            success_message = (
                f"Image path: {image_path}\n"
                f"Width: {width}, Height: {height} | Size: {size_human_readable} | Generation time: {end_time - start_time:.3f}s\n"
            )
            print(success_message)

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    startup_message()
    font = select_font()
    color = select_color(font)
    save_location = select_save_location()

    compress = ask_compression()
    max_words_per_line = ask_line_breaks()

    try:
        while True:
            text = prompt("Enter the text you want to generate: ")
            generate_and_info(
                text, font, color, save_location, compress, max_words_per_line
            )
    except KeyboardInterrupt:
        sys.exit("Closing...")


if __name__ == "__main__":
    main()
