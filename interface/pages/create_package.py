import logging
import streamlit as st
import os
import yaml
from interface.utilities.load_config import RepositoryConfig,\
    RemoteServerConfig, SlackConfig, JiraConfig, ArtifactConfig,\
    UdeployConfig
from interface.utilities.remote_client import RemoteClientUtility
from interface.utilities.jira_client import JiraRESTClient
from interface.utilities.package_util import PackageVersionIncrement,\
    LatestPackage
from interface.common.constants import StreamlitSetup
from interface.streamlit_UI.animation import vanishing_logs
from interface.utilities.uDeployClient import UdeployUtilityClient


def genereate_data_string(
    template_name: str,
    package_name: str,
    script_name: str,
    param1: str,
    param2: str,
    param3: str
        ) -> str:
    return {
                "template_name": template_name,
                "pkg_directory": package_name,
                "script_name": script_name.strip(),
                "pkg_details": {
                            "__parameter_one__": param1,
                            "__parameter_two__": param2,
                            "__parameter_three__": param3
                      }
        }


def app():
    """
    Create Artifact utilities task
    """
    st.subheader(":symbols: Develop Package \ Use Script Templates")
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

    progress_bar = st.sidebar.progress(0)

    display = st.sidebar.empty()
    display.info("Running background processes!")
    # Get latest Artifact
    
    try:
        pkg = LatestPackage(repo_config, serv_config, artf_config).get_latest_local()
        progress_bar.progress(5)
    except Exception:
        logging.error("Failed to load remote value")
        pkg = LatestPackage(repo_config, serv_config, artf_config).get_latest_local()
        progress_bar.progress(5)

    remote_name = f"{artf_config.artifact_base}.{pkg}"
    package_name = PackageVersionIncrement().increment_package_ver(remote_name)

    full_pkg_dir = f"{serv_config.source}/{package_name}"
    display.button(package_name)

    st.sidebar.subheader("`ツ` Features")
    st.sidebar.markdown(StreamlitSetup.DEVELOP_ART_FEATURES.value, unsafe_allow_html=True)

    linuxClient = RemoteClientUtility(serv_config, repo_config)
    jiraClient = JiraRESTClient(jira_config)

    templates_Choices = artf_config.templatelist
    permission = artf_config.permissionlist
    
    jira_ticket = st.text_input("Jira Ticket*")
        
    flash_area = st.empty()

    script_name = "deployment_script.sh"
    category = st.checkbox('Database Category ?')
    rollback = st.checkbox('Want Backout package ?')


    if 'jira_ticket' not in st.session_state:
        st.session_state.jira_ticket = jira_ticket

    if category is False:
        template = st.selectbox(
            "Select template for deployment script OR skip",
            ['NO Template'] + templates_Choices)
        if template == "COPY_FILES":
            param1 = st.text_input("Directory Path [ /app/scripts ]")
            col1, col2 = st.columns(2)
            param2 = col1.text_input("File names [abc.sh xyz.ini ]")
            param3 = col2.selectbox("Permission for Files", permission)
        elif template == "CREATE_DIR":
            param1 = st.text_input("Directory Path [ /app/scripts ]")
            col1, col2 = st.columns(2)
            param2 = col1.text_input("New Directory Name")
            param3 = col2.selectbox("Permission for Files", permission)
        elif template in ['MONGO_QUERY', 'UPDATE_ENV_FILE']:
            param1 = "MONGO_QUERY"
            param2 = param3 = ""
        elif template == "ORACLE_QUERY":
            param1 = st.text_area("Enter Query")
            param2 = param3 = ""
        else:
            st.write('')
    else:
        get_query = st.text_area("Enter Query")

    col1, col2  = st.columns(2)

    if col1.button("Create Package"):
        if jira_ticket:
            # Validate Jira if its exists
            valid_jira = jiraClient.get_issue(jira_ticket)
            if jira_ticket == valid_jira:
                progress_bar.progress(10)
                if category is False:
                    # No-Template mode execution
                    if template != "NO Template":
                        progress_bar.progress(20)
                        output_pkg = linuxClient.execute_package_utility(
                            package_name, 'unix', script_name)
                        if output_pkg[0] != []:
                            st.success(output_pkg[0][0])
                            output_template = linuxClient.execute_template(
                                genereate_data_string(
                                    template,
                                    full_pkg_dir,
                                    script_name,
                                    param1, param2, param3)
                            )
                            st.info(f""" Package Output: {output_pkg[0][0]}""")
                            st.info(f""" Template Output: {output_template}""")
                            if rollback:
                                rollback_pkg = PackageVersionIncrement(
                                ).backout_package_ver(
                                    package_name)
                                linuxClient.execute_package_utility(
                                    package_name, 'upgrade', rollback_pkg)
                                rollback_string = genereate_data_string(
                                    'RESTORE_FILES',
                                    f"{full_pkg_dir}/backout.sh",
                                    param1, param2, param3)
                                logging.info(rollback_string)
                                linuxClient.execute_template(rollback_string)

                            comment_string = f"""
                                *Package Output* : {output_pkg[0][0]}\n
                                *Template Output*: {output_template}
                            """
                            jiraClient.update_comment(
                                jira_ticket,
                                comment_string)
                            progress_bar.progress(100)    
                        else:
                            st.error(output_pkg[1][0])
                            progress_bar.progress(100)
                    else:
                        # Template mode execution
                        progress_bar.progress(50)
                        output_pkg = linuxClient.execute_package_utility(
                            package_name, 'unix', script_name)
                        if output_pkg[0] != []:
                            st.success(output_pkg[0][0])
                            jiraClient.update_comment(
                                jira_ticket,
                                f"""Pakage Output: {output_pkg}""")
                        else:
                            st.error(output_pkg[1][0])
                            progress_bar.progress(100)
                else:
                    # Database Task    
                    script_name = 'deployment_script.sql'
                    output_pkg = linuxClient.execute_package_utility(
                        package_name, 'database', script_name)
                    progress_bar.progress(70)
                    if output_pkg[0] != []:
                        st.success(output_pkg[0][0])
                        query_string = genereate_data_string(
                            "QUERY", full_pkg_dir, script_name,
                            get_query, " ", " ")
                        logging.info(query_string)
                        output_template = linuxClient.execute_template(
                            query_string)
                        updated = jiraClient.update_comment(
                            jira_ticket, f"""Pakage Output: {output_pkg}""")
                        vanishing_logs(
                            flash_area, 'info',
                            f"{jira_ticket} Commented : {updated}")
                        progress_bar.progress(100)
                    else:
                        st.error(output_pkg[1][0])
                        progress_bar.progress(100)
            else:
                vanishing_logs(flash_area, 'error', valid_jira)
                progress_bar.progress(100)
        else:
            vanishing_logs(flash_area, 'error', 'Enter valid Jira ticket to proceed task')
            progress_bar.progress(100)


    with col2:
        with st.form("my_form"):
            st.write("Want to Create New Jira?")
            jira_summary = st.text_input("Enter short Summary for New Jira")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Create New Jira")
            if submitted:
                if jira_summary:
                    # ICJ --> Interface Created Jira
                    summary = f"ICJ: {jira_summary}"
                    desc = f"Jira created by Interface:\n Desciption: {jira_summary}"
                    st.success(jiraClient.create_issue(summary, desc))
                else:
                    st.error("Enter jira summary to create New Jira")
    