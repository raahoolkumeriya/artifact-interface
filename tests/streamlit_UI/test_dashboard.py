"""TestProcessGitLocal Class"""


import unittest
from interface.common.validation import Validations
from interface.utilities.load_config import ArtifactConfig, RepositoryConfig
from interface.streamlit_UI.dashboard import ProcessGitLocal


class TestProcessGitLocal(unittest.TestCase):
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
        non_conf_dict_repo = {
              "remoterepo": "git@bitbucket.org:raahoolkumeriya/no_repository.git",
              "localrepo": "/application/repository/no_repository"
        }
        self.artf_config = ArtifactConfig(**conf_dict_artifact)
        self.repo_config = RepositoryConfig(**conf_dict_repo)
        self.non_repo_config = RepositoryConfig(**non_conf_dict_repo)
        self.client = ProcessGitLocal(
            self.repo_config,
            self.artf_config)
        self.df = self.client.construct_dataframe()
        self.non_df = ""

    def test_formation_of_data(self):
        """
        Formation of statistics from repository
        """
        # Method execution
        result = self.client.formation_of_data(self.df)
        self.assertIn('dataframe', result.keys())
        self.assertIn('date_dataframe', result.keys())
        self.assertIn('hour_dataframe', result.keys())
        self.assertIn('year_dataframe', result.keys())
        self.assertIn('month_dataframe', result.keys())
        self.assertNotIn('non_dataframe', result)

    def test_formation_of_data_to_halt(self):
        """
        Halting of Statistics from Non repository
        """
        # Method execution
        with self.assertRaises(Exception):
            self.client.formation_of_data(self.non_df)
