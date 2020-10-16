from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
import random


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
    out = os.system("openssl genrsa -out "+names[0]+" 2048")
    if out!=0:
        return json.dumps({"status": "Error"})
    while True:
        if os.path.exists(names[0]):
            break
    with open(names[0], 'r') as f:
        private_key = f.read()
    out = os.system("openssl rsa -in "+names[0]+" -pubout -out "+names[1])
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
    filename = 'random.txt' 
    hash_type="-sha256"
    name = str(random.randint(rand_beg, rand_end))+".txt"
    command = "openssl dgst -out "+name+" "+hash_type+" "+filename
    os.system(command)
    if out!=0:
        return json.dumps({"status": "Error"})
    while True:
        if os.path.exists(name):
            break
    with open(name, 'r') as f:
        digest = f.read()
    os.remove(name)
    return json.dumps({"status": "Success", "digest": digest})


@app.route('/symmetric-encryption', methods=['POST'])
def symmetricEncryption(filename, hash_type="-sha256"):
    print()


if __name__=="__main__": 
    app.run(debug=True)