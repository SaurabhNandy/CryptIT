from flask import Flask, render_template, request, url_for
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
def genHash():
    file_ = request.files['file']
    filename = os.path.join(upload_folder, secure_filename(file_.filename))
    file_.save(filename)
    hash_type = "-" + request.form["algo"].strip().lstrip("-")

    return_hash = hashDigest(filename, hash_type)
    return json.dumps(return_hash)


@app.route('/symmetric-encryption', methods=['POST'])
def genSymmetricEncryption():
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


@app.route('/digital-signature', methods=['POST'])
def genDigitalSignature():
    file_ = request.files['file']
    filename = os.path.join(upload_folder, secure_filename(file_.filename))
    file_.save(filename)
    
    hash_type = "-" + request.form["hash_algo"].strip().lstrip("-")
    typ = request.form["type"].strip()
    
    if typ=="sign":
        pvt_key = request.form["pvt_key"].strip()
        pvt_key_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".pem")
        with open(pvt_key_file, 'w') as f:
            f.write(pvt_key)

        signed_data = digitalSign(filename, pvt_key_file, hash_type)
        os.remove(pvt_key_file)
        os.remove(filename)
        return json.dumps(signed_data)
    else:
        pub_key = request.form["pub_key"].strip()
        pub_key_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".pem")
        with open(pub_key_file, 'w') as f:
            f.write(pub_key)

        digital_sign = request.form["digital_sign"].strip()
        digital_sign_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
        with open(digital_sign_file, 'w') as f:
            f.write(digital_sign)

        verified_data = verifyDigitalSign(filename, pub_key_file, digital_sign_file, hash_type)
        os.remove(pub_key_file)
        os.remove(digital_sign_file)
        os.remove(filename)
        return json.dumps(verified_data)
    

@app.route('/ssl-certificate', methods=['POST'])
def genSSLCertificate():
    algo = "rsa:2048"
    hash_algo = "-sha256"
    days = request.form["days"]
    if not (days and days.isdigit()):
        days = "365"
    certificate_data = sslCertificate(request.form, days, algo, hash_algo)
    return json.dumps(certificate_data)


@app.route('/delete', methods=['POST'])
def deleteData():
    files = request.form["data"].split(",")
    for f in files:
        if f.startswith(upload_folder) and os.path.isfile(f) and os.path.exists(f):
            os.remove(f)
    return {"status": "Success"}

if __name__=="__main__": 
    app.run(debug=True)