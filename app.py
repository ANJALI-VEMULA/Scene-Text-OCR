from unittest import result
from flask import Flask, flash, request, redirect, url_for, render_template
import googletrans
from googletrans import Translator
from gtts import gTTS
import base64
import os
import cv2
import numpy as np
import glob
import secrets
from layout import LayoutAPI
from ocr import OCRAPI
from PIL import Image
import shutil
from functools import reduce
from flask_sslify import SSLify
import ssl




Lang = {
    'english': 'en',
	'hindi': 'hi',
	'marathi': 'mr',
	'tamil': 'ta',
	'telugu': 'te',
	'kannada': 'kn',
	'gujarati': 'gu',
	'punjabi': 'pa',
	'bengali': 'bn',
	'malayalam': 'ml',
	'assamese': 'asa',
	'manipuri': 'mni',
    'oriya': 'ori',
	'urdu': 'ur',
}

app = Flask(__name__)
app.secret_key = "abhahjsncjhn"
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert.pem', 'key.pem')


app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['AUDIO_FILE_UPLOAD'] = 'static/audio/'
app.config['LANGUAGE'] = 'LANGUAGE'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == "POST":
        if 'image' not in request.files:
            flash('No file found')
            return redirect(request.url)
    
        file = request.files['image']
        filename = file.filename
    
        if filename == '':
            flash('No image selected')
            return redirect(request.url)
    
        if file:
            f = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            afilename = processing(f)
           
            return render_template("forms.html",afilename = afilename ,fname = filename)
            
    else:
        return render_template("forms.html")

@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.form['image']
    nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    filen = secrets.token_hex(10)+".jpg"
    f = 'static/uploads/'+filen
    cv2.imwrite(f, img)
    afilename = processing(f)
    return render_template('captured_image.html',filename = filen,afilename = afilename)

def processing(f):
    x=[]
    y=[]
    w=[]
    h=[]
    res={}
    result = ''
    
    b = LayoutAPI.fire(f)
    for i in range(len(b[0]['regions'])):
        x.append(b[0]['regions'][i]['bounding_box']['x'])
        y.append(b[0]['regions'][i]['bounding_box']['y'])
        w.append(b[0]['regions'][i]['bounding_box']['w'])
        h.append(b[0]['regions'][i]['bounding_box']['h'])
    print(x,y,w,h)

    im = Image.open(f)
    for i in range(len(x)):
        im1 = im.crop((x[i],y[i],x[i]+w[i],y[i]+h[i]))
        p = str(i)+'.jpg'
        im1.save(os.path.join(app.config['LANGUAGE'],p))
    li = request.form['langinput']
    modality = request.form['modality']
    la = OCRAPI.fire(app.config['LANGUAGE'],li,modality)
    
    for i in la.values():
        result = result + i

    print(result)
    flash('Image uploaded successfully')
    translator = Translator()
    lo = request.form['langoutput']
    print(li+"  "+lo+"  "+modality)
    textt =translator.translate(result, dest=lo)
    print(textt.text)
    tts = gTTS(text= textt.text, lang=lo)
    afilename = secrets.token_hex(10)+".mp3"
    file_location = os.path.join(app.config['AUDIO_FILE_UPLOAD'], afilename)
    tts.save(file_location)

    files = glob.glob(app.config['LANGUAGE']+'/*.jpg')
    for f in files:
        os.remove(f)
    return afilename


if __name__ == "__main__":
    app.run(ssl_context=context)