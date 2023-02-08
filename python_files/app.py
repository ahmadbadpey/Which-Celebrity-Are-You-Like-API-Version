import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from prediction_blueprint import prediction_blueprint

# from time import sleep

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(prediction_blueprint)


@app.route('/')
def index():  # put application's code here
    return render_template('./index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    fn = secure_filename(file.filename)
    # sleep(3)
    file.save(os.path.join('../uploads', fn))
    return {
        "success": True,
        "message": fn
    }


if __name__ == '__main__':
    app.run()
