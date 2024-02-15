from flask import Flask, render_template, request, redirect, url_for
from main import generate_image, generate_filename, get_font_paths

App = Flask(__name__)

@App.route('/')
def index():
    return render_template('index.html')

@App.route('/support')
def supported():
    return render_template('supported.html')

@App.route('/examples')
def examples():
    return render_template('examples.html')

@App.route('/', methods=['POST'])
def form():
    if request.method == "POST":
        try:
            text = request.form['text']
            font = int(request.form['font'])
            color = request.form['color']

            text = text.upper() if font == 5 else text

            font_paths = get_font_paths(font, color)

            filename = generate_filename()
            image_url, _ = generate_image(text, filename, font_paths)

            return redirect(url_for('result', output=image_url))

        except FileNotFoundError as error:
            return render_template('index.html', error=f"Error: {error}", error_type='FileNotFoundError')

        except Exception as error:
            return render_template('index.html', error=f"Error: {error}")

    return render_template('index.html', error="POST METHOD NOT AVAILABLE")

@App.route('/result')
def result():
    output = request.args.get('output')
    return render_template('result.html', output=output)

if __name__ == "__main__":
    App.run()
