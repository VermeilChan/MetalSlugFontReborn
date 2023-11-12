# Import necessary libraries
import sys

from flask import Flask, render_template, request

# Disable writing bytecode to avoid clutter
sys.dont_write_bytecode = True

# Prevent the generation of .pyc (Python bytecode) files
from main import ImageGeneration

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def index():
    # Render the index.html template with a default state
    return render_template('index.html', state="on change")

# Define a route for form submission with support for multiple HTTP methods
@app.route('/', methods=['POST', 'GET', 'PUT', 'DELETE'])
def form():
    if request.method == "POST":
        # Handle form submission when the method is POST

        # Get form data (user input, font, and color)
        x = request.form['text']
        y = request.form['font']
        z = request.form['color']

        # Create an instance of the ImageGeneration class
        image = ImageGeneration(x, y, z)
        
        # Generate the image and get the image URL
        image_url: str = image.GenerateImage()

        # Render the index.html template with the generated image URL
        return render_template('index.html', output=image_url.replace('src', ''))
    else:
        # Render the index.html template with an error message if the method is not POST
        return render_template('index.html', error="something went wrong")

# Run the Flask application if the script is executed directly
if __name__ == "__main__":
    app.run()
