from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import numpy as np
from PIL import Image
import pytesseract
import os
import easyocr, cv2, time

IMAGE = os.path.join('static', 'image')

app = Flask(__name__)
CORS(app, resources={r"/uploader": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = IMAGE

@app.route("/")
def home():
    o = urlparse(request.base_url)
    print(o.hostname, o.port)
    
    return render_template("home.html")

    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/uploader', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def upload_file():
    dir = app.config['UPLOAD_FOLDER']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify(message="POST request returned") 


@app.route('/show_img')
def show_img():
    filename = os.path.splitext(os.listdir(app.config['UPLOAD_FOLDER'])[0])
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'],filename[0] + filename[1])
    return render_template("show_img.html", user_image = full_filename)

@app.route('/show_text')
def show_text():
    filename = os.path.splitext(os.listdir(app.config['UPLOAD_FOLDER'])[0])
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'],filename[0] + filename[1])

    reader = easyocr.Reader(['it'], gpu=True)
    output = reader.readtext(full_filename, detail = 0)
    text = ""

    for i in output:
        text += i 
    
    print(text)

    return render_template("show_text.html", user_text = text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
