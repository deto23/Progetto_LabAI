from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image
from roboflow import Roboflow

import os, easyocr
import requests
import json
import io
import cv2
import requests



IMAGE = os.path.join('static', 'image')
IMAGE2 = os.path.join('static', 'result')

app = Flask(__name__)
CORS(app, resources={r"/uploader": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = IMAGE
app.config['RESULT_FOLDER'] = IMAGE2

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

    version = project.version(1)
    model = version.model
    prediction = model.predict(full_filename)

    dir = app.config['RESULT_FOLDER']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    prediction.save(output_path="static/result/predictions.jpg")

    num_col = 0
    for c in prediction:
        if(c["class"] == "testo_col"):
            num_col+=1
            '''
            with Image.open("static/result/predictions.jpg") as im:
                x = int(c["x"])
                y = int(c["y"])
                w = int(c["width"])
                h = int(c["height"])
                im.crop((x, y, w, h-y)).save("titolo.jpg")
            '''
                


    '''
    img = Image.open(full_filename)
    rgb_img = img.convert('RGB')
        
    dir = app.config['UPLOAD_FOLDER']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    rgb_img.save('static/image/image.jpg')

    img = cv2.imread('static/image/image.jpg')
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)

    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")

    m = MultipartEncoder(fields={'file': ('static/image/image.jpg', buffered.getvalue(), "image/jpeg")})

    response = requests.post("https://detect.roboflow.com/newspaper_yolo/1?api_key=bB8ECItRBAYsBNPihGMZ", data=m, headers={'Content-Type': m.content_type})
    '''

    reader = easyocr.Reader(['it'], gpu=True)
    output = reader.readtext(full_filename, detail = 0)
    text = ""

    for i in output:
        text += i 
    
    print(text)

    return render_template("show_text.html", user_image = "static/result/predictions.jpg", user_text = text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
