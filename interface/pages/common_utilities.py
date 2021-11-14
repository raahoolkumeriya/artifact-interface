import os
import yaml
import json
import logging
import streamlit as st
from interface.utilities.remote_client import RemoteClientUtility
from interface.utilities.git_client import GitClientUtility
from interface.utilities.load_config import SlackConfig, JiraConfig, RemoteServerConfig, RepositoryConfig, ArtifactConfig, UdeployConfig
from interface.utilities.uDeployClient import UdeployUtilityClient


environment_config = os.path.join(
    os.path.abspath('.'),
    "configs", "template.json")


# Function to add to JSON
def write_json(new_data, filename=environment_config):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["templates"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def app():
    logging.info("CONFIGURATION ZONE")
    st.subheader("⚙️ Synchronize and Configuration")
    
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
    # Reading artifact configration
    udep_config = UdeployConfig(**config['udeployspace'])


    remoteClient = RemoteClientUtility(serv_config,repo_config)
    gitClient = GitClientUtility(repo_config, artf_config)

    load_template = st.checkbox('Test and Load Templates')

    if load_template is True:
        if st.button("Fetch template list"):
            # Configurtion setup
            output = remoteClient.connect_server(
                f'ls -1rt {serv_config.processor}/TEMPLATES')
            updated_list = list(map(lambda s: s.strip(), output[0]))
            st.write(updated_list)
            # print(updated_list)

    template_add = st.checkbox("❌ Do you want to add new template ?")

    if template_add is True:
        st.error('''Caution:
        -   Template Name should be in CAPS Letters Only [ 8-12 Letter ]
        -   Enter Parameter description
                e.g., Enter directory Path
                e.g., Enter script name
        ''')

        param1 = param2 = param3 = ""

        template_name = st.text_input(
            "Enter Template Name [ CAPS _ ] 8 to 10 letter only")
        param1 = st.text_input("Enter discription of First Parameter")
        need_paramter2 = st.checkbox("Need Second Parameter")
        if need_paramter2 is True:
            param2 = st.text_input("Enter discription of Second Parameter")
            need_paramter3 = st.checkbox("Need Thrid Parameter")
            if need_paramter3 is True:
                param3 = st.text_input("Enter discription of Third Parameter")
            else:
                param3 = ""
        else:
            param2 = ""

        new = {
                "template_name": template_name,
                "param1": param1,
                "param2": param2,
                "param3": param3
            }

        if st.button("ADD NEW TEMPLATE"):
            write_json(new)

    load_env_template = st.checkbox('❌ Load Environment templates')

    if load_env_template is True:
        dict1 = {}
        with open(environment_config) as json_file:
            dict1 = json.load(json_file)
        dict2 = {}
        for i in dict1["templates"]:
            dict2[i["template_name"]] = i
        st.write(dict2)

    delete_tag = st.checkbox('Delete Local-Remote Tag')

    if delete_tag is True:
        tag_name = st.text_input("Enter Tag details [10.XX.XXX.XXXX]")
        if st.button('Delete Tag'):
            st.info(gitClient.git_delete_tag_local(tag_name))
            st.info(gitClient.git_delete_tag_remote(tag_name))

    show_mongo_artifacts = st.checkbox("Mongo ATLAS Created Version")

    if show_mongo_artifacts is True:
        st.json(UdeployUtilityClient(udep_config).get_list_of_version())