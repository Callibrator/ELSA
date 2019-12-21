#This is the client class, it is responsible for containing all functions required for the communication of client/server

import threading
import json




class Client(threading.Thread):

    def __init__(self, Socket, Address, serviceManager, services):
        super(Client, self).__init__()
        self.socket = Socket
        self.address = Address
        self.serviceManager = serviceManager
        self.services = services

    def run(self):
        self.request_handler()

    def request_handler(self):
        client = self.socket
        data = client.recv(1024)
        buffer_length = int(data.decode())

        client.sendall(b"ok")

        data = json.loads(client.recv(buffer_length).decode())

        if "action" in data:
            if data["action"] == "add":
                if ("service_name" in data ) and ("name" in data ) and ("description" in data ) and ("github_rep" in data ) and ("install_file" in data ) and ("execute_file" in data ) and ("startup" in data ):

                    if "github_username" in data:
                        username = data["github_username"]
                    else:
                        username = None

                    if "github_password" in data:
                        password = data["github_password"]
                    else:
                        password = None



                    if self.serviceManager.isBusy:
                        ret = {"message":"It is install a software currently, try again later"}
                    else:
                        ret = self.serviceManager.add_service(self.services,  data, username, password)
                else:
                    ret = {"message":"missing parameters"}

            elif data["action"] == "stop":
                if "service_id" in data:
                    sid = data["service_id"]
                    ret = self.serviceManager.stop_service(self.services, sid)

            elif data["action"] == "start":
                if "service_id" in data:
                    sid = data["service_id"]
                    ret = self.serviceManager.start_service(self.services, sid)

            elif data["action"] == "status":
                    ret = self.serviceManager.get_services_status(self.services)

            elif data["action"] == "restart":
                if "service_id" in data:
                    sid = data["service_id"]
                    ret = self.serviceManager.restart_service(self.services, sid)

            elif data["action"] == "modify":
                if "service_id" in data:
                    sid = data["service_id"]

                    if "name" in data:
                        name = data["name"]
                    else:
                        name = None

                    if "description" in data:
                        description = data["description"]
                    else:
                        description = None

                    if "startup" in data:
                        startup = data["startup"]
                    else:
                        startup = None

                    ret = self.serviceManager.modify_service(self.services, sid, name, description, startup)

            elif data["action"] == "remove":
                if "service_id" in data:
                    sid = data["service_id"]
                    ret = self.serviceManager.remove_service(self.services, sid)

            else:
                ret = {"message": "Unknown Command"}
        else:
            ret = {
                "message": "Error, Action Not Specified"
            }



        ret = json.dumps(ret)

        client.sendall(str(len(ret)).encode())
        r = client.recv(2048)
        if r.decode() == "ok":
            client.sendall(ret.encode())

        client.close()

