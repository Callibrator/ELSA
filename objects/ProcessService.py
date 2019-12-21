# This is a a Service Object, it runs as container to executing the process plus it keeps logs and other important data

import threading
import subprocess
import os
import psutil
import time
import traceback

import config

class ProcessService(threading.Thread):

    def __init__(self,service_dict):
        super(ProcessService, self).__init__()
        self.service_dict = service_dict
        self.isRunning = False
        self.isTerminated = False
        self.service = None
        self.out_log = ""
        self.error_log = ""
        self.isTerminatedByUser = False



    def run(self):

        self.isRunning = True
        exec_path = self.service_dict["local_dir"] + os.sep + self.service_dict["execute_file"]

        new_env = os.environ.copy()
        new_env["PATH"] += ":\""+self.service_dict["local_dir"]+"\""

        try:
            self.service = subprocess.Popen(exec_path, cwd=self.service_dict["local_dir"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=new_env)

        except:
            tb = traceback.format_exc()
            fl = open(self.service_dict["local_dir"]+os.sep+"elsa_error_logs.txt", "w")
            fl.write(str(tb))
            fl.close()




        # fl = open("out1","w")
        # fl.write(self.service.stdout.read())
        # fl.close()
        #
        #
        # fl = open("err1","w")
        # fl.write(self.service.stderr.read())
        # fl.close()

        self.output_thread = threading.Thread(target=self.get_output_async)
        self.errors_thread = threading.Thread(target=self.get_errors_async)

        self.output_thread.start()
        self.errors_thread.start()

        self.service.wait()

        self.isRunning = False
        self.isTerminated = True

        self.output_thread.join()
        self.errors_thread.join()



    def nuke_service(self):
        self.isTerminatedByUser = True
        parent_pid = self.service.pid
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()

    def get_output(self):
        return self.out_log

    def get_output_async(self):
        while not self.isTerminated:
            time.sleep(1)
            if self.service != None:
                output = self.service.stdout.read(config.max_output_log)
                if output != None:
                    output = output.decode().strip()
                else:
                    output = ""

                if len(output) > config.max_output_log:
                    self.out_log = output[-config.max_output_log:]
                else:
                    self.out_log += output

                if len(self.out_log) > config.max_output_log:
                    self.out_log = self.out_log[-config.max_output_log:]

                return self.out_log
            else:
                return self.out_log

    def get_errors(self):
        return self.error_log

    def get_errors_async(self):
        while not self.isTerminated:
            time.sleep(1)
            if self.service != None:
                output = self.service.stderr.read(config.max_error_log)
                if output != None:
                    output = output.decode().strip()
                else:
                    output = ""

                if len(output) > config.max_error_log:
                    self.error_log = output[-config.max_error_log:]
                else:
                    self.error_log += output

                if len(self.out_log) > config.max_error_log:
                    self.error_log = self.error_log[-config.max_error_log:]

                return self.error_log
            else:
                return self.error_log



