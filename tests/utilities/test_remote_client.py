"""RemoteClientUtilty class"""


import unittest
from unittest import result
from interface.utilities.load_config import RemoteServerConfig, RepositoryConfig
from interface.utilities.remote_client import RemoteClientUtility
from interface.common.custom_exceptions import FailedToCopyFile


class TestRemoteClientUtility(unittest.TestCase):
    """
    Testing the ProcessGitLocal class
    """

    def setUp(self):
        """
        Setting up the environment
        """
        # Creating artifact configuration
        conf_remote_server = {
            "hostname": "raahool-HP-Pavilion-15-Notebook-PC",
            "port": 22,
            "username": "raahool",
            "password": "REMOTE_SER_PASSWORD",
            "source":  "/var/tmp",
            "destination": "/opt/uDeploy",
            "processor": "/opt/server_action",
        }
        non_conf_remote_server = {
            "hostname": "raahool-HP-Pavilion-15-Notebook-PC",
            "port": 22,
            "username": "unknown",
            "password": "REMOTE_SER_PASSWORD",
            "source":  "/var/tmp",
            "destination": "/opt/uDeploy",
            "processor": "/opt/server_action",
        }
        conf_dict_repo = {
              "remoterepo": "git@bitbucket.org:raahoolkumeriya/repo-adhoc-space.git",
              "localrepo": "/application/repository/repo-adhoc-space/"
        }
        
        self.repo_config = RepositoryConfig(**conf_dict_repo)
        self.serv_config = RemoteServerConfig(**conf_remote_server)
        self.non_serv_config = RemoteServerConfig(**non_conf_remote_server)
        self.client = RemoteClientUtility(self.serv_config, self.repo_config)

    def test_connect_server(self):
        """
        Remote server Connect 
        """
        # Expected Result
        exp_result = (['Linux\n'], [])
        # Test init
        cmd = 'uname'
        # Method execution
        v = self.client.connect_server(cmd)
        # Tests methods
        self.assertEqual(exp_result, v)

    # def test_connect_server_exception_raise(self):
    #     """
    #     Connect server exception test
    #     """
    #     # Method execution
    #     with self.assertRaises(Exception):
    #         cmd = "uname"
    #         self.client.connect_server(cmd)
            
    def test_execute_package_utility(self):
        """
        Test execute_package_utility method for package development
        """
        artifact = 'TEST-10.0.0.1'
        mode = 'unix'
        option = 'test.sh'
        v = RemoteClientUtility(self.serv_config, self.repo_config).execute_package_utility(
            artifact, mode, option
        )
        self.assertEqual(v[1], [])

    def test_execute_template(self):
        """
        Test execute_template method for template execution
        """ 
        # Expected
        result = "{'TEMPLATE_EXECUTED': 'Artifact deployment script udpated with template content'},{'BACKOUT_SKIPPED': 'No action'}\n"
        # Test init
        raw_string = {
                "template_name": 'COPY_FILES',
                "pkg_directory": 'TEST-10.0.0.1',
                "script_name": 'test.sh',
                "pkg_details": {
                            "__parameter_one__": '/var/tmp',
                            "__parameter_two__": 'TEST',
                            "__parameter_three__": '775'
                      }
        }
        v = RemoteClientUtility(self.serv_config, self.repo_config).execute_template(raw_string)
        self.assertEqual(v, result) 


    def test_run_udeploy_process(self):
        """
        Test run_udeploy_process shell script
        """
        # Expected result
        result = (['10.0.0.1 already exists\n'], [])
        # Test Init
        artifact = "TEST-10.0.0.1"
        version = "10.0.0.1"
        v = RemoteClientUtility(self.serv_config, self.repo_config).run_udeploy_process(
            artifact, version)
        self.assertEqual(v, result)

    def test_download_artifact_to_local(self):
        """
        Test download_artifact_to_local method to place artifact to repository 
        location at local space
        """
        # Test init
        artifact = 'TEST-10.0.0.1.tar.gz'
        with self.assertRaises(FailedToCopyFile):
            RemoteClientUtility(self.serv_config, self.repo_config).download_artifact_to_local(artifact)

    def test_download_artifact_to_local_remote_version(self):
        """
        Test download_artifact_to_local method to place artifact to repository 
        location at local space
        """
        # Test init
        artifact = 'TEST-10.0.0.1.tar.gz'
        v = RemoteClientUtility(self.serv_config, self.repo_config).download_artifact_to_local_remote_version(artifact)
        self.assertEqual(v, None)

    def test_upload_artifact_to_server(self):
        """
        Test upload_artifact_to_server method to uplaod artifact to remote
        server
        """
        artifact_list = ['TEST-10.0.0.1.tar.gz']
        with self.assertRaises(FileNotFoundError):
            RemoteClientUtility(self.serv_config, self.repo_config).upload_artifact_to_server(artifact_list)

