"""Udeploy Clinet Utility for Artifact"""

import os
import requests
import json
import logging
from interface.utilities.load_config import JsonFormating, UdeployConfig


class UdeployUtilityClient(JsonFormating):
    """ Udeploy REST Client """
    def __init__(self, udep_config: UdeployConfig):
        self.udep_config = udep_config
        self._logger = logging.getLogger(__name__)

    def get_list_of_version(self):
        """Get list of versions"""
        url = f"""{self.udep_config.rooturl}"""
        response = requests.get(
            url, 
            headers=self.udep_config.headers)
        # return JsonFormating(response.json())
        parse = response.json()
        return parse

    def create_version(self, artifact_name: str, version_name: str):
        """Create Version in Udeploy"""
        payload = json.dumps({
                'artifact_name': artifact_name,
                'version_name': version_name
        })
        self._logger.info(payload)
        url = f"""{self.udep_config.rooturl}"""
        response = requests.post(
            url, data=payload,
            headers=self.udep_config.headers)
        return JsonFormating(response.json())
