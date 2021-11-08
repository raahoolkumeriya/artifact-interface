import os
import yaml
import logging
from interface.utilities.load_config import RemoteServerConfig, RepositoryConfig,\
    SlackConfig, JiraConfig, ArtifactConfig, UdeployConfig

def load_configuration():
    # Configurtion setup
    config = os.path.join( os.path.abspath('.'), "configs", "app_config.yml")
    config = yaml.safe_load(open(config))
    
    log_config = config['logging']
    logging.config.dictConfig(log_config)

    # reading remote server configuration
    serv_config = RemoteServerConfig(**config['server'])
    # reading jira configuration
    jira_config = JiraConfig(**config['jira'])
    # reading jira configuration
    repo_config = RepositoryConfig(**config['repository'])
    # Reading slack configration
    slack_config = SlackConfig(**config['slack'])
    # Reading artifact configration
    artf_config = ArtifactConfig(**config['artifact'])
    # Rreading Udeploy configuration 
    udep_Config = UdeployConfig(**config['udeployspace'])

    return {
            "serv_config": serv_config,
            "jira_config": jira_config, 
            "repo_config": repo_config,
            "slack_config": slack_config,
            "artf_config": artf_config,
            "udep_config": udep_Config
            }