import sys

sys.path.append("./../objects")
sys.path.append("./../config")

import config
import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((config.host,config.port))

service_id = "7906af27-82fe-42db-aefb-5c9f16be4539"

example = {
    "action": "remove",
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
