import sys
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from main import generate_filename, generate_image, get_font_paths

valid_colors_by_font = {
    1: ["Blue", "Orange", "Gold"],
    2: ["Blue", "Orange", "Gold"],
    3: ["Blue", "Orange"],
    4: ["Blue", "Orange", "Yellow"],
    5: ["Orange"]
}

save_locations = {
    'Home': Path.home(),
    'Desktop': Path.home() / 'Desktop',
    'Downloads': Path.home() / 'Downloads',
    'Documents': Path.home() / 'Documents',
    'Pictures': Path.home() / 'Pictures'
}

def display_intro_messages():
    print("\nMetalSlugFontReborn v1.8.0 (Dev)")
    print("Maintained by VermeilChan")
    print("GPL-3.0 Licensed")
    print("https://github.com/VermeilChan/MetalSlugFontReborn\n")
    print("You can check the supported characters in SUPPORTED.txt.")
    print("Type 'exit' or press CTRL+C to close the program.")

def get_valid_input(prompt_text, valid_values):
    completer = WordCompleter(valid_values)
    while True:
        user_input = prompt(prompt_text, completer=completer)
        if user_input.lower() == 'exit':
            sys.exit('Closing...')
        elif user_input.title() in valid_values:
            return user_input.title()
        else:
            print("Invalid input. Please try again.")

def select_font():
    valid_fonts = list(map(str, range(1, 6)))
    return int(get_valid_input("\nChoose a font (1-5): ", valid_fonts))

def select_color(font):
    valid_colors = valid_colors_by_font.get(font, [])
    return get_valid_input(f"Available colors: {', '.join(valid_colors)}\nChoose a color: ", valid_colors)

def select_save_location():
    default_locations = list(save_locations.keys())
    save_location_prompt = f"Select save location:\n{', '.join(default_locations)}: "
    save_location = get_valid_input(save_location_prompt, default_locations)
    return save_locations[save_location]

def generate_and_display_image(text, font, color, save_location):
    if text.lower() == 'exit':
        sys.exit('Closing...')

    if not text:
        return print("Input text is empty. Please enter some text.")

    text = text.upper() if font == 5 else text

    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        image_path, error_message_generate = generate_image(text, filename, font_paths, save_location)

        if error_message_generate:
            print(f"Error generating image: {error_message_generate}")
        else:
            print(f"You can find the generated image here: {image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    display_intro_messages()

    font = select_font()
    color = select_color(font)
    save_location = select_save_location()

    try:
        while True:
            text = prompt("Enter the text you want to generate: ")
            generate_and_display_image(text, font, color, save_location)
    except KeyboardInterrupt:
        sys.exit('Closing...')

if __name__ == "__main__":
    main()
