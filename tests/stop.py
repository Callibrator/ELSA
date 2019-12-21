import sys

sys.path.append("./../objects")
sys.path.append("./../config")

import config
import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((config.host,config.port))

service_id = "ea594ab7-ebfd-43c6-8f9e-c096ecd083ba"

example = {
    "action": "stop",
    "service_id": service_id

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
