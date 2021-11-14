import logging
import streamlit as st
from interface.common.validation import Validations
from interface.utilities.remote_client import RemoteClientUtility
from interface.utilities.jira_client import JiraRESTClient
from interface.utilities.git_client import GitClientUtility
from interface.utilities.slack_client import SlackConnect
from interface.pages.configration import load_configuration
from interface.common.constants import StreamlitSetup
from interface.utilities.uDeployClient import UdeployUtilityClient
from interface.streamlit_UI.animation import vanishing_logs


def app():
    """
    Artifact action includes:
    - Testing Artifact via shell script
    - Code commit to repository
    - Deploy artifact
    - Comment Jira
    """
    logging.info("Interface : ARTIFACT ACTION ZONE")
    st.subheader("🧪 Test Artifact \ Code Commit \ Deploy")

    config = load_configuration()

    progress_bar = st.sidebar.progress(0)
    
    st.sidebar.subheader("`ツ` Features")
    st.sidebar.markdown(StreamlitSetup.EXECUTE_ART_FEATURES.value, unsafe_allow_html=True)

    linuxClient = RemoteClientUtility(config['serv_config'], config['repo_config'])
    gitClient = GitClientUtility(config['repo_config'], config['artf_config'])
    jiraClient = JiraRESTClient(config['jira_config'])
    validate = Validations(config['artf_config'])
    slackClient = SlackConnect(config['slack_config'])
    udeployClient = UdeployUtilityClient(config['udep_config'])

    env_Choices = config['artf_config'].environment

    col1, col2, col3 = st.columns(3)
    jira_ticket = col1.text_input("Jira Ticket*").strip()
    package_name = col2.text_input("Test Package Name*").strip()
    environment = col3.selectbox(
        "Select template",
        options=list(env_Choices.keys()),
        format_func=lambda x: env_Choices[x])

    comment_jira = st.checkbox('📚 Want to comment logs to jira ?')
    code_commit = st.checkbox('🗜 Want to Code commit ?')
    if code_commit is True:
        commit_message = st.text_input("Enter Commit Message*").strip()
    trigger_process = st.checkbox('🌀 Want to run Udeploy Process ?')
    trigger_mongo_call = st.checkbox('🌀 Want to run MONGO-FASAPI create version Process ?')
    slack_post = st.checkbox('📨 Want to post message to SLACK ?')
    
    log_empty = st.empty()

    if st.button("Test Package"):
        if package_name:
            if validate.get_correct_artifact_name(package_name):
                artifact = validate.return_artifact_name(package_name)
                version_name = validate.get_version_name(artifact)
                progress_bar.progress(10)
                if environment:
                    output_pkg = linuxClient.execute_package_utility(
                        package_name, 'test', environment)[0]
                    string = " "
                    output = string.join(output_pkg)
                    progress_bar.progress(50)
                    st.text(output)
                                    
                    if "FAIL" in output:
                        progress_bar.progress(100)
                        st.error("Testing failed......")
                    else:
                        if comment_jira is True:
                            progress_bar.progress(30)
                            updated = jiraClient.update_comment(
                                jira_ticket, f"TEST Result: {output}")
                            log_empty.info(f"Jira updated {updated}")

                        if code_commit is True:
                            progress_bar.progress(50)
                            log_empty.info(linuxClient.download_artifact_to_local(
                                artifact))
                            gitClient.git_delete_tag_local(version_name)
                            gitClient.git_delete_tag_remote(version_name)
                            value = gitClient.git_push_artifact(
                                artifact, commit_message, jira_ticket)
                            message = f"""
                            |**Repository Details**|\
                                [Download](https://bitbucket.org/raahoolkumeriya/repo-adhoc-space/src/master/{artifact})|
                            |-------------|--------------------------|
                            | Commit id   |`{value.get('commit_id')}`|
                            | Tag Version |`{value.get('tag_name')}` |
                            """
                            jiraClient.update_comment(jira_ticket, message)
                            log_empty.info(value)

                        if trigger_process is True:
                            progress_bar.progress(70)
                            process = linuxClient.run_udeploy_process(
                                artifact, version_name)
                            st.info(process)
                            udeploy_message = f"""
                            |**Deployment Package Details**|\
                                [{jira_ticket}](https://codelocked.atlassian.net/browse/{jira_ticket})|
                            |-------------|----------------|
                            |Artifact Name| `{artifact}`   |
                            |Version Name |`{version_name}`|
                            """
                            st.markdown(udeploy_message)
                            jiraClient.update_comment(
                                jira_ticket, udeploy_message)
                        
                        if trigger_mongo_call is True:
                            result = udeployClient.create_version(artifact, version_name)
                            st.info(result)
                            jiraClient.update_comment(jira_ticket, result)
                            progress_bar.progress(70)

                        if slack_post is True:
                            slack = slackClient.post_in_channel(
                                artifact, version_name, jira_ticket)
                            log_empty.success(
                                {
                                    "Url": "https://app.slack.com/client/TNYSS0150/CPDSD2B4N/user_profile/UP57HA3C1",
                                    "status": slack})
                            progress_bar.progress(100)
            else:
                vanishing_logs(log_empty, 'error', "Package name dosen't meet the standards")
                progress_bar.progress(100)
        else:
            vanishing_logs(log_empty, 'error', "Enter test Package to proceed")
            progress_bar.progress(100)    
    