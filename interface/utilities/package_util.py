"""
    __author__      : Rahul Kumeriya <rahul.kumeriya@outlook.com>
    __title__       : Package Utility
    __description__ : This porgram help to maintain the DEPLOYME
                        package stndards by Incrementing package
                        w.r.t Major, Minor, release and Backout
                        versions.
                      Pull the Latest version of package from
                        Remote to maintiant the flow of execution.
"""

import re
import os
import git
import logging
from interface.utilities.load_config import RepositoryConfig, RemoteServerConfig, ArtifactConfig


class PackageVersionIncrement():
    """
    Package Version Increment for Major, Minor, release and Backout
    """
    @staticmethod
    def increment_package_ver(pkg_string: str) -> str:
        """
        Returns Package incremented
         
        :param pkg_string: The package string

        :returns:
            Incremented package string
        """

        pkg_number = pkg_string.split('.')
        pkg_number[-1] = str(int(pkg_number[-1]) + 1)
        return '.'.join(pkg_number)

    @staticmethod
    def upgrade_pkg_minor_ver(pkg_string: str) -> str:
        """ 
        Returns Package Minor version

        :param pkg_string: The package string

        :returns:
            Incremented package string
        """
        pkg_number = pkg_string.split('.')
        pkg_number[-2] = str(int(pkg_number[-2]) + 1)
        return '.'.join(pkg_number)

    @staticmethod
    def upgrade_pkg_major_ver(pkg_string: str) -> str:
        """ Returns Package Major version

        :param pkg_string: The package string

        :returns:
            Incremented package string
        """
        pkg_number = pkg_string.split('.')
        pkg_number[-3] = str(int(pkg_number[-3]) + 1)
        return '.'.join(pkg_number)

    @staticmethod
    def backout_package_ver(pkg_string: str) -> str:
        """
        Returns Package Backout version

        :param pkg_string: The package string

        :returns:
            Incremented package string
        """
        pkg_number = pkg_string.split('.')
        pkg_number[2] = "5"
        return '.'.join(pkg_number)


class LatestPackage():
    """
    Get the latest package from Remote and Local
    """
    def __init__(self, repo_config: RepositoryConfig, serv_config: RemoteServerConfig, artf_config: ArtifactConfig):
        """
        The Constructor for latest Package

        :param repo_config: NamedTuple class with repository configuration
        :param serv_config: NamedTuple class with remote server configuration
        """
        self._logger = logging.getLogger(__name__)
        self.repo_config = repo_config
        self.serv_config = serv_config
        self.artf_config = artf_config

    def get_latest_remote(self) -> str:
        """
        Returns the remote tags with GitPython module and dilter out
        the highest package version to get the numerical value like 1500

        :returns:
            last Digit of tag
        """
        g = git.cmd.Git()
        return_list = map(
            lambda x: x.split('.')[3], re.findall(
                r'refs/tags/10.0.0.\d{1,4}',
                g.ls_remote(
                    "--refs", "--tags",
                    self.repo_config.remoterepo)
                ))
        if return_list == []:
            return '0'
        return max(return_list)

    def get_latest_local(self) -> str:
        """
        Directory Walk function which read the local path files and
        extract the file name
        This function utilizes more time than Remote

        :returns:
            last Digit of tag
        """
        return_list = [int(i.split('.')[3]) for i in os.listdir(self.repo_config.localrepo) if i.endswith(self.artf_config.artifactends) and i.startswith(self.artf_config.artifactstart)]
        if return_list == []:
            return '0'
        return max(return_list)

    # For command base method to get remote max version
    # Equivalent method to  get_latest_remote
    # def get_latest_remote_cmd(self) -> str:
    #     """
    #     Get the remote Tags with command Line command and filter the get max
    #     package version number
    #     It will return interger value like 1400

    #     :returns:
    #         last Digit of tag
    #     """
    #     git_cmd_start =\
    #         'git ls-remote -q --refs --tags --sort="version:refname"'
    #     git_cmd_end = '10.0.*.*'
    #     cmd = f'{git_cmd_start} {self.repo_config.remoterepo} {git_cmd_end}'
    #     return_list = map(
    #         lambda x: x.split('.')[3], re.findall(
    #             r'refs/tags/10.0.0.\d{1,4}', os.popen(cmd).read()))
    #     if return_list == []:
    #         return '0'
    #     return max(return_list)
