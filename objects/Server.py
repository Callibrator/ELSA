#This is the server class, it contains all the functions and binds almost everything together
import socket
import json

import config
from ServiceManager import ServiceManager
from Client import Client

import threading


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((config.host,config.port))
        self.socket.listen(config.listen_queue)
        self.services = []

        self.serviceManager = ServiceManager()
        self.serviceManager.restore_services(self.services)

    def start(self):
        while True:
            client, address = self.socket.accept()
            c = Client(client, address, self.serviceManager, self.services)
            c.start()












