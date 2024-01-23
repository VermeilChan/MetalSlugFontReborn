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
    print("\nYou can check the supported characters in SUPPORTED.txt.")

def get_user_input():
    return input("Enter the text you want to generate (type 'exit' to close): ")

def get_valid_input(prompt, valid_values):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            sys.exit('Closing...')
        elif user_input in valid_values:
            return user_input
        else:
            print(f"Invalid input. Please choose from {', '.join(valid_values)}.")

def select_font():
    valid_fonts = [str(i) for i in range(1, 6)]
    return int(get_valid_input("\nChoose a font from 1 to 5: ", valid_fonts))

def select_color(font):
    valid_colors = VALID_COLORS_BY_FONT.get(font, [])
    return get_valid_input(f"Available colors: {', '.join(valid_colors)}\nChoose a color: ", valid_colors).title()

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

    font = select_font()
    color = select_color(font)

    try:
        while True:
            text = get_user_input()
            generate_and_display_image(text, font, color)
    except KeyboardInterrupt:
        sys.exit('Closing...')

if __name__ == "__main__":
    main()
