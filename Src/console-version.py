import sys

from main import generate_filename, generate_image, get_font_paths

from constants import CLOSING_MESSAGE, VALID_COLORS_BY_FONT, DESKTOP_PATH

def display_intro_message():
    print("Note: Converting your text input to the Metal Slug font may not work with all fonts.")
    print("Please refer to the details provided in the SUPPORTED.md file for more information.")

def get_user_input():
    return input("Enter the text you want to generate (type 'exit' to close): ")

def select_font_and_color():
    while True:
        try:
            user_input = input("Choose a font from 1 to 5 (Refer to EXAMPLE.md for Font Preview) or type 'exit' to close: ")

            if user_input.lower() == 'exit':
                print(CLOSING_MESSAGE)
                sys.exit(0)

            font = int(user_input)

            if font in VALID_COLORS_BY_FONT:
                valid_colors = VALID_COLORS_BY_FONT[font]
                print("Available colors: " + " | ".join(valid_colors))
                color_input = input("Enter the color you want to use or type 'exit' to close: ")

                if color_input.lower() == 'exit':
                    print(CLOSING_MESSAGE)
                    sys.exit(0)
                elif color_input.title() in valid_colors:
                    color_input = color_input.title()
                    return font, color_input
                else:
                    print("Invalid color. Please choose a valid color.")
            else:
                print("Invalid input. Please choose a font between 1 and 5.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print(CLOSING_MESSAGE)
            sys.exit(0)

def generate_and_display_image(text, font, color):
    if text.lower() == 'exit':
        print(CLOSING_MESSAGE)
        sys.exit(0)

    if not text.strip():
        print("Input text is empty. Please enter some text.")
        return

    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        img_path, error_message_generate = generate_image(text, filename, font_paths)

        if error_message_generate:
            print(f"Error: {error_message_generate}")
        else:
            print(f"Image successfully generated and saved as: {filename}")
            print(f"You can find the image on your desktop: {DESKTOP_PATH / img_path}")

    except Exception as e:
        print(f"Error: {e}")
        print(CLOSING_MESSAGE)
        sys.exit(0)

def main():
    display_intro_message()

    font, color = select_font_and_color()

    try:
        while True:
            text = get_user_input()
            generate_and_display_image(text, font, color)
    except KeyboardInterrupt:
        print(CLOSING_MESSAGE)
        sys.exit(0)

if __name__ == "__main__":
    main()
