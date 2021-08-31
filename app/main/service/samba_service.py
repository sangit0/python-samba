import uuid
import datetime
import tempfile
import paramiko
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import app
from smb.SMBConnection import SMBConnection
from ..util.dto import FilesDTO
_files = FilesDTO.file
from flask import current_app
api = FilesDTO.api

file_path = "/var/www/html/app/";

def create_user_using_ssh(username,password,user_folder):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(current_app.config["SAMBA_IP"], username=current_app.config["SAMBA_USER"], password=current_app.config["SAMBA_USER_PASS"])

    # "etc/samba/smb.tmp"
    stdin, stdout, stderr = client.exec_command(f"./create-user.sh {username}")
    stringOutput = ""
    for line in stdout:
        stringOutput = stringOutput + '... ' + line.strip('\n')
    client.close()
    return stringOutput

def change_password(username,password):
    session = Popen(['/bin/bash',f'{file_path}update-password.sh',f'{username}',f'{password}'], stdout=PIPE, stderr=PIPE)    
    stdout, stderr = session.communicate()
    if session.returncode !=0:
        raise Exception("Error while updating password! \n"+str(stderr))
    return True
def create_user_using_command(username,password,user_folder):
    session = Popen(['/bin/bash',f'{file_path}create-user.sh',f'{username}',f'{password}'], stdout=PIPE, stderr=PIPE)    
    stdout, stderr = session.communicate()
    if session.returncode !=0:
        raise Exception("Error while creating user! \n"+str(stderr))
    return True

def connect(username,password):
    global conn

    userID = username
    password = password
    client_machine_name = current_app.config["SAMBA_IP"]

    server_name = 'servername'
    server_ip = current_app.config["SAMBA_IP"]

    domain_name = 'workgroup'

    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, 
                        use_ntlm_v2=True,
                        is_direct_tcp=True)

    return conn.connect(server_ip, 445)
def disconnect():
    conn.close()
    
def get_file_list(username,password,user_folder,path):
    try: 
        if connect(username,password):
            try:
                shares = conn.listShares()
                fileNames = []
                sharedfiles = conn.listPath(user_folder, path)
                return get_files_by_folder(sharedfiles)
            except Exception as e:
                raise FileNotFoundError("Error file or user not found") 
        else:
            raise ConnectionError("Connection error! wrong username")   
    except Exception as e:
            raise e   
         


def get_files_by_folder(sharedfiles):
    dirs  = []
    for sharedfile in sharedfiles:
        string_path = ""
        if sharedfile.filename not in [u'.', u'..']:
            string_path +=  sharedfile.filename
            file_info = {
                    'name': sharedfile.filename, 
                    'is_directory' : sharedfile.isDirectory,
                    'file_size' : sharedfile.file_size,
                    'path' : string_path,
                }
            dirs.append(file_info)
    disconnect()
    return dirs
        
def download_normal(username,password,user_folder,files: list):
    try: 
        if connect(username,password):
            pass
        else:
            raise ConnectionError("Connection error! wrong username")
                                      
        return True  
    except Exception as e:
        raise ConnectionError("Connection error")   
        

def download_using_file_writter(username,password,user_folder,files: list):
    try: 
        if connect(username,password):
            pass
        else:
            raise ConnectionError("Connection error! wrong username")
        """ Download files from the remote share. """
        for file in files:
            with open("app/main/downloads/" + file, 'wb') as file_obj:
                conn.retrieveFile(service_name=user_folder,
                                        path=file,
                                        file_obj=file_obj)
        disconnect()   
        file_obj.close()                               
        return True  
    except Exception as e:
        raise ConnectionError("Connection error")
