import os
import json
import requests
# Disable insecure SSL warnings
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)
from interface.utilities.load_config import JsonFormating


class ArtifactoryClient():
    """
    Artifactory REST Client
    - Intilized artifactory REST Url and API key in environment varaible
    - set proxy if any
    """
    def __init__(self):
        self.url = os.getenv('artiactoryRootUrl')
        self.header = {
            "Content-Type": "application/x-gzip",
            "X-JFrog-Art-Api": os.getenv("artifactoryAPIKey")}
        self.proxy = {}

    def upload_artifact(self, path: str, artifact: str) -> json:
        """
        Upload artifact to Artifactory
        """
        url = f"{self.url}/{artifact}"
        try:
            response = requests.put(
                url,
                headers=open(os.path.join(path, artifact), 'rb'),
                verify=False, proxies=self.proxy)
            if response.status_code != 201:
                return JsonFormating(response.text)
            else:
                return response.text.get('uri')
        except Exception as diag:
            return {"result": f"failed to upload artifact -> {diag}"}

    def delete_artifact(self, artifact: str) -> json:
        """ Return response 204 if artifact exists
            Return response 404 if artifact doesn't exists
        """
        url = f"{self.url}/{artifact}"
        try:
            response = requests.delete(
                url,
                verify=False, proxies=self.proxy)
            if response.status_code != 204:
                return JsonFormating(response.text)
            else:
                return {"result": f"{artifact} deleted from Artifactory Space"}
        except Exception as diag:
            return {"result": diag}
