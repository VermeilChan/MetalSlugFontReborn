# Import necessary libraries
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle

# Prevent the generation of .pyc (Python bytecode) files
sys.dont_write_bytecode = True

# Import necessary functions from the main module
from main import generate_filename, generate_image, get_font_paths
# Import necessary functions from the constants module
from constants import VALID_COLORS_BY_FONT, CLOSING_MESSAGE

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

        # Generate a filename based on the input text
        filename = generate_filename(text)

        # Get the font paths based on user selections
        font_paths = get_font_paths(font, color)

        # Generate the image and handle any errors
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

# Apply the dark theme
style = ThemedStyle(root)
style.set_theme("equilux")

# Create a frame for input elements
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

# Label for text input
text_label = ttk.Label(frame, text="Text to Generate:")
text_label.grid(row=0, column=0, columnspan=3, sticky="w")

# Text input field
text_entry = ttk.Entry(frame)
text_entry.grid(row=1, column=0, columnspan=3, sticky="ew")

# Label for font selection
font_label = ttk.Label(frame, text="Select Font:")
font_label.grid(row=2, column=0, columnspan=3, sticky="w")

# Font selection dropdown
font_var = tk.StringVar()
font_var.set("1")  # Default font selection
font_combobox = ttk.Combobox(frame, textvariable=font_var, values=["1", "2", "3", "4", "5"])
font_combobox.grid(row=3, column=0, columnspan=3, sticky="ew")

# Label for color selection
color_label = ttk.Label(frame, text="Select Color:")
color_label.grid(row=4, column=0, columnspan=3, sticky="w")

# Color selection dropdown
color_var = tk.StringVar()
color_var.set("Blue")  # Default color selection
color_combobox = ttk.Combobox(frame, textvariable=color_var, values=[])
color_combobox.grid(row=5, column=0, columnspan=3, sticky="ew")

# Bind the font selection change event
font_var.trace("w", on_font_change)

# Generate button
generate_button = ttk.Button(frame, text="Generate and Save Image", command=generate_and_display_image)
generate_button.grid(row=6, column=0, columnspan=3, sticky="ew")

# Clear button
clear_button = ttk.Button(frame, text="Clear", command=lambda: text_entry.delete(0, tk.END))
clear_button.grid(row=7, column=0, columnspan=3, sticky="ew")

# Add padding and make widgets expand
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5, sticky="nsew")

# Run the tkinter main loop
root.mainloop()
