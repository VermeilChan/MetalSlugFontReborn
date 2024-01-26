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
    print("\nMetalSlugFontReborn")
    print("You can check the supported characters in SUPPORTED.txt.")
    print("Type 'exit' to close the program.")

def get_user_input(prompt):
    return input(prompt).strip()

def get_valid_input(prompt, valid_values):
    while True:
        user_input = get_user_input(prompt)
        if user_input.lower() == 'exit':
            sys.exit('Closing...')
        elif user_input in valid_values:
            return user_input.title()
        else:
            print("Invalid input. Please try again.")

def select_font():
    valid_fonts = map(str, range(1, 6))
    return int(get_valid_input("\nChoose a font (1-5): ", valid_fonts))

def select_color(font):
    valid_colors = VALID_COLORS_BY_FONT.get(font, [])
    return get_valid_input(f"Available colors: {', '.join(valid_colors)}\nChoose a color: ", valid_colors)

def generate_and_display_image(text, font, color):
    if text.lower() == 'exit':
        sys.exit('Closing...')

    if not text:
        return print("Input text is empty. Please enter some text.")

    text = text.upper() if font == 5 else text

    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        image_path, error_message_generate = generate_image(text, filename, font_paths)

        if error_message_generate:
            print(f"Error generating image: {error_message_generate}")
        else:
            print(f"You can find the generated image here: {image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    display_intro_message()

    font = select_font()
    color = select_color(font)

    try:
        while True:
            text = get_user_input("Enter the text you want to generate: ")
            generate_and_display_image(text, font, color)
    except KeyboardInterrupt:
        sys.exit('Closing...')

if __name__ == "__main__":
    main()
