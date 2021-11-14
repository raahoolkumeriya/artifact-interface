"""Running the Interface Application"""

import os
import streamlit as st
from interface.streamlit_UI.multipage import MultiPage
from interface.pages import homepage, create_package ,artifact_action,\
    restore_old, guidelines, common_utilities, to_do_tasks, commit_utilities
from interface.common.constants import StreamlitSetup


def check_environment_var():
    MANDATORY_ENV_VARS = ['REMOTE_SER_PASSWORD', 'JIRA_AUTH_TOKEN', 'SLACK_API_TOKEN']
    for var in MANDATORY_ENV_VARS:
        if var not in os.environ:
            raise EnvironmentError(f"Failed because {var} is not set.")
            
            
def main():
    """Application Entry Point"""
    # Initial page config
    st.set_page_config(
        page_title=StreamlitSetup.APPLICATION_TITLE.value,
        page_icon='📦',
        layout="wide",
        initial_sidebar_state="expanded")

    st.markdown(StreamlitSetup.HIDE_STREAMLIT_STYLE.value, unsafe_allow_html=True)
    st.markdown(StreamlitSetup.PAGE_SETUP.value, unsafe_allow_html=True)

    st.sidebar.header("Artifact InterFace `ʕ•́ᴥ•̀ʔ`")
    
    # Create an instance of the app
    app = MultiPage()

    # Add all your applications (pages) here
    app.add_page("Dashboard", homepage.app)
    app.add_page("Develop Package", create_package.app)
    app.add_page("Process Artifact", artifact_action.app)
    app.add_page("Restore Artifacts", restore_old.app)
    app.add_page("Commit Utilities", commit_utilities.app)
    app.add_page("Configuration setup", common_utilities.app)
    app.add_page("Guide Line", guidelines.app)
    # app.add_page("TODO-Enhancements", to_do_tasks.app)

    # The main app
    app.run()

    st.sidebar.subheader("`ツ` Contribute")
    col1, col2, col3 = st.sidebar.columns(3)
    col1.markdown(StreamlitSetup.GITHUB_STAR.value, unsafe_allow_html=True)
    col2.markdown(StreamlitSetup.GITHUB_WATCH.value, unsafe_allow_html=True)
    col3.markdown(StreamlitSetup.GITHUB_FORK.value, unsafe_allow_html=True)
    st.sidebar.subheader("`ツ` Connect")
    st.sidebar.markdown(StreamlitSetup.SOCIAL.value, unsafe_allow_html=True)
    

if __name__ == "__main__":
    check_environment_var()
    main()    
    