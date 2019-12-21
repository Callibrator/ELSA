import sys

sys.path.append("./../objects")
sys.path.append("./../config")

import config
import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((config.host,config.port))


example = {
    "action": "status",

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

print("--Pretier--")

for s in json.loads(ret.decode()):
    print("---------------")
    print("id:", s["id"])
    print("name:", s["name"])
    print("description:", s["description"])
    print("local_dir:", s["local_dir"])
    print("install_script:", s["install_script"])
    print("execute_file:", s["execute_file"])
    print("install_status:", s["install_status"])
    print("install_log:", s["install_log"])
    print("install_error_log:", s["install_error_log"])
    print("startup:", s["startup"])
    print("output_log:", s["output_log"])
    print("error_log:", s["error_log"])
    print("isRunning:", s["isRunning"])
    print("isTerminatedByUser:", s["isTerminatedByUser"])
    print("isTerminated:", s["isTerminated"])
