"""Git Client Utility for Artifact tasks"""

import os
import logging
from git import Repo, GitCommandError
from typing import List, Dict
from interface.utilities.load_config import RepositoryConfig, ArtifactConfig


class GitClientUtility():
    """
    Class for Git utilities to process Artifact tasks
    """
    def __init__(self, repo_config: RepositoryConfig, artf_config: ArtifactConfig):
        self.repo_config = repo_config
        self.artf_config = artf_config
        self.git_dir = ".git"
        self.repository = Repo(os.path.join(self.repo_config.localrepo +'/' + self.git_dir))
        self._logger = logging.getLogger(__name__)

    def git_pull_to_sync(self) -> bool:
        """Pulling updates to local from remote"""
        self.repository.git.pull()
        return True

    def git_push_to_sync(self) -> bool:
        """Push updates to remote from local"""
        self.repository.git.push()
        return True

    def git_delete_tag_local(self, tag_name: str) -> bool:
        """Delete Tag"""
        # Local Tag Deletion
        try:
            self.repository.delete_tag(tag_name)
            return True
        except GitCommandError:
            return False

    def git_delete_tag_remote(self, tag_name: str) -> str:
        """Delete Tag fom Remote"""
        # Remote Tag Deletion
        try:
            remote = self.repository.remote(name="origin")
            remote.push(refspec=(f':{tag_name}'))
            return True
        except GitCommandError:
            return False

    def git_push_artifact(
        self,
        artifact_name: str,
        commit_message: str,
        issue_key: str
            ) -> Dict:
        """Push Artifact to repository with linked jira key"""
        if os.path.isfile(os.path.join(self.repo_config.localrepo, artifact_name)):
            logging.info("File successfully downloaded to local")
            try:
                tag_name = artifact_name.split('-')[1].split('.tar')[0]
                self.repository.git.add(artifact_name)
                self.repository.git.commit(
                        m='[%s] %s' % (issue_key, commit_message))
                commit_id = self.repository.commit('master')
                self.repository.create_tag(tag_name)
                self.repository.remotes.origin.push(tag_name)
                self.repository.git.push()
                return dict({"tag_name": tag_name, "commit_id": commit_id})
            except Exception as diag:
                logging.info(f"{diag.__class__.__name__}:{diag}")
                return None

    def get_requested_package_by_list(self, artifact_list: List) -> List:
        """Get Filtered artifact list"""
        filenames = []
        for artifact in artifact_list:
            for _, dirs, files in os.walk(self.repo_config.localrepo):
                if self.git_dir in dirs:
                    dirs.remove(self.git_dir)
                filenames.append(
                    [i for i in files if i.endswith(str(artifact)+self.artf_config.artifactends)])
        return list(filter(None, filenames))

    def get_requested_package_by_last_digits(
        self,
        artifact_number: str
            ) -> List:
        """Get Filtered artifact with Last digits"""
        filenames = []
        for root, dirs, files in os.walk(self.repo_config.localrepo):
            if self.git_dir in dirs:
                dirs.remove(self.git_dir)
            filenames.append(
                [os.path.abspath(os.path.join(root, i)) for i in files if i.endswith(str(artifact_number) + self.artf_config.artifactends)])
        return list(filter(None, filenames))

    def get_file_from_local_repository(self) -> List:
        """ Get Files from local Repository """
        list_dir_file = []
        path_ = os.path.abspath(self.repo_config.localrepo)
        for root, dirs, files in os.walk(path_):
            for file_ in files:
                if self.git_dir in dirs:
                    dirs.remove(self.git_dir)
                list_dir_file.append(os.path.join(root, file_))
        return list_dir_file
