import config
import uuid
import os

def generate_service_id():

    sid = str(uuid.uuid4())
    while True:
        if not os.path.exists(config.services_folder + os.sep + sid):
            break
        sid = str(uuid.uuid4())

    return sid
