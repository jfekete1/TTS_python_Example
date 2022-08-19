import string
from flask import Flask, request, send_file
from datetime import datetime
import time
from flask_cors import CORS
import requests
import json
import random
import pyttsx3
import sys, base64
import os
from waitress import serve

app = Flask(__name__)
CORS(app)

def mp3_string():
    f = open('speech_server.mp3', 'rb')
    b = base64.b64encode(f.read())
    b_str = b.decode()
    f.close()
    return b_str

def create_wav(txt):
    parancs = '/usr/bin/espeak -w speech_server.mp3 -v hu+f2' + " " + txt
    os.system(parancs)

def create_mp3(txt):
    engine = pyttsx3.init()
    engine.setProperty('voice','hungarian+f2')
    engine.save_to_file(txt, "speech_server.mp3")
    engine.runAndWait()
    engine.stop()

@app.route('/speech', methods=['GET'])
def get_speech():
    txt = request.args.get('speech')
    print("Ezt a stringet kaptam: ")
    print(txt)
    time.sleep(1)
    create_wav(txt)
    b_str = mp3_string()
    return json.dumps({'speech': b_str, 'file': 'http://127.0.0.1:8080/file' })

@app.route('/file', methods=['GET'])
def get_file():
    return send_file("speech_server.mp3", as_attachment=True)

def main_prod():
    serve(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main_prod()
