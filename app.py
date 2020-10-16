from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import json
import os
import random
import time

# secureIt or crypton


app = Flask(__name__)
app.secret_key = 'any random string'
app.config['UPLOAD_FOLDER'] ='static/media/'
rand_beg = 1
rand_end = 1000000


@app.route('/', methods=['POST','GET'])
def home():
    return render_template("home.html")


@app.route('/gen-keypair', methods=['GET'])
def genKeyPair():
    names = [str(random.randint(rand_beg, rand_end))+".pem", str(random.randint(rand_beg, rand_end))+".pem"]
    command = "openssl genrsa -out "+names[0]+" 2048 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return json.dumps({"status": "Error"})
    while True:
        if os.path.exists(names[0]):
            break
    with open(names[0], 'r') as f:
        private_key = f.read()
    
    command = "openssl rsa -in "+names[0]+" -pubout -out "+names[1]+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return json.dumps({"status": "Error"})
    while True:
        if os.path.exists(names[1]):
            break
    with open(names[1], 'r') as f:
        public_key = f.read()
    os.remove(names[0])
    os.remove(names[1])
    return json.dumps({"status": "Success", "publicKey": public_key, "privateKey": private_key})


@app.route('/hash', methods=['POST'])
def hash():
    print(request.files)
    file_ = request.files['file']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_.filename))
    file_.save(filename)

    hash_type = "-" + request.form["algo"].lstrip("-")
    name = os.path.join(app.config['UPLOAD_FOLDER'], str(random.randint(rand_beg, rand_end))+".txt")

    command = "openssl dgst -out "+name+" "+hash_type+" "+filename+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return json.dumps({"status": "Error"})
    while True:
        if os.path.exists(name):
            break
    with open(name, 'r') as f:
        digest = f.read()
    os.remove(name)
    os.remove(filename)
    return json.dumps({"status": "Success", "digest": digest})


@app.route('/symmetric-encryption', methods=['POST'])
def symmetricEncryption():
    filename = 'h'
    enc_type = "-aes-256-cbc"
    password = "asdfgh"
    name = str(random.randint(rand_beg, rand_end))+".enc"
    command = "openssl enc "+enc_type+" -pass pass:"+password+" -in "+filename+" -out "+name+" 2>/dev/null"
    os.system(command)
    if out!=0:
        return json.dumps({"status": "Error"})
    while True:
        if os.path.exists(name):
            break
    with open(name, 'r') as f:
        encrypted_file = f.read()
    os.remove(name)
    return json.dumps({"status": "Success", "digest": encrypted_file})
    


if __name__=="__main__": 
    app.run(debug=True)