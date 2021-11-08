"""Remote Client Utility"""

import os
import json
import shutil
import logging
from typing import Dict, List
from time import sleep
from paramiko import SSHClient, AutoAddPolicy
from interface.utilities.load_config import RemoteServerConfig, RepositoryConfig
from interface.common.custom_exceptions import FailedToCopyFile


class RemoteClientUtility():
    """
    Linux Utility to perform on Remote and local server
    """
    def __init__(self, serv_config: RemoteServerConfig, repo_config: RepositoryConfig):
        self.serv_config = serv_config
        self.repo_config = repo_config
        self._logger = logging.getLogger(__name__)
            
    def connect_server(self, cmd):
        try:
            client = SSHClient()  
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                    self.serv_config.username,
                    self.serv_config.port,
                    self.serv_config.username,
                    os.environ[self.serv_config.password])    
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_code = stdout.channel.recv_exit_status()
            stdin.close()
            # wait for the command to terminate
            while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
                sleep(1)
            stdoutstring = stdout.readlines()
            stderrstring = stderr.readlines()
            self._logger.info(f"exit_code : {exit_code}")
            return stdoutstring, stderrstring
        except Exception as diag:
            self._logger.error(f"Client connection Failed: {diag}")
        finally:
            client.close()

    def execute_package_utility(self, artifact_name: str, mode: str, option: str):
        """Function wraps the command for execution"""
        script =\
            f'{self.serv_config.processor}/package_utility.sh'
        return self.connect_server(
            f'bash {script} {artifact_name} {mode} {option}')

    def execute_template(self, raw_string: Dict):
        """Function execute tempalte script"""
        script =\
            f'{self.serv_config.processor}/execute_template.py'
        try:
            return os.popen(
                f"python {script} '''{json.dumps(raw_string)}'''").read()
        except Exception as diag:
            logging.warning(diag)
            return self.connect_server(
                f"python {script} '''{json.dumps(raw_string)}'''")

    def run_udeploy_process(self, artifact_name: str, version: str):
        """Function wraps the command for execution"""
        script =\
            f'{self.serv_config.destination}/process/application_process.sh'
        output = self.connect_server(
            f'''bash {script} "{artifact_name}" {version}''')
        self._logger.info(output)
        return output

    def download_artifact_to_local(self, artifact_name: str):
        source = f"{self.serv_config.source}/{artifact_name }"
        destination = f"{self.repo_config.localrepo}/{artifact_name}"
        print(f"{source} --> {destination}")
        try:
            shutil.copyfile(source, destination)
            return "File copied successfully."
            # If source and destination are same
        except shutil.SameFileError:
            return "Source and destination represents the same file."
            # If destination is a directory.
        except IsADirectoryError:
            return "Destination is a directory."
            # If there is any permission issue
        except PermissionError:
            return "Permission denied."
            # For other errors
        except Exception as _:
            raise FailedToCopyFile

    def download_artifact_to_local_remote_version(self, artifact_name: str):
        self.gitLocalPath = os.path.join(self.repo_config.localrepo + '.git')
        try:
            client = SSHClient()  
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                    self.serv_config.username,
                    self.serv_config.port,
                    self.serv_config.username,
                    os.environ[self.serv_config.password])    
            self._logger.info(
                f"sftp connection made to download packages {artifact_name}")
            sftp = client.open_sftp()
            sftp.get(
                f'{self.serv_config.source}/{artifact_name}',
                os.path.join(
                    self.repo_config.localrepo, artifact_name))
            sftp.close()
            client.close()
            del sftp, client
            return True
        except Exception as diag:
            self._logger.error(f"SFTP Connection failed with Server...{diag}")

    def upload_artifact_to_server(self, list_of_files: List):
        """Upload Fiels to Linux server"""
        try:
            client = SSHClient()  
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                    self.serv_config.username,
                    self.serv_config.port,
                    self.serv_config.username,
                    os.environ[self.serv_config.password])    
            self._logger.info(
                f"FTP connection making to upload packages {list_of_files}")
            ftp_client = client.open_sftp()
            for i in list_of_files:
                ftp_client.put(
                    i,
                    f"""{self.serv_config.source}/{os.path.basename(i)}""")
            ftp_client.close()
            client.close()
            del ftp_client, client
            return True
        except Exception as diag:
            self._logger.info(f"FTP Connection failed with Server...{diag}")
            raise
