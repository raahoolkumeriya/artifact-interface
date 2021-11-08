"""Artifact Validation Class"""

import re
import logging
from interface.utilities.load_config import ArtifactConfig
from interface.common.constants import ArtifactDetails as ART


class Validations():
    """
    Validation for standard Deployment package
    """
    def __init__(self, artf_config: ArtifactConfig) -> None:
        self.artf_config = artf_config
        self.regex_list = self.artf_config.regexlist
        self._logger = logging.getLogger(__name__)
        self.match = []

    def check_artifact_string(self, arg: str) -> bool:
        """
        Return bool for valid artifact name

        :param arg: Package string as Input

        :returns:
            bool
                ``True`` if validation pass
                ``False`` if validation failed
        """
        for i in self.regex_list:
            self.match.append(bool(re.compile(i).match(str(arg))))
        if True in self.match:
            self._logger.info("Validation Cleared: Artifact name in standrds")
            return True
        else:
            self._logger.info("Validation Cleared: Artifact name in standrds")
            return False

    def get_correct_artifact_name(self, arg: str) -> str:
        """
        Return final arrtifact name base on package name

        :param arg: Package string as Input

        :returns:
            Artifact name
        """
        if ART.ART_EXT_TRZ.value in arg:
            self._logger.info("Validation cleared .tar.gz removed")
            return arg.strip(ART.ART_EXT_TRZ.value)
        elif ART.ART_EXT_TAR.value in arg:
            self._logger.info("Validation cleared .tar removed")
            return arg.strip(ART.ART_EXT_TAR.value)
        elif ART.ART_EXT_TGZ.value in arg:
            self._logger.info("Validation cleared .tgz removed")
            return arg.strip(ART.ART_EXT_TGZ.value)
        else:
            logging.info(f"Validation supress: {arg}")
            return arg

    def return_artifact_name(self, arg: str) -> str:
        """
        Return valid Artifact name

        :param arg: Base Artifact name

        :returns: 
           Tar gzip artifact name
        """
        return self.get_correct_artifact_name(arg) + ART.ART_EXT_TRZ.value

    def get_version_name(self, arg: str) -> str:
        """
        Return Version name from artifact
        :param arg: Base Artifact name

        :returns:
            extract version name from Artifact abse version
        """
        return re.findall(r'\d+.\d+.\d+.\d+', arg)[0]
