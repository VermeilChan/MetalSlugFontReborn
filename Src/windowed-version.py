# Import necessary libraries
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Prevent the generation of .pyc (Python bytecode) files
sys.dont_write_bytecode = True

from main import generate_filename, generate_image, get_font_paths

# Define valid color options for each font
VALID_COLORS_BY_FONT = {
    1: ["Blue", "Orange-1", "Orange-2"],
    2: ["Blue", "Orange-1", "Orange-2"],
    3: ["Blue", "Orange-1"],
    4: ["Blue", "Orange-1"],
    5: ["Orange-1"]
}

# Define a constant for the closing message
CLOSING_MESSAGE = "Closing..."

# Function to generate and display an image based on user input
def generate_and_display_image():
    text = text_entry.get()
    font = int(font_var.get())
    color = color_var.get()

    try:
        if text.lower() == 'exit':
            messagebox.showinfo("Info", CLOSING_MESSAGE)
            root.quit()

        # Check for empty input
        if not text.strip():
            messagebox.showerror("Error", "Input text is empty. Please enter some text.")
            return

        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)

        img_path, error_message_generate = generate_image(text, filename, font_paths)

        if error_message_generate:
            messagebox.showerror("Error", f"Error: {error_message_generate}")
        else:
            messagebox.showinfo("Success", f"Image successfully generated and saved as: {img_path}")
    except FileNotFoundError as e:
        error_message_generate = f"Font file not found: {e.filename}"
        messagebox.showerror("Error", error_message_generate)
    except Exception as e:
        error_message_generate = f"An error occurred: {e}"
        messagebox.showerror("Error", error_message_generate)

# Function to handle font selection change
def on_font_change(*args):
    font = int(font_var.get())
    valid_colors = VALID_COLORS_BY_FONT.get(font, [])
    color_combobox['values'] = valid_colors
    color_var.set(valid_colors[0] if valid_colors else "")

# Create the main window
root = tk.Tk()
root.title("Metal Slug Font")

# Create a frame for input elements
frame = ttk.Frame(root, padding=20)
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label for text input
text_label = ttk.Label(frame, text="Enter the text:")
text_label.grid(column=0, row=0, sticky=tk.W)

# Text input field
text_entry = ttk.Entry(frame, width=40)
text_entry.grid(column=1, row=0, columnspan=2)

# Label for font selection
font_label = ttk.Label(frame, text="Choose a font:")
font_label.grid(column=0, row=1, sticky=tk.W)

# Font selection dropdown
font_var = tk.StringVar()
font_var.set("1")  # Default font selection
font_combobox = ttk.Combobox(frame, textvariable=font_var, values=["1", "2", "3", "4", "5"])
font_combobox.grid(column=1, row=1, columnspan=2)

# Label for color selection
color_label = ttk.Label(frame, text="Choose a color:")
color_label.grid(column=0, row=2, sticky=tk.W)

# Color selection dropdown
color_var = tk.StringVar()
color_var.set("Blue")  # Default color selection
color_combobox = ttk.Combobox(frame, textvariable=color_var, values=[])
color_combobox.grid(column=1, row=2, columnspan=2)

# Bind the font selection change event
font_var.trace("w", on_font_change)

# Generate button
generate_button = ttk.Button(frame, text="Generate Image", command=generate_and_display_image)
generate_button.grid(column=0, row=3, columnspan=3)

# Add padding and make widgets expand
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5, sticky=(tk.W, tk.E))

# Run the tkinter main loop
root.mainloop()