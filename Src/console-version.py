import sys
from time import time
from PIL import Image
from pathlib import Path
from prompt_toolkit import prompt
from platform import system, architecture
from prompt_toolkit.completion import WordCompleter
from image_generation import generate_filename, generate_image, get_font_paths, compress_image
from info import msfr_version, build_date
from qt_utils import readable_size

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
    print(
        f"\nMetalSlugFontReborn {msfr_version}, {system()} ({architecture()[0]}), Build Date {build_date}."
    )
    print("Maintained by VermeilChan, GPL-3.0 Licensed.")
    print("Repository: https://github.com/VermeilChan/MetalSlugFontReborn\n")
    print("You can check the supported characters in SUPPORTED.txt.")
    print("Type 'exit' or press CTRL+C to close the program.")


def get_valid_input(prompt_text, valid_values):
    completer = WordCompleter(valid_values)
    while True:
        user_input = prompt(prompt_text, completer=completer).title()
        if user_input == "Exit":
            sys.exit("Closing...")
        if user_input in valid_values:
            return user_input
        print("Invalid input. Please try again.")


def select_font():
    return int(get_valid_input("\nChoose a font (1-5): ", list(map(str, range(1, 6)))))


def select_color(font):
    valid_colors = valid_colors_by_font[font]
    return get_valid_input(
        f"Available colors: {', '.join(valid_colors)}\nChoose a color: ", valid_colors
    )


def select_save_location():
    options = list(save_locations.keys()) + ["Custom"]
    choice = get_valid_input(f"Select save location:\n{', '.join(options)}: ", options)

    if choice == "Custom":
        custom_path = Path(prompt("Enter a custom path for saving: "))
        if not custom_path.exists():
            try:
                custom_path.mkdir(parents=True)
            except Exception as e:
                print(f"Could not create the specified path. Error: {e}")
                return select_save_location()
        return custom_path
    return save_locations[choice]


def ask_compression():
    return get_valid_input("Do you want to compress the image? (Yes/No): ", ["Yes", "No"]) == "Yes"


def ask_line_breaks():
    line_break_choice = get_valid_input("Do you want to enable line breaks? (Yes/No): ", ["Yes", "No"])
    if line_break_choice == "Yes":
        while True:
            try:
                max_words_per_line = int(prompt("Enter the maximum number of words per line: "))
                if max_words_per_line > 0:
                    return max_words_per_line
                print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    return None


def generate_and_info(
    text, font, color, save_location, compress=False, max_words_per_line=None
):
    if not text:
        return print("Input text is empty. Please enter some text.")

    text = text.upper() if font == 5 else text

    try:
        start_time = time()
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        image_path, error_message = generate_image(text, filename, font_paths, save_location, max_words_per_line)

        if error_message:
            print(f"Error generating image: {error_message}")
            return

        if compress:
            compress_image(image_path)

        end_time = time()
        image_path = Path(image_path)
        with Image.open(image_path) as image:
            width, height = image.size
            size_bytes = image_path.stat().st_size
            size_human_readable = readable_size(size_bytes)
            success_message = (
                f"Image path: {image_path}\n"
                f"Width: {width}, Height: {height} | Size: {size_human_readable} | Generation time: {end_time - start_time:.3f}s\n")
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
            generate_and_info(text, font, color, save_location, compress, max_words_per_line)
    except KeyboardInterrupt:
        sys.exit("Closing...")


if __name__ == "__main__":
    main()
