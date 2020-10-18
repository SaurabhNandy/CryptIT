from constants import upload_folder, rand_beg, rand_end
import os 
import random
import base64


def hashDigest(filename, hash_type):
    hash_filename = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
  
    command = "openssl dgst -out "+hash_filename+" "+hash_type+" "+filename+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(hash_filename):
            break
    # with open(hash_filename, 'r') as f:
    #     digest = f.read()
    #     digest = digest.split()[1]
    # os.remove(hash_filename)

    os.remove(filename)
    return {"status": "Success", "algo": hash_type.lstrip("-").upper(), "ext": ".txt", "file_url": hash_filename}


def symmetricEncrypt(filename, enc_type, password):
    enc_name = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".enc")

    command = "openssl enc "+enc_type+" -pass pass:"+password+" -in "+filename+" -out "+enc_name+" -base64 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(enc_name):
            break
    # with open(enc_name, 'r') as f:
    #     encrypted_file = f.read()
    # os.remove(enc_name)

    os.remove(filename)
    return {"status": "Success", "algo": enc_type.lstrip("-").upper(), "ext": ".enc", "file_url": enc_name}


def symmetricDecrypt(filename, enc_type, password, op_ext=".png"):
    dec_name = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+op_ext)

    command = "openssl enc "+enc_type+" -pass pass:"+password+" -in "+filename+" -out "+dec_name+" -base64 -d 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(dec_name):
            break
    # with open(dec_name, 'rb') as f:
    #     decrypted_file = str(base64.b64encode(f.read()))
    # os.remove(dec_name)

    os.remove(filename)
    return {"status": "Success", "algo": dec_name.lstrip("-").upper(), "ext": op_ext, "file_url": dec_name}
    

def digitalSign(filename, pvt_key_file, hash_type='-sha256'):
    hash_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    signature_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    
    command = "openssl dgst "+hash_type+" -out "+hash_file+" "+filename
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(hash_file):
            break
    
    command = "openssl rsautl -sign -inkey "+pvt_key_file+" -keyform PEM -in "+hash_file+" -out "+signature_file
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(signature_file):
            break
    try:
        with open(signature_file, 'rb') as f:
            temp = base64.b64encode(f.read())
        with open(signature_file, 'wb') as f:
            f.write(temp)
    except Exception as e:
        return {"status": "Error "+str(e)}
    
    os.remove(hash_file)
    return {"status": "Success", "algo": "RSA "+hash_type.lstrip("-").upper(), "ext": ".txt", "file_url": signature_file}


def verifyDigitalSign(filename, pub_key_file, signature_file, hash_type='-sha256'):
    old_hash_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    new_hash_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    output_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt") 

    command = "openssl dgst "+hash_type+" -out "+old_hash_file+" "+filename
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(old_hash_file):
            break
    try:
        with open(signature_file, 'r') as f:
            temp = base64.b64decode(f.read())
        with open(signature_file, 'wb') as f:
            f.write(temp)
    except Exception as e:
        return {"status": "Error "+str(e)}
    command = "openssl rsautl -verify -inkey "+pub_key_file+" -pubin -keyform PEM -in "+signature_file+" -out "+new_hash_file
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(new_hash_file):
            break

    with open(old_hash_file, 'r') as f:
        old_hash = str(f.read().split()[1])
    with open(new_hash_file, 'r') as f:
        new_hash = str(f.read().split()[1])
    
    os.remove(old_hash_file)
    os.remove(new_hash_file)
    with open(output_file, 'w') as f:
        if old_hash==new_hash:
            f.write("Signature Verified.")
        else:
            f.write("Verification failure.")
    return {"status": "Success", "algo": "RSA "+hash_type.lstrip("-").upper(), "ext": ".txt", "file_url": output_file}
    




def sslCertificate():
    print()