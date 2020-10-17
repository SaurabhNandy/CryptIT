from constants import upload_folder, rand_beg, rand_end
import os 
import random


def hashDigest(filename, hash_type):
    hash_filename = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
  
    command = "openssl dgst -out "+hash_filename+" "+hash_type+" "+filename+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(hash_filename):
            break
    with open(hash_filename, 'r') as f:
        digest = f.read()
        digest = digest.split()[1]

    os.remove(hash_filename)
    os.remove(filename)
    return {"status": "Success", "algo": hash_type.lstrip("-").upper(), "data": digest, "ext": ".txt"}


def symmetricEncrypt(filename, enc_type, password):
    enc_name = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".enc")

    command = "openssl enc "+enc_type+" -pass pass:"+password+" -in "+filename+" -out "+enc_name+" -base64 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(enc_name):
            break
    with open(enc_name, 'r') as f:
        encrypted_file = f.read()

    os.remove(enc_name)
    os.remove(filename)
    return {"status": "Success", "algo": enc_type.lstrip("-").upper(), "data": encrypted_file, "ext": ".enc"}


def symmetricDecrypt(filename, enc_type, password, op_ext=".png"):
    dec_name = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+op_ext)

    command = "openssl enc "+enc_type+" -pass pass:"+password+" -in "+filename+" -out "+dec_name+" -base64 -d 2>/dev/null"
    print(command)
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(dec_name):
            break
    with open(dec_name, 'r') as f:
        decrypted_file = f.read()
    print('aaaaaaaaaaa')

    os.remove(dec_name)
    os.remove(filename)
    return {"status": "Success", "algo": dec_name.lstrip("-").upper(), "data": decrypted_file, "ext": op_ext}
    