"""Test PacakgeUtil"""


import unittest
from interface.utilities.load_config import RepositoryConfig, RemoteServerConfig, ArtifactConfig
from interface.utilities.package_util import LatestPackage, PackageVersionIncrement


class TestLatestPackage(unittest.TestCase):
    """
    Testing the LatestPackage class
    """
    def setUp(self):
        """
        Setting up the environment
        """
        # Creating artifact configuration
        conf_dict_artifact = {
            "artifactstart": "TEST-10",
            "artifactends": ".tar.gz",
            "artifact_base": "TEST-10.0.0",
            "templatelist": ['COPY_FILES', 'CREATE_DIR', 'MONGO_QUERY', 'ORACLE_QUERY',
                'QUERY', 'RESTORE_FILES', 'UPDATE_ENV_FILE'],
            "permissionlist": ['775', '777', '776', '765'], 
            "environment": {"ASIA": 'ASIA', "EMEA": 'EMEA', "DEV": "DATABASE"},
            "regexlist": [
                '^TEST-10.\d*.\d*.\d*$',
                '^TEST-\d{1,2}.\d{1,2}.\d{1,3}.\d{1,4}$'
            ]
        }
        conf_remote_server = {
            "hostname": "raahool-HP-Pavilion-15-Notebook-PC",
            "port": 22,
            "username": "raahool",
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
        self.artf_config = ArtifactConfig(**conf_dict_artifact)

    def test_get_latest_local(self):
        """
        Test get_latest_local method for latest artifact tag
        from local repository 
        """
        v = LatestPackage(self.repo_config, self.serv_config, self.artf_config).get_latest_local()
        self.assertNotEqual('0', v)

    def test_get_latest_remote(self):
        """
        Test get_latest_remote method for latest artifact tag
        from remote repository 
        """
        v = LatestPackage(self.repo_config, self.serv_config, self.artf_config).get_latest_remote()
        self.assertNotEqual('0', v)

 
class TestPackageVersionIncrement(unittest.TestCase):
    """
    Testing the PackageVersionIncrement class
    """        
    def test_increment_package_ver(self):
        """
        Test increment_package_ver method for incremented
        artifact string
        """
        # Expected Result
        exp_result = 'TEST-10.0.0.2'
        wrong_result = 'TEST-10.0.0.1'
        # Test init
        artifact = 'TEST-10.0.0.1'
        # Method execution
        v = PackageVersionIncrement.increment_package_ver(artifact)
        self.assertEqual(v, exp_result)
        self.assertNotEqual(v, wrong_result)

    def test_upgrade_pkg_minor_ver(self):
        """
        Test upgrade_pkg_minor_ver method for minor versio incremented
        artifact string
        """
        # Expected Result
        exp_result = 'TEST-10.0.1.1'
        wrong_result = 'TEST-10.0.0.1'
        # Test init
        artifact = 'TEST-10.0.0.1'
        # Method execution
        v = PackageVersionIncrement.upgrade_pkg_minor_ver(artifact)
        self.assertEqual(v, exp_result)
        self.assertNotEqual(v, wrong_result)

    def test_upgrade_pkg_major_ver(self):
        """
        Test upgrade_pkg_major_ver method for major version incremented
        artifact string
        """
        # Expected Result
        exp_result = 'TEST-10.1.0.1'
        wrong_result = 'TEST-10.0.0.1'
        # Test init
        artifact = 'TEST-10.0.0.1'
        # Method execution
        v = PackageVersionIncrement.upgrade_pkg_major_ver(artifact)
        self.assertEqual(v, exp_result)
        self.assertNotEqual(v, wrong_result)

    def test_backout_package_ver(self):
        """
        Test backout_package_ver method for backout/rollback incremented
        artifact string
        """
        # Expected Result
        exp_result = 'TEST-10.0.5.1'
        wrong_result = 'TEST-10.0.2.1'
        # Test init
        artifact = 'TEST-10.0.0.1'
        # Method execution
        v = PackageVersionIncrement.backout_package_ver(artifact)
        self.assertEqual(v, exp_result)
        self.assertNotEqual(v, wrong_result)
