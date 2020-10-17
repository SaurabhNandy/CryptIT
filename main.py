from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import json
import os
import random

from openssl.helper import KeyPair
from openssl.functions import *
from constants import *

# cryptIt or secureIt or crypton


app = Flask(__name__, static_url_path = static_url_path)
app.secret_key = secret_key
app.config['UPLOAD_FOLDER'] = upload_folder


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@app.route('/gen-keypair', methods=['GET'])
def getKeyPair():
    return_data = KeyPair()
    return json.dumps(return_data)


@app.route('/hash', methods=['POST'])
def getHash():
    file_ = request.files['file']
    filename = os.path.join(upload_folder, secure_filename(file_.filename))
    file_.save(filename)
    hash_type = "-" + request.form["algo"].strip().lstrip("-")

    return_hash = hashDigest(filename, hash_type)
    return json.dumps(return_hash)


@app.route('/symmetric-encryption', methods=['POST'])
def symmetricEncryption():
    file_ = request.files['file']
    filename = os.path.join(upload_folder, secure_filename(file_.filename))
    file_.save(filename)
    enc_type = "-" + request.form["algo"].strip().lstrip("-")
    password = request.form["password"].strip()
    typ = request.form["type"].strip()
    
    if typ=="enc":
        encoded_data = symmetricEncrypt(filename, enc_type, password)
        return json.dumps(encoded_data)
    else:
        decoded_data = symmetricDecrypt(filename, enc_type, password)
        return json.dumps(decoded_data)
    


if __name__=="__main__": 
    app.run(debug=True)