from flask import Flask, render_template, request

from main import ImageGeneration, CharacterNotFound

App = Flask(__name__)

@App.route('/')
def index():
    return render_template('index.html', state=False)

@App.route('/support')
def supported():
    return render_template('supported.html')

@App.route('/examples')
def examples():
    return render_template('examples.html')

@App.route('/', methods=['POST', 'GET', 'PUT', 'DELETE'])
def form():
    if request.method == "POST":
        x = request.form['text']
        y = int(request.form['font'])
        z = request.form['color']

        image = ImageGeneration(x, y, z)

        try:
            image_url = image.generate_image()
            return render_template('index.html', output=image_url.replace('src', ''), state=image.state)

        except CharacterNotFound as error:
            return render_template('index.html', error=f"Error: {error}")

        except Exception as error:
            return render_template('index.html', error=f"Unexpected error: {error}")

    else:
        return render_template('index.html', error="POST METHOD NOT AVAILABLE")

if __name__ == "__main__":
    App.run()
