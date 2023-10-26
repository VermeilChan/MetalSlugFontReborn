# Import necessary libraries
import os
import sys

# Prevent the generation of .pyc (Python bytecode) files
sys.dont_write_bytecode = True

# Import necessary functions from the main module
from main import generate_filename, generate_image, get_font_paths
# Import necessary functions from the constants module
from constants import CLOSING_MESSAGE, VALID_COLORS_BY_FONT

# Function to display an introductory message
def display_intro_message():
    print("Note: Metal Slug Font style conversion may not be compatible with all fonts.")
    print("Refer to the SUPPORTED.md file for details.")

# Function to get user input for text to be converted
def get_user_input():
    return input("Enter the text you want to generate (type 'exit' to close): ")

# Function to allow the user to select a font and color
def select_font_and_color():
    while True:
        try:
            # Prompt the user to choose a font or exit
            user_input = input("Choose a font from 1 to 5 (Refer to EXAMPLE.md for Font Preview) or type 'exit' to close: ")

            if user_input.lower() == 'exit':
                print(CLOSING_MESSAGE)
                sys.exit(0)

            font = int(user_input)

            # Check if the chosen font is valid
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

# Function to generate and display an image based on user input
def generate_and_display_image(text, font, color):
    try:
        if text.lower() == 'exit':
            print(CLOSING_MESSAGE)
            sys.exit(0)

        # Check for empty input
        if not text.strip():
            print("Input text is empty. Please enter some text.")
            return

        filename = generate_filename(text)

        font_paths = get_font_paths(font, color)

        img_path, error_message_generate = generate_image(text, filename, font_paths)

        if error_message_generate:
            print(f"Error: {error_message_generate}")
        else:
            print(f"Image successfully generated and saved as: {img_path}")
            print(f"You can find the image on your desktop: {os.path.abspath(os.path.join(os.path.expanduser('~'), 'Desktop', img_path))}")

    except KeyboardInterrupt:
        print(CLOSING_MESSAGE)
        sys.exit(0)
    except FileNotFoundError as e:
        error_message_generate = f"Font file not found: {e.filename}"
        print(error_message_generate)
    except Exception as e:
        error_message_generate = f"An error occurred: {e}"
        print(error_message_generate)

# The main function of the program
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
    except Exception as e:
        error_message_main_inner = f"An unexpected error occurred: {e}"
        print(error_message_main_inner)

# Entry point of the script
if __name__ == "__main__":
    main()
