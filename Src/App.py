from flask import Flask , render_template , request , url_for
from main import ImageGeneration

App = Flask(__name__)

@App.route('/')
def index():
    return render_template('index.html' , state="on change")


@App.route('/' , methods=['POST' , 'GET' , 'PUT' , 'DELETE'])
def form():
    if request.method == "POST":

        x = request.form['text']
        y  = request.form['font']
        z = request.form['color']


        image = ImageGeneration(x , y , z)

        image_url:str = image.GenerateImage()

    

        return render_template('index.html' , output=image_url.replace('src' , ''))
    
    else:
        return render_template('index.html' , error="something went wrong")


if __name__ == "__main__":
    App.run(debug=1)