# ELSA

<p align="center">
  <img src="/res/logo.png">
</p>

Easy Leading Service API. It is an API that helps you manager (start,stop,add,remove) services with python. It creates an additional python layer for the services and it does not uses native system ways of creating services. It is simpler!
Right now the possible sources are downloaded from github!

# Linux Automatic Installation

- Just run the following command in your bash

```curl -s https://raw.githubusercontent.com/Callibrator/ELSA/master/install.sh | sudo bash```


# Communication Protocol

- connect to ELSA with tcp/ip sockets
- send ELSA the length of your json data
- wait for ELSA to respond with ok, it it is not ok something is wrong!
- send ELSA your serialized json data
- wait for ELSA to respond to you with the size of the response
- Respond with ok
- Receive the data from ELSA as a serialized json

# Supported Commands

- add: adds a service
- remove: removes a service, if the service is running then the service is stopped
- modify: modify the name,startup,description of a service
- start: starts a service
- stop: stops a service
- restart: restarts a service

# JSON Examples

## General Info

- action field specifies the command (see supported commands for possible values)

## Add Service

```
{
    "action": "add",
    "name": "test Service",
    "description":"This is a simple test service!",
    "github_rep": "https://github.com/Callibrator/test_for_elsa.git",
    "github_username": "my-user",
    "github_password": "my-password",
    "install_file": "install.bat",
    "execute_file": "execute.bat",
    "startup":"true"

}
```

- name: The name of your service. Multiple services can have the same name
- description: Just a brief descriptions of your service
- github_rep: the github repository of your project, it will clone it locally!
- github_username: Used for github username if needed!
- github_password: Used for github password if needed!
- install_file: the bash/batch file that will run to install the requirments of your project
- execute_file: the bash/batch file that will run to execute the service
- startup: false if you do not want your service to start as soon as the program is starting

- If you catch your user credentials, you can skips github username and password. It is totally recommended!

## Modify Service

```
{
    "action": "modify",
    "service_id": service_id,
    "name": "test Service123",
    "description": "This is a simple test service!123",
    "startup": "true"

}
```

- name: The name of your service. Multiple services can have the same name
- description: Just a brief descriptions of your service
- startup: false if you do not want your service to start as soon as the program is starting
- service_id: the id of the service you want to modify

## Remove Service

```
{
    "action": "remove",
    "service_id": service_id

}
```

- service_id: The name of your service. Multiple services can have the same name

## Restart Service

```
{
    "action": "restart",
    "service_id": service_id

}
```

- service_id: The name of your service. Multiple services can have the same name

## Start Service

```
{
    "action": "start",
    "service_id": service_id

}
```

- service_id: The name of your service. Multiple services can have the same name


## Status Service

```
{
    "action": "status",

}
```

- service_id: The name of your service. Multiple services can have the same name


## Stop Service

```
{
    "action": "stop",
    "service_id": service_id

}
```

- service_id: The name of your service. Multiple services can have the same name



# Response Examples

## Status

```
[
   {
      "id":"8250f538-4a77-412f-90ea-d88249685d4c",
      "uri":"https://github.com/Callibrator/test_for_elsa.git",
      "name":"test Service",
      "description":"This is a simple test service!",
      "local_dir":"F:\\Sources\\Python Sources\\services\\8250f538-4a77-412f-90ea-d88249685d4c",
      "install_script":"install.bat",
      "execute_file":"execute.bat",
      "install_status":"success",
      "install_log":"\r\nF:\\Sources\\Python Sources\\services\\8250f538-4a77-412f-90ea-d88249685d4c>pip install -r requirments.txt \r\nRequirement already satisfied: numpy in f:\\python\\lib\\site-packages (from -r requirments.txt (line 1)) (1.15.1)\r\n",
      "install_error_log":"You are using pip version 18.1, however version 19.3.1 is available.\r\nYou should consider upgrading via the 'python -m pip install --upgrade pip' command.\r\n",
      "startup":true,
      "output_log":"",
      "error_log":"",
      "isRunning":true,
      "isTerminatedByUser":false,
      "isTerminated":false
   },
   {
      "id":"b8b64dbd-e861-4130-84e0-e5ef6634f426",
      "uri":"https://github.com/Callibrator/test_for_elsa.git",
      "name":"test Service",
      "description":"This is a simple test service!",
      "local_dir":"F:\\Sources\\Python Sources\\services\\b8b64dbd-e861-4130-84e0-e5ef6634f426",
      "install_script":"install.bat",
      "execute_file":"execute.bat",
      "install_status":"success",
      "install_log":"\r\nF:\\Sources\\Python Sources\\services\\b8b64dbd-e861-4130-84e0-e5ef6634f426>pip install -r requirments.txt \r\nRequirement already satisfied: numpy in f:\\python\\lib\\site-packages (from -r requirments.txt (line 1)) (1.15.1)\r\n",
      "install_error_log":"You are using pip version 18.1, however version 19.3.1 is available.\r\nYou should consider upgrading via the 'python -m pip install --upgrade pip' command.\r\n",
      "startup":true,
      "output_log":"",
      "error_log":"",
      "isRunning":false,
      "isTerminatedByUser":false,
      "isTerminated":false
   }
]
```


- Special Thanks to Zoi for her help in fixing a bug regarding the execution of a batch file!