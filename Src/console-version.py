import sys
from termcolor import cprint

from main import generate_filename, generate_image, get_font_paths

from constants import VALID_COLORS_BY_FONT, DESKTOP_PATH

def display_intro_message():
    cprint(f"\nNote: Converting your text to the Metal Slug font may not work with all fonts.", 'yellow', attrs=['bold'])
    cprint(f"Please refer to SUPPORTED.txt file for more information.\n", 'yellow', attrs=['underline'])

def get_user_input():
    return input(f"\nEnter the text you want to generate: ")

def select_font_and_color():
    while True:
        try:
            user_input = input(f"Choose a font from 1 to 5 (type 'exit' to close): ")

            if user_input.lower() == 'exit':
                cprint(f'\nClosing...\n', 'blue')
                sys.exit(0)

            font = int(user_input)

            if 1 <= font <= 5:
                valid_colors = VALID_COLORS_BY_FONT.get(font, [])
                cprint(f"\nAvailable colors: " + " | ".join(valid_colors), 'blue')
                color_input = input(f"\nChoose a color: ")

                if color_input.lower() == 'exit':
                    cprint(f'\nClosing...\n', 'blue')
                    sys.exit(0)
                elif color_input.title() in valid_colors:
                    color_input = color_input.title()
                    return font, color_input
                else:
                    cprint(f"\nInvalid color. Please choose a valid color.\n", 'red')
            else:
                cprint(f"\nInvalid input. Please choose a font between 1 and 5.\n", 'red')

        except ValueError:
            cprint(f"\nInvalid input. Please enter a valid number.\n", 'red')
        except KeyboardInterrupt:
            cprint(f'\nClosing...\n', 'blue')
            sys.exit(0)

def ask_to_check_supported_characters():
    check_supported = input(f"Do you want to check the supported characters? [Y/n]: ").lower()

    if check_supported == 'y':
        with open(f"Documentation/SUPPORTED.txt", "r") as supported_file:
            content = supported_file.read()
            cprint(content, 'blue')
            cprint(f"Note:", 'light_magenta')
            cprint(f"Some characters may not load due to font limitations or console compatibility.\n", 'light_magenta')
    elif check_supported == 'n':
        pass
    else:
        cprint(f"\nInvalid input.\n", 'red')

def generate_and_display_image(text, font, color):
    if text.lower() == 'exit':
        cprint(f'\nClosing...\n', 'blue')
        sys.exit(0)

    if not text.strip():
        cprint(f"Input text is empty. Please enter some text.", 'red')
        return

    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        img_path, error_message_generate = generate_image(text, filename, font_paths)

        if error_message_generate:
            cprint(f"Error: {error_message_generate}", 'red')
        else:
            cprint(f"\nImage saved as: {filename}", 'green')
            cprint(f"\nYou can find the image on your desktop: \n{DESKTOP_PATH / img_path}", 'magenta')

    except Exception as e:
        cprint(f"Error: {e}", 'red')

def main():
    display_intro_message()
    ask_to_check_supported_characters()

    font, color = select_font_and_color()

    try:
        while True:
            text = get_user_input()
            generate_and_display_image(text, font, color)
    except KeyboardInterrupt:
        cprint(f'\nClosing...\n', 'light_grey')
        sys.exit(0)

if __name__ == "__main__":
    main()
