"""TestValidation"""


import unittest
from interface.common.validation import Validations
from interface.utilities.load_config import ArtifactConfig


class TestValidation(unittest.TestCase):
    """
    Testing the Validation class
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
        self.artf_config = ArtifactConfig(**conf_dict_artifact)
        
    def test_check_artifact_string(self):
        """
        Test check_artifact_string method for valid
        artifact string
        """
        # Test init
        artifact = 'TEST-10.0.0.1'
        non_artifact = 'TEST-0.0-123'
        # Method execution
        v1 = Validations(self.artf_config).check_artifact_string(artifact)
        self.assertTrue(v1)
        v2 = Validations(self.artf_config).check_artifact_string(non_artifact)
        self.assertTrue(v2)

    def test_get_correct_artifact_name(self):
        """
        Test get_correct_artifact_name method for correct
        artifact name
        """
        result = 'TEST-10.0.0.0'
        a1 = 'TEST-10.0.0.0'
        a2 = 'TEST-10.0.0.0.tar'
        a3 = 'TEST-10.0.0.0.tar.gz'
        a4 = 'TEST-10.0.0.0.tgz'
        v1 = Validations(self.artf_config).get_correct_artifact_name(a1)
        v2 = Validations(self.artf_config).get_correct_artifact_name(a2)
        v3 = Validations(self.artf_config).get_correct_artifact_name(a3)
        v4 = Validations(self.artf_config).get_correct_artifact_name(a4)
        self.assertEqual(v1, result)
        self.assertEqual(v2, result)
        self.assertEqual(v3, result)
        self.assertEqual(v4, result)

    def test_return_artifact_name(self):
        """
        Test return_artifact_name method for return
        as tar gzip developed artifact
        """
        result = 'TEST-10.0.0.0.tar.gz'
        a = 'TEST-10.0.0.0'
        v = Validations(self.artf_config).return_artifact_name(a)
        self.assertEqual(v, result)

    def test_get_version_name(self):
        """
        Test get_version_name method for version name 
        from the artifact
        """
        result = '10.0.0.0'
        a1 = 'TEST-10.0.0.0'
        a2 = 'TEST-10.0.0.0.tar.gz'
        a3 = 'TEST-10.0.0.0.tgz'
        v1 = Validations(self.artf_config).get_version_name(a1)
        v2 = Validations(self.artf_config).get_version_name(a2)
        v3 = Validations(self.artf_config).get_version_name(a3)
        self.assertEqual(v1, result)
        self.assertEqual(v2, result)
        self.assertEqual(v3, result)
