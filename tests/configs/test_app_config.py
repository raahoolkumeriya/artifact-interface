""" Test App configuration """

import os
import unittest


class TestAppConfigParameters(unittest.TestCase):
    """
    Testing the Application config parameters
    """

    def test_environment_variable_set_on_os(self):
        """
        Test the paramters setup in enviroment
        """
        # Expected results
        app_ser_password = "REMOTE_SER_PASSWORD"
        jira_auth_token = "JIRA_AUTH_TOKEN"
        slack_api_token = "SLACK_API_TOKEN"
        # Test init
        # Method execution
        # tests after method execution
        self.assertNotEqual(os.getenv(app_ser_password), "")
        self.assertNotEqual(os.getenv(jira_auth_token), "")
        self.assertNotEqual(os.getenv(slack_api_token), "")
