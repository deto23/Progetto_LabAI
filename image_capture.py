# Import essential libraries
import requests
import cv2
import numpy as np
import imutils
from PIL import Image 
import pytesseract
  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
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
        cv2.imwrite(filename='saved_img.jpg', img=img)
        print("Processing image...")
        img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
        print("Converting RGB image to grayscale...")
        gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
        print("Converted RGB image to grayscale...")
        print("Resizing image to 28x28 scale...")
        img_ = cv2.resize(gray,(28,28))
        print("Resized...")
        img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
        print("Image saved!")

        break

    elif cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()

        break

