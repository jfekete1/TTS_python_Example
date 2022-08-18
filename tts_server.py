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
    # date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    # filename = "speech_server" + date + ".mp3"
    # engine.save_to_file(txt, filename)
    engine.save_to_file(txt, "speech_server.mp3")
    engine.runAndWait()
    engine.stop()
    # return filename


# @app.route('/speech', methods=['POST'])
# def create_speech():
#     print(request)
#     data = request.get_json()
#     create_mp3(data['speech'])
#     b_str = mp3_string()
#     return json.dumps({'speech': b_str })

@app.route('/speech', methods=['GET'])
def get_speech():
    txt = request.args.get('speech')
    print("Ezt a stringet kaptam: ")
    print(txt)
    # os.system("rm -f speech_server.mp3")
    # filename = create_mp3(txt)
    # create_mp3(txt)
    time.sleep(1)
    create_wav(txt)
    # b_str = mp3_string(filename)
    b_str = mp3_string()
    return json.dumps({'speech': b_str, 'file': 'http://127.0.0.1:8080/file' })
    # return send_file("speech_server.mp3")

@app.route('/file', methods=['GET'])
def get_file():
    # return send_file(filename, as_attachment=True)
    return send_file("speech_server.mp3", as_attachment=True)

def main_prod():
    serve(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # app.run(debug=True)
    main_prod()
