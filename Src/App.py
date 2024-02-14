from flask import Flask, render_template, request, redirect, url_for
from main import generate_image

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

@App.route('/', methods=['POST'])
def form():
    if request.method == "POST":
        try:
            text = request.form['text']
            font = int(request.form['font'])
            color = request.form['color']

            text = text.upper() if font == 5 else text

            image_url = generate_image(text, font, color)

            return redirect(url_for('result', output=image_url.replace('src', ''), state=True))

        except FileNotFoundError as error:
            return render_template('index.html', error=f"Error: {error}", error_type='FileNotFoundError')

        except Exception as error:
            return render_template('index.html', error=f"Error: {error}")

    return render_template('index.html', error="POST METHOD NOT AVAILABLE")

@App.route('/result')
def result():
    output = request.args.get('output')
    state = request.args.get('state')
    return render_template('result.html', output=output, state=state)

if __name__ == "__main__":
    App.run()
