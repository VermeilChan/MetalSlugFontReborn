from flask import Flask , render_template , request , url_for
from main import ImageGeneration

App = Flask(__name__)

@App.route('/')
def index():
    return render_template('index.html')


@App.route('/' , methods=['POST' , 'GET' , 'PUT' , 'DELETE'])
def form():
    if request.method == "POST":
        request.form['input']


if __name__ == "__main__":
    App.run(debug=1)