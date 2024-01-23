import sys
from main import generate_filename, generate_image, get_font_paths

VALID_COLORS_BY_FONT = {
    1: ["Blue", "Orange-1", "Orange-2"],
    2: ["Blue", "Orange-1", "Orange-2"],
    3: ["Blue", "Orange-1"],
    4: ["Blue", "Orange-1", "Yellow"],
    5: ["Orange-1"]
}

def display_intro_message():
    print("Note:\nConverting your text to the Metal Slug font may not work with all fonts.")

def get_user_input():
    return input("Enter the text you want to generate: ")

def select_font_and_color():
    while True:
        font_input = input("\nChoose a font from 1 to 5 (type 'exit' to close): ")
        if font_input.lower() == 'exit':
            sys.exit('Closing...')

        try:
            font = int(font_input)
            if 1 <= font <= 5:
                valid_colors = VALID_COLORS_BY_FONT.get(font, [])
                color = get_valid_color(valid_colors)
                return font, color
            else:
                print("Invalid input. Please choose a font between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_color(valid_colors):
    while True:
        print("Available colors: " + " | ".join(valid_colors))
        color_input = input("Choose a color: ")

        if color_input.lower() == 'exit':
            sys.exit('Closing...')

        color = color_input.title()
        if color in valid_colors:
            return color

        print("\nInvalid color. Please choose a valid color.\n")

def ask_to_check_supported_characters():
    check_supported = input("Do you want to check the supported characters? [Y/n]: ").lower()

    if check_supported == 'y':
        print_supported_characters()
    elif check_supported != 'n':
        print("Invalid input. Defaulting to 'n'.")

    print("You can check them later if you want in SUPPORTED.txt")

def print_supported_characters():
    with open("Documentation/SUPPORTED.txt", "r", encoding="utf-8") as supported_file:
        content = supported_file.read()
        print(f"{content}\nNote:\nSome characters may not load due to terminal compatibility.\nYou can open SUPPORTED.txt if it doesn't work properly")

def generate_and_display_image(text, font, color):
    if text.lower() == 'exit':
        sys.exit('Closing...')

    if not text.strip():
        print("Input text is empty. Please enter some text.")
        return

    if font == 5:
        text = text.upper()

    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        image_path, error_message_generate = generate_image(text, filename, font_paths)

        if error_message_generate:
            print(f"Error: {error_message_generate}")
        else:
            print(f"You can find the image on your desktop:\n{image_path}")

    except Exception as e:
        print(f"Error: {e}")

def main():
    display_intro_message()
    ask_to_check_supported_characters()

    font, color = select_font_and_color()

    try:
        while True:
            text = get_user_input()
            generate_and_display_image(text, font, color)
    except KeyboardInterrupt:
        sys.exit('Closing...')

if __name__ == "__main__":
    main()
