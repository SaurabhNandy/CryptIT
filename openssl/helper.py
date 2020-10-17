from constants import upload_folder, rand_beg, rand_end
import os
import random



def KeyPair():
    private_key_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".pem")
    public_key_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".pem")
    
    command = "openssl genrsa -out "+private_key_file+" 2048 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(private_key_file):
            break
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    
    command = "openssl rsa -in "+private_key_file+" -pubout -out "+public_key_file+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(public_key_file):
            break
    with open(public_key_file, 'r') as f:
        public_key = f.read()

    os.remove(private_key_file)
    os.remove(public_key_file)
    return {"status": "Success", "publicKey": public_key, "privateKey": private_key}