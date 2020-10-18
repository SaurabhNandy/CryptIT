import subprocess, time
import os 
import base64
# out = subprocess.Popen('openssl genrsa -out keypair.pem 2048'.split(), 
#     stdout=subprocess.PIPE, 
#     stderr=subprocess.STDOUT)
# time.sleep(3)
# out = subprocess.Popen('openssl rsa -in keypair.pem -pubout'.split(), 
#     stdout=subprocess.PIPE, 
#     stderr=subprocess.STDOUT)
# stdout,stderr = out.communicate()
# print(stdout, stderr)

# openssl dgst -out abc.txt -sha256 app.py

# openssl enc -aes-256-cbc -pass pass:12345 -in hist.png -out file.enc -base64
# openssl enc -aes-256-cbc -pass pass:12345 -in file.enc -out temp.py -base64 -d

# openssl dgst -sha256 -out abc.txt hist.png
# openssl rsautl -sign -inkey pvt.pem -keyform PEM -in abc.txt -out sign.txt
# openssl rsautl -verify -inkey pub.pem -pubin -keyform PEM -in sign.txt -out oghash.txt

# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

os.system("openssl dgst -sha256 -out abc.txt hist.png")
os.system("openssl rsautl -sign -inkey pvt.pem -keyform PEM -in abc.txt -out sign.txt")
with open("sign.txt", 'rb') as f:
    a = base64.b64encode(f.read())
print(a)
with open("sign1.txt", 'wb') as f:
    f.write(base64.b64decode(a))

os.system("openssl rsautl -verify -inkey pub.pem -pubin -keyform PEM -in sign1.txt -out oghash.txt")



