from constants import upload_folder, rand_beg, rand_end
from .helper import generateConf
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
    #     digest = f.read().split()
    # with open(hash_filename, 'w') as f:
    #     f.write(digest[1]) 
        
    # os.remove(hash_filename)
    os.remove(filename)
    return {
        "status": "Success", 
        "algo": hash_type.lstrip("-").upper(), 
        "result": [
            {
                "description": "Hashed file" +" ("+ filename.split('/')[-1] + ")",
                "ext": ".txt", 
                "file_url": hash_filename
            }
        ]
    }


def verifyhashDigest(filename, verification_digest, hash_type):
    hash_filename = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    output_filename = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
  
    command = "openssl dgst -out "+hash_filename+" "+hash_type+" "+filename+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(hash_filename):
            break
    with open(hash_filename, 'r') as f:
        digest = f.read().split()[1]
    
    with open(output_filename, 'w') as f:
        verification_digest = verification_digest.split()
        if len(verification_digest)==1 and verification_digest[0]==digest:
            f.write("Hash Verified.")
        elif len(verification_digest)==2 and verification_digest[1]==digest:
            f.write("Hash Verified.")
        else:
            f.write("Hash Invalid.")
    
    os.remove(hash_filename)
    return {
        "status": "Success", 
        "algo": hash_type.lstrip("-").upper(), 
        "result": [
            {
                "description": "Hash verification" + " (" + filename.split('/')[-1] + ")",
                "ext": ".txt", 
                "file_url": output_filename
            }
        ] 
    }


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
    return {
        "status": "Success", 
        "algo": enc_type.lstrip("-").upper(), 
        "result": [
            {
                "description": "Encrypted file" + " (" + filename.split('/')[-1] + ")",
                "ext": ".enc", 
                "file_url": enc_name
            }
        ] 
    }


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
    return {
        "status": "Success", 
        "algo": enc_type.lstrip("-").upper(), 
        "result": [
            {
                "description": "Decrypted file" + " (" + filename.split('/')[-1] + ")",
                "ext": op_ext, 
                "file_url": dec_name
            }
        ] 
    }
    

def digitalSign(filename, pvt_key_file, hash_type='-sha256'):
    hash_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    signature_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    
    command = "openssl dgst "+hash_type+" -out "+hash_file+" "+filename + " 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(hash_file):
            break
    
    command = "openssl rsautl -sign -inkey "+pvt_key_file+" -keyform PEM -in "+hash_file+" -out "+signature_file + " 2>/dev/null"
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
    return {
        "status": "Success", 
        "algo": "RSA "+hash_type.lstrip("-").upper(), 
        "result": [
            {
                "description": "Signed file" + " (" + filename.split('/')[-1] + ") base64 encoded",
                "ext": ".txt", 
                "file_url": signature_file
            }
        ]
    }


def verifyDigitalSign(filename, pub_key_file, signature_file, hash_type='-sha256'):
    old_hash_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    new_hash_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt")
    output_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".txt") 

    command = "openssl dgst "+hash_type+" -out "+old_hash_file+" "+filename + " 2>/dev/null"
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
    command = "openssl rsautl -verify -inkey "+pub_key_file+" -pubin -keyform PEM -in "+signature_file+" -out "+new_hash_file + " 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error", "info": "Bad decrypt"}
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
    return {
        "status": "Success", 
        "algo": "RSA "+hash_type.lstrip("-").upper(), 
        "result": [
            {
                "description": "Sign Verification" + " (" + filename.split('/')[-1] + ")",
                "ext": ".txt", 
                "file_url": output_file
            }
        ]
    }
    

def sslCertificate(request_data, days="365", algo="rsa:2048", hash_algo="-sha256"):
    config_file = generateConf(request_data)
    private_key_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".pem")
    public_key_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".pem")
    ssl_certificate_file = os.path.join(upload_folder, str(random.randint(rand_beg, rand_end))+".cert.pem")
    
    command = "openssl req -config "+config_file+" -new -x509 "+hash_algo+" -newkey "+algo+" -nodes -keyout "+private_key_file+" -days "+days+" -out "+ssl_certificate_file+ " 2>/dev/null"
    out = os.system(command)
    os.remove(config_file)
    if out!=0:
        return {"status": "Error", "info": "Unable to generate cerificate"}
    while True:
        if os.path.exists(private_key_file) and os.path.exists(ssl_certificate_file):
            break
    
    command = "openssl rsa -in "+private_key_file+" -pubout -out "+public_key_file+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(public_key_file):
            break
    return {
        "status": "Success", 
        "algo": algo.upper()+" "+hash_algo.lstrip("-").upper(), 
        "result": [
            {
                "description": "SSL Cetificate" + " (Valid for " + days + " days)",
                "ext": ".cert.pem", 
                "file_url": ssl_certificate_file
            },
            {
                "description": "Private Key for SSL certificate",
                "ext": ".pem", 
                "file_url": private_key_file
            },
            {
                "description": "Public Key for SSL certificate",
                "ext": ".pem", 
                "file_url": public_key_file
            }
        ]
    }