#This class handles the services and everything related to them! There should only be one instance of this class, like a static one

import config
import os
import git
import subprocess
import time
import shutil
import json
import stat


from generate_service_id import generate_service_id
from ProcessService import ProcessService

class ServiceManager:
    def __init__(self):
        self.isBusy = False

    def restore_services(self, services):
        if os.path.isfile("services_db.json"):
            fl = open("services_db.json","r")

            services_db = json.loads(fl.read())

            fl.close()

            for s in services_db:
                services.append(s)
                if ("id" in s) and ("startup" in s) and ("install_status" in s):
                    if s["startup"] == True and s["install_status"] == "success":
                        self.start_service(services_db, s["id"])




    #Installs a service to the system & adds it to the services pool. Then it returns a json object describing the service
    def __update_services_db(self, services):
        services_db = self.get_services_status(services)

        fl = open("services_db.json","w")
        fl.write(json.dumps(services_db))
        fl.close()


    def add_service(self, services, service,username = None, password = None):
        if self.isBusy:
            return False

        self.isBusy = True
        s = self.__install(service, username, password)
        services.append(s)

        self.__update_services_db(services)

        self.isBusy = False

        return s

    def __install(self, service, username=None, password=None):
        if not os.path.exists(config.services_folder):
            os.mkdir(config.services_folder, 0o777)

        sid = generate_service_id()
        local_dir = config.services_folder + os.sep + sid

        os.makedirs(local_dir)

        rep_uri = service["github_rep"]

        if username != None and password != None:
            if username != "" and password != "":
                rep_uri = "https://"+username+":"+password+"@"+rep_uri[8:]



        repo = git.Repo.clone_from(rep_uri, local_dir)
        rep_dir = repo.working_tree_dir



        #Executing Installation Script
        install_filepath = rep_dir + os.sep + service["install_file"]
        execute_filepath = rep_dir + os.sep + service["execute_file"]

        error_log = ""
        install_log = "Installation Failed!"


        try:

            st = os.stat(install_filepath)
            os.chmod(install_filepath, st.st_mode | stat.S_IEXEC)

            st = os.stat(execute_filepath)
            os.chmod(execute_filepath, st.st_mode | stat.S_IEXEC)

            install_log = subprocess.run(install_filepath, cwd=rep_dir,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            ret_code = install_log.returncode
            error_log = install_log.stderr.decode()
            install_log = install_log.stdout.decode()

        except:
            ret_code = 1
            print("Installation Failed")

        if ret_code == 0:
            install_status = "success"
        else:
            install_status = "failed"

        startup = False

        if "startup" in service:
            if service["startup"] != "false" and service["startup"] != False:
                startup = True

        s = {
            "id": sid,
            "uri": rep_uri,
            "name": service["name"],
            "description": service["description"],
            "startup": startup,
            "local_dir": rep_dir,
            "install_script": service["install_file"],
            "execute_file": service["execute_file"],
            "install_status": install_status,
            "install_log": install_log,
            "install_error_log": error_log,
            "created_at": time.time()
        }

        return s

    def remove_service(self, services, sid):
        if self.isBusy:
            return False

        self.isBusy = True

        service = None
        for s in services:
            if s["id"] == sid:
                service = s
                if "process" in s:
                    if s["process"].isRunning:
                        s["process"].nuke_service()
                        while s["process"].isRunning:
                            pass # wait until terminated!

                        if os.path.isdir(s["local_dir"]):
                            self.change_permissions_recursive(s["local_dir"],0o777)
                            shutil.rmtree(s["local_dir"])

                    else:
                        if os.path.isdir(s["local_dir"]):
                            self.change_permissions_recursive(s["local_dir"],0o777)
                            shutil.rmtree(s["local_dir"])

                else:
                    if os.path.isdir(s["local_dir"]):
                        self.change_permissions_recursive(s["local_dir"],0o777)
                        shutil.rmtree(s["local_dir"])


        self.isBusy = False

        if service != None:
            services.remove(service)
            self.__update_services_db(services)
            return True

        return False


    def stop_service(self, services, sid):
        for s in services:
            if s["id"] == sid:
                if "process" in s:
                    if s["process"].isRunning:
                        s["process"].nuke_service()
                        return True
        return False


    #Starts a service give its id, the service must exists in services file!

    def start_service(self, services, sid):
        for s in services:
            if s["id"] == sid:
                if not "process" in s:
                    s["process"] = ProcessService(s)
                    s["process"].start()
                    return True
                else:
                    if not s["process"].isRunning:
                        s["process"] = ProcessService(s)
                        s["process"].start()
                        return True

        return False

    def restart_service(self, services, sid):
        for s in services:
            if s["id"] == sid:

                if "process" in s:
                    if s["process"].isRunning == True:
                        self.stop_service(services, sid)

                if not "process" in s:
                    self.start_service(services, sid)
                else:
                    while s["process"].isRunning == True:
                        pass #Wait!
                    self.start_service(services,sid)

                return True

        return False

    def get_services_status(self, services):
        available_services = []
        for s in services:
            if "process" in s:
                output    = s["process"].get_output()
                errors    = s["process"].get_errors()
                isRunning = s["process"].isRunning
                isTerminated = s["process"].isTerminated
                isTerminatedByUser = s["process"].isTerminatedByUser
            else:
                output = ""
                errors = ""
                isRunning = False
                isTerminated = False
                isTerminatedByUser = False


            available_services.append({
                "id": s["id"],
                "uri": s["uri"],
                "name": s["name"],
                "description": s["description"],
                "local_dir": s["local_dir"],
                "install_script": s["install_script"],
                "execute_file": s["execute_file"],
                "install_status": s["install_status"],
                "install_log": s["install_log"],
                "install_error_log": s["install_error_log"],
                "startup": s["startup"],
                "output_log": output,
                "error_log": errors,
                "isRunning": isRunning,
                "isTerminatedByUser": isTerminatedByUser,
                "isTerminated": isTerminated
            })

        return available_services

    def modify_service(self, services, sid ,new_name,new_description,new_startup):
        for s in services:
            if s["id"] == sid:
                if new_name != None:
                    s["name"] = new_name

                if new_description != None:
                    s["description"] = new_description

                if new_startup != None:
                    if new_startup != "false" and new_startup != False:
                        s["startup"] = True
                    else:
                        s["startup"] = False

                self.__update_services_db(services)
                return True

        return False


    def change_permissions_recursive(self, path, mode):
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in [os.path.join(root,d) for d in dirs]:
                os.chmod(dir, mode)
            for file in [os.path.join(root, f) for f in files]:
                os.chmod(file, mode)



