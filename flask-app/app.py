from asyncio import wait
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
from roboflow import Roboflow

import os, easyocr
import requests
import json
import io
import cv2
import requests



IMAGE = os.path.join('static', 'image')
IMAGE2 = os.path.join('static', 'result')
OBJECT_TEXT = os.path.join('static', 'object', "testo")
OBJECT_TITLE = os.path.join('static', 'object', "titolo")

app = Flask(__name__)
CORS(app, resources={r"/uploader": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = IMAGE
app.config['RESULT_FOLDER'] = IMAGE2
app.config['OBJECT_TEXT_FOLDER'] = OBJECT_TEXT
app.config['OBJECT_TITLE_FOLDER'] = OBJECT_TITLE

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

@app.route('/extract_image_text')
def extract_image_text():
    filename = os.path.splitext(os.listdir(app.config['UPLOAD_FOLDER'])[0])
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'],filename[0] + filename[1])

    rf = Roboflow(api_key="bB8ECItRBAYsBNPihGMZ")
    workspace = rf.workspace()

    project = workspace.project("newspaper_yolo")
    #project.upload(full_filename)

    version = project.version(3)
    model = version.model
    prediction = model.predict(full_filename)

    dir = app.config['RESULT_FOLDER']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    prediction.save(output_path="static/result/predictions.jpg")

    n_col = 1
    #img = Image.open("static/result/predictions.jpg")
    print(full_filename)
    img_real = Image.open(full_filename)

    dir = app.config['OBJECT_TEXT_FOLDER']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    dir = app.config['OBJECT_TITLE_FOLDER']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    reader = easyocr.Reader(['it'], gpu=True)
    column = []

    for c in prediction:
        if(c["class"] == "titolo" or c["class"] == "testo_col"):
            print(c)
            x = c["x"]
            y = c["y"]
            w = c["width"]
            h = c["height"]

            left = x - (w/2)
            right = x + (w/2)
            top = y - (h/2)
            bottom = y + (h/2)

            box = (left, top, right, bottom)
            print(box)
                
            img2 = img_real.crop(box)

        if(c["class"] == "titolo"):
            name = "static/object/titolo/titolo.jpg"
            img2.save(name)
            title = reader.readtext(name, detail = 0)
            print("Save title")
        elif(c["class"] == "testo_col"):
            name = "static/object/testo/colonna" + str(n_col) + ".jpg"
            img2.save(name)
            column.append((x, reader.readtext(name, detail = 0)))
            print("Column Append")
            n_col += 1

    column.sort(key=lambda tup: tup[0])

    text = ""
    print("Start text: " + text)
    for c in column:
        for i in c[1]:
            text += " " + i 
            print("Start adding text: " + text)
    
    text = text.replace("- ", "")

    title_string = ""
    print("Start title: " + title_string)
    for t in title:
        title_string += " " + t
        print("Start adding title: " + title_string)

    print("End process")

    return render_template("show_text.html", user_image = "static/result/predictions.jpg", user_text = text, user_title = title_string)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
