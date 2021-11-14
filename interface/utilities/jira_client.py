"""Jira Client Utility for Artifact"""

import os
import requests
import json
import logging
from requests.auth import HTTPBasicAuth
from interface.common.constants import ErrorCodesMessages as codes
from interface.utilities.load_config import JiraConfig, JsonFormating
from interface.common.custom_exceptions import InvalidAuthToken, FailedToAssigned, FailedToUpdate


class Auth():
    """
    Authentication for Header Proxy setup

    :param  jira_config: Load jira configuration 
    """
    def __init__(self, jira_config: JiraConfig):
        """
        Set up proxy information if configuration contains proxyURL
        :param config: Object contains all certificate configurations
        """
        self._logger = logging.getLogger(__name__)
        self.jira_config = jira_config

    def authenticate(self):
        """
        Get the user authentication
        :returns:
            HTTPBasicAuth of User credentials
        """
        try:
            if os.environ[self.jira_config.authtoken]:
                return HTTPBasicAuth(
                    self.jira_config.username,
                    os.environ[self.jira_config.authtoken])
            else:
                logging.info(codes.USER_PASS_ERR.value)
        except Exception as diag:
            logging.info(f"{diag.__class__.__name__}:{diag}")
            raise InvalidAuthToken


class JiraRESTClient(Auth, JsonFormating):
    """ JIRA Rest Client """
    def __init__(self, jira_config: JiraConfig):
        self.jira_config = jira_config
        self.auth = Auth(self.jira_config).authenticate()

    def get_issue(self, key: str):
        """Get Jira ticket if its exists"""
        url = f"""{self.jira_config.rooturl}/issue/{key}"""
        response = requests.get(
            url, auth=self.auth,
            headers=self.jira_config.headers)
        # return JsonFormating(response.json())
        parse = response.json()
        if 'key' in parse:
            return parse.get('key')
        else:
            return parse.get('errorMessages')[0]

    def create_issue(self, summary: str, description: str = None):
        """Create Jira Ticket"""
        payload = json.dumps({
            "fields": {
                "project": {"key": self.jira_config.project},
                "summary": summary,
                "priority": {"name": self.jira_config.priority},
                "issuetype": {"name": self.jira_config.type},
                "components": [{"name": self.jira_config.component}],
                "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{
                                    "text": description,
                                    "type": "text"}
                                ]}]},
                "assignee": {"name": self.jira_config.username}
            }
        })
        url = f"""{self.jira_config.rooturl}/issue/"""
        response = requests.post(
            url, data=payload,
            headers=self.jira_config.headers, auth=self.auth)
        return JsonFormating(response.json())

    def update_comment(self, issue_key: str, comment_string: str):
        """Update Jira ticket comments"""
        try:
            payload = json.dumps({
                "body": {
                        "type": "doc",
                        "version": 1,
                        "content": [{
                                "type": "paragraph",
                                "content": [{
                                    "text": "Furiosa: %s" % comment_string,
                                    "type": "text"
                                }]
                        }]}
                })
            url =\
                f'{self.jira_config.rooturl}/issue/{issue_key}/comment'
            response = requests.post(
                url, data=payload,
                headers=self.jira_config.headers, auth=self.auth)
            print(f"{issue_key} updated at {response.json()['updated']}")
            return response.json()['updated']
        except Exception as _:
            raise FailedToUpdate

    def assign_issue(self, issue_key):
        """Assign jira ticket to executor"""
        try:
            payload = json.dumps({
                "accountId": self.jira_config.lead})
            url = f'{self.jira_config.rooturl}/issue/{issue_key}/assignee'
            response = requests.put(
                url, data=payload,
                headers=self.jira_config.headers, auth=self.auth)
            return True
        except Exception as _:
            raise FailedToAssigned  
