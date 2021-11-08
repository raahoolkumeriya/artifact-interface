import os
import logging
import pandas as pd
import streamlit as st
from interface.utilities.remote_client import RemoteClientUtility
from interface.utilities.git_client import GitClientUtility
from interface.pages.configration import load_configuration
from interface.common.constants import StreamlitSetup
from interface.streamlit_UI.animation import vanishing_logs


def app():

    logging.info("App Execution: RESTORE ZONE:")
    # Upload the dataset and save as csv
    st.subheader("♻️ Restore Artifact \ Create Version")

    # Configurtion setup
    config = load_configuration()

    progress_bar = st.sidebar.progress(0)

    st.sidebar.subheader("`ツ` Features")
    st.sidebar.markdown(StreamlitSetup.RESTORE_ART_FEATURES.value, unsafe_allow_html=True)

    serverClient = RemoteClientUtility(config['serv_config'], config['repo_config'])
    gitClient = GitClientUtility(config['repo_config'], config['artf_config'])
   
    search_field = st.text_input(
        "Search Artifact with last digits e.g., 10 100 1234")
    regex_list = list(
        map(lambda x: f".{x}.tar.gz", list(search_field.split())))[::-1]

    list_dir_file = gitClient.get_file_from_local_repository()
    # Loading long of artifact form repository into Pandas Dataframe
    # for quick filtering
    df = pd.DataFrame(list_dir_file, columns=['Artifacts'])
    output = df[df['Artifacts'].str.contains(
        pat='|'.join(regex_list), regex=True)]
    # Converting dataFrame to series
    list_full_path = output['Artifacts'].to_list()
    my_choice = st.multiselect(
        'Multi-select Artifact',
        list(map(lambda x: os.path.basename(x), list_full_path)))

    # Storing Full path artifacts
    ready_files_list = []
    # Storing only file name
    ready_files_name = []
    for filename in list_full_path:
        if os.path.basename(filename) in my_choice:
            ready_files_list.append(filename)
            ready_files_name.append(os.path.basename(filename))

    flash_area = st.empty()

    if st.button("Upload to Server"):
        output = serverClient.upload_artifact_to_server(ready_files_list)
        if output is True:
            st.success("File uploaded to Server location")

    udeploy = st.checkbox("Do you want to Trigger Udeploy Process?")
    if udeploy is True:
        version_name = st.text_input(
            "Enter Unique Version Name [10.X.XX.XXX]"
        )
        if st.button("Create Version"):
            progress_bar.progress(50)
            if version_name:
                artifact_name = '\n'.join(ready_files_name)
                artifact_list = ' '.join(artifact_name.split('\n'))
                process_id = serverClient.run_udeploy_process(
                    artifact_name, version_name)
                st.info(process_id)
                if 'already exists' not in process_id[0][0]:
                    udeploy_comment = f"""
                    |**Deployment Package** |Details |
                    |--------------|-----------------|
                    | Artifact Name|`{artifact_list}`|
                    | Version Name |`{version_name}` |
                    """
                    st.markdown(udeploy_comment)
                    progress_bar.progress(100)
                else:
                    st.error(process_id[0][0])
                    progress_bar.progress(100)
            else:
                vanishing_logs(flash_area, 'error', "Version Name Required")
                progress_bar.progress(100)
