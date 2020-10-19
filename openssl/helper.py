from constants import static_url_path, upload_folder, conf_folder, rand_beg, rand_end
import os
import random
import json



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
    
    command = "openssl rsa -in "+private_key_file+" -pubout -out "+public_key_file+" 2>/dev/null"
    out = os.system(command)
    if out!=0:
        return {"status": "Error"}
    while True:
        if os.path.exists(public_key_file):
            break

    return {"status": "Success", "publicKey_file": public_key_file, "privateKey_file": private_key_file}


def generateConf(req_data):
    conf_file = os.path.join(conf_folder, str(random.randint(rand_beg, rand_end))+".cnf")
    with open("."+os.path.join(static_url_path, "certconf.json"), "r") as f:
        configs = json.loads(f.read())

    conf_data = [configs["pre"]]
    add_data = configs["data"]
    for key in add_data:
        temp = add_data[key]["abbrv"] + " = "
        if key in req_data and req_data[key] and req_data[key]!="undefined":
            temp += req_data[key]
        else:
            temp += add_data[key]["default"]
        conf_data.append(temp+"\n")

    conf_data.append(configs["post"])

    if "DNS" in req_data and req_data["DNS"] and req_data["DNS"]!="undefined":
        for i, dns in enumerate(set(req_data["DNS"].split(","))):
            conf_data.append("DNS." + str(i+1) + " = " + dns+"\n")
    else:
        conf_data.append(configs["dns"]["default"])
    with open(conf_file, 'w') as f:
        f.writelines(conf_data)
    return conf_file