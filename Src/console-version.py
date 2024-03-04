import sys
from main import generate_filename, generate_image, get_font_paths

valid_colors_by_font = {
    1: ["Blue", "Orange-1", "Orange-2"],
    2: ["Blue", "Orange-1", "Orange-2"],
    3: ["Blue", "Orange-1"],
    4: ["Blue", "Orange-1", "Yellow"],
    5: ["Orange-1"]
}

def display_welcome_message():
    print("\nMetalSlugFontReborn v1.7.0")
    print("You can check the supported characters in SUPPORTED.txt.")
    print("Type 'exit' to close the program.")

def get_input(prompt):
    return input(prompt).strip()

def get_valid_input(prompt, valid_values):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            sys.exit('Closing...')
        elif user_input in valid_values:
            return user_input.title()
        else:
            print("Invalid input. Please try again.")

def select_font():
    valid_font_numbers = [str(num) for num in range(1, 6)]
    user_choice = int(get_valid_input("\nChoose a font (1-5): ", valid_font_numbers))
    return user_choice

def select_color(font):
    valid_colors = valid_colors_by_font.get(font, [])
    available_colors = ', '.join(valid_colors)
    return get_valid_input(f"Available colors: {available_colors}\nChoose a color: ", valid_colors)

def generate_and_display_image(input_text, selected_font, selected_color):
    if input_text.lower() == 'exit':
        sys.exit('Closing...')

    if not input_text:
        return print("Input text is empty. Please enter some text.")

    text = input_text.upper() if selected_font == 5 else input_text

    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(selected_font, selected_color)
        image_path, error_message = generate_image(text, filename, font_paths)

        if error_message:
            print(f"Error generating image: {error_message}")
        else:
            print(f"You can find the generated image here: {image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    display_welcome_message()

    selected_font = select_font()
    selected_color = select_color(selected_font)

    try:
        while True:
            user_input = get_input("Enter the text you want to generate: ")
            generate_and_display_image(user_input, selected_font, selected_color)
    except KeyboardInterrupt:
        sys.exit('Closing...')

if __name__ == "__main__":
    main()
