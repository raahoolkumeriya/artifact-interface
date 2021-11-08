"""Test GitClientUtility class"""


import unittest
from unittest import result

from git.exc import GitCommandError
from interface.utilities.load_config import RepositoryConfig, ArtifactConfig, RemoteServerConfig
from interface.utilities.git_client import GitClientUtility


class TestGitClientUtility(unittest.TestCase):
    """
    Testing the ProcessGitLocal class
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
        conf_dict_repo = {
              "remoterepo": "git@bitbucket.org:raahoolkumeriya/repo-adhoc-space.git",
              "localrepo": "/application/repository/repo-adhoc-space/"
        }
        conf_dict_non_repo = {
              "remoterepo": "git@bitbucket.org:raahoolkumeriya/repo-adhoc.git",
              "localrepo": "/application/repository/repo-adhoc-space/"
        }
        self.artf_config = ArtifactConfig(**conf_dict_artifact)
        self.repo_config = RepositoryConfig(**conf_dict_repo)
        self.repo_non_config = RepositoryConfig(**conf_dict_non_repo)
        self.client = GitClientUtility(self.repo_config, self.artf_config)
        # self.non_client = GitClientUtility(self.repo_non_config, self.artf_config)
        

    def test_git_pull_to_sync(self):
        """
        Test git_pull_to_sync method 
        """
        # Expected Result
        exp_result = True
        # Method execution
        v = self.client.git_pull_to_sync()
        # Tests methods
        self.assertEqual(exp_result, v)

    def test_git_push_to_sync(self):
        """
        Test git_push_to_sync method
        """
          # Expected Result
        exp_result = True
        # Method execution
        v = self.client.git_push_to_sync()
        # Tests methods
        self.assertEqual(exp_result, v)

    # def test_git_pull_to_sync_for_exception(self):
    #     """
    #     Test git_pull_to_sync from exception 
    #     """
    #     with self.assertRaises(GitCommandError):
    #         self.non_client.git_pull_to_sync()
   