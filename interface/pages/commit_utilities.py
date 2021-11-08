import logging
import streamlit as st
from interface.common.validation import Validations
from interface.streamlit_UI.dashboard import ProcessGitLocal
from interface.utilities.remote_client import RemoteClientUtility
from interface.utilities.git_client import GitClientUtility
from interface.pages.configration import load_configuration
from interface.common.constants import StreamlitSetup
from interface.streamlit_UI.animation import vanishing_logs


def app():
    logging.info("COMMIT ACTION ZONE")
    st.subheader("🎁 Code Commit artifact")

    config = load_configuration()

    progress_bar = st.sidebar.progress(0)
    
    st.sidebar.subheader("`ツ` Features")
    st.sidebar.markdown(StreamlitSetup.COMMIT_ART_FEATURE.value, unsafe_allow_html=True)

    gitClient = GitClientUtility(config['repo_config'], config['artf_config'])
    linuxClient = RemoteClientUtility(config['serv_config'], config['repo_config'])
    validate = Validations(config['artf_config'])
    
    with st.form("commit_artifact_form"):
        display_filed = st.empty()
        col1, col2 = st.columns([2,2])
        jira_ticket = col1.text_input("Jira Ticket*").strip()
        package_name = col2.text_input(
            "Commit Package Name*").strip()
        commit_message = st.text_input("Enter commit message")
        
        if package_name:
            progress_bar.progress(20)
            if validate.get_correct_artifact_name(package_name):
                progress_bar.progress(30)
                artifact = validate.return_artifact_name(package_name)
                progress_bar.progress(40)
                version_name = validate.get_correct_artifact_name(artifact)

        if st.form_submit_button("Commit Artifact"):
            display_filed.info(linuxClient.download_artifact_to_local(
                artifact))
            if commit_message is None:
                commit_message = f"ICA: Artifact {artifact} added"
            progress_bar.progress(50)
            # Delete tags override task
            vanishing_logs(
                display_filed, 'info',
                gitClient.git_delete_tag_local(version_name))
            vanishing_logs(
                display_filed, 'info',
                gitClient.git_delete_tag_remote(version_name))
            progress_bar.progress(60)
            value = gitClient.git_push_artifact(
                artifact, commit_message, jira_ticket)
            progress_bar.progress(80)
            vanishing_logs(
                display_filed, 'success', value)
            progress_bar.progress(100)

    st.write("\n")

    st.subheader("📈 Commit and File count analaysis between dates")
    with st.form("stats_form"):
        progress_bar.progress(0)
        analysis = ProcessGitLocal(config['repo_config'], config['artf_config'])
        df = analysis.construct_dataframe()
        progress_bar.progress(20)

        col1, col2 = st.columns(2)
        start_date = str(col1.date_input("Select Start date"))
        end_date = str(col2.date_input("Select End date"))
        progress_bar.progress(20)
        if st.form_submit_button("Filter data and get commit Analysis"):
            st.write(analysis.between_date_analysis(
                df, start_date, end_date))
            progress_bar.progress(100)
        