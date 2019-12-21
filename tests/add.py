import sys

sys.path.append("./../objects")
sys.path.append("./../config")

import config
import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((config.host,config.port))


example = {
    "action": "add",
    "service_name": "My Simple Service",
    "name": "test Service",
    "description":"This is a simple test service!",
    "github_rep": "https://github.com/Callibrator/test_for_elsa.git",
    "github_username": "example_username", # Not Email!!!! Just username
    "github_password": "example_password",
    "install_file": "install.bat",
    "execute_file": "execute.bat",
    "startup":"true"

}

exampleStr = json.dumps(example)
exampleLen = len(exampleStr)

s.send(str(exampleLen).encode())

ret = s.recv(2048).decode()
print(ret)
s.send(exampleStr.encode())
retLen = int(s.recv(2048).decode())
s.send(b"ok")
ret = s.recv(retLen)

print("------------")
print(ret.decode())
