import json
from typing import NamedTuple

from pkg_resources import Environment

class RemoteServerConfig(NamedTuple):
    """
    Class for remtote server configuration data
    
    hostname: Remote server hostname
    port: Remote server port
    username: Remote server port
    password: Remote server password
    source: Remote server source location for artifact
    destination: Remote server destination udeploy script path
    processor: Udeploy Script path
    """
    hostname: str
    port: int
    username: str
    password: str
    source: str
    destination: str
    processor: str

class JiraConfig(NamedTuple):
    """
    Class for jira configuration data
    
    rooturl: jira restapi root url
    username: Jira user
    authtoken: Jira auth token string
    headers: Headers for jira restapi connection
    lead: Jira project lead
    project: Project of jira space
    label: label for the jira tickets
    region: Region for jira space
    component: component of jira sprint
    priority: Priority of jira ticket to update/create
    type: Jira ticket type
    """
    rooturl: str
    username: str
    authtoken: str
    headers: dict
    lead: str
    project: str
    label: str
    region: str
    component: str
    priority: str
    type: str

class RepositoryConfig(NamedTuple):
    """
    Class for Repository configuration data

    remoterepo: Remote URL for repository
    localrepo: Local directory location of repository
    """
    remoterepo: str
    localrepo: str

class ArtifactConfig(NamedTuple):
    """
    Class for Artifact configuration data

    artifactstart: Artifact Starts String
    artifactends: Artifact Ending string
    artifact_base: Base version of Artifact
    templatelist: Template list resides on server
    permissionlist: Permission list for file and dir
    environment: Enivronment base of config.csv files
    regexlist: List of Regex for capture wide artifacts
    """
    artifactstart: str
    artifactends: str
    artifact_base: str
    templatelist: list
    permissionlist: list
    environment: dict
    regexlist: list

class UdeployConfig(NamedTuple):
    """
    Class for Udeploy configuration data

    rooturl: str
    headers: dict    
    """
    rooturl: str
    headers: dict

class SlackConfig(NamedTuple):
    """
    Class for Slack configuration

    authtoken: auth token for communication
    channelid: Channel Id form slack group
    """
    authtoken: str
    channelid: str


class JsonFormating():
    """Json String Formating class"""
    def __init__(self, json_obj):
        self.obj = json_obj

    def __str__(self):
        return json.dumps(
            self.obj, sort_keys=True,
            indent=4, separators=(",", ": "))
