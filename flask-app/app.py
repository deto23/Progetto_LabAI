from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import socket
from urllib.parse import urlparse

import requests
import cv2
import numpy as np
import imutils
from PIL import Image
import pytesseract
import os

IMAGE = os.path.join('static', 'image')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE

@app.route("/")
def home():
    o = urlparse(request.base_url)
    print(o.hostname, o.port)
    
    return render_template("home.html")

 
@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/uploader')
def upload_file():
    url = "http://192.168.1.164:8080/shot.jpg"
  
    # While loop to continuously fetching data from the Url
    while True:
        img_resp = requests.get(url)
        
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=1000, height=1800)
        cv2.imshow("Android_cam", img)
    
        # Press Esc key to exit
        if cv2.waitKey(1) == ord('s'):
            cv2.imwrite(filename='static/image/saved_img.jpg', img=img)
            print("Image saved!")

            break
    return render_template('upload.html')

@app.route('/show_img')
def show_img():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_img.jpg')
    return render_template("show_img.html", user_image = full_filename)

@app.route('/show_text')
def show_text():
    filename = 'static/image/saved_img.jpg'

    img1 = np.array(Image.open(filename))

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(img1)
    return render_template("show_text.html", user_text = text)


if __name__ == "__main__":
    app.run(debug=True)
