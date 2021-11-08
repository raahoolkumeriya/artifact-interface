import os
import logging
from pandas.io.pickle import read_pickle
import yaml
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import logging.config
from interface.common.constants import StreamlitSetup
from interface.utilities.git_client import GitClientUtility
from interface.utilities.load_config import RepositoryConfig, ArtifactConfig
from interface.streamlit_UI.dashboard import ProcessGitLocal


# def read_pickle_file(filename, repo_config, artf_config):
#     file_name = os.path.join(os.path.abspath('statics'), f'{filename}.pkl')
#     if os.path.exists(file_name):
#         read_file = pd.read_pickle(file_name)
#         return read_file
#     else:
#         ProcessGitLocal(repo_config, artf_config).formation_of_data()
#         read_file = pd.read_pickle(file_name)
#         return read_file


def sns_chart_snippets(data_frame, column, category):
    ax = sns.barplot(
            x = data_frame[column],
            y = data_frame['commit_count'],
            palette='pastel', ci=None)
    ax.set(title=f'{category}ly Commit vs Commit Count', xlabel=f'Commit {category}',
        ylabel='Commit Counts')
        

def app():
    
    # Configurtion setup
    config = os.path.join( os.path.abspath('.'), "configs", "app_config.yml")
    config = yaml.safe_load(open(config))
    
    log_config = config['logging']
    logging.config.dictConfig(log_config)

    # reading repository configuration
    repo_config = RepositoryConfig(**config['repository'])
    # reading artifact configuration
    artf_config = ArtifactConfig(**config['artifact'])

    gitClient = GitClientUtility(repo_config, artf_config)
    analysis = ProcessGitLocal(repo_config, artf_config)
    construct_df = analysis.construct_dataframe()

    df_dict = analysis.formation_of_data(construct_df)

    dataframe = df_dict.get('dataframe')
    date_dataframe = df_dict.get('date_dataframe')
    hour_dataframe = df_dict.get('hour_dataframe')
    month_dataframe = df_dict.get('month_dataframe')
    year_dataframe = df_dict.get('year_dataframe')
    
    st.subheader('🔠 Repository statistics')
    
    progress_bar = st.sidebar.progress(0)

    with st.form("home_page_stats_form"):
        c1, c2, c3, c4 = st.columns(4)
        h_style = "style='text-align: center; color: blue; font-size: 70px'"
        p_style = "style='text-align: center;'"
        with c1:
            number = dataframe.iat[0, 1]
            st.markdown(f"<h1 {h_style}> {number}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p {p_style}>Total Commits</p>", unsafe_allow_html=True)
        with c2:
            number = dataframe.iat[0, 2]
            st.markdown(f"<h1 {h_style}'> {number}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p {p_style}>Total Authors</p>", unsafe_allow_html=True)
        with c3:
            number = dataframe.iat[0, 0]
            st.markdown(f"<h1 {h_style}'>{number}</h1>", unsafe_allow_html=True)
            st.markdown(
                f"<p {p_style}>Total Artifacts</p>", unsafe_allow_html=True)
        with c4:
            number = dataframe.iat[0, 3]
            st.markdown(f"<h1 {h_style}>{number}</h1>", unsafe_allow_html=True)
            st.markdown(
                f"<p {p_style}>Current Month Commit</p>", unsafe_allow_html=True)
        if st.form_submit_button(""):
            pass

    progress_bar.progress(25)

    st.subheader('\n 📊 Repository Insights with graph plots:')

    # Graph Plots        
    f = plt.figure(figsize=(5, 4))
    gs = f.add_gridspec(2, 2)
    sns.set_context("paper")
    sns.set(font_scale=0.5) 

    with sns.axes_style("darkgrid"):
        ax = f.add_subplot(gs[0, 0])
        sns_chart_snippets(date_dataframe, 'commit_date', 'Date-')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    with sns.axes_style("darkgrid"):
        ax = f.add_subplot(gs[0, 1])
        sns_chart_snippets(hour_dataframe, 'commit_hour', 'Hour')
    
    with sns.axes_style("darkgrid"):
        ax = f.add_subplot(gs[1, 0])
        sns_chart_snippets(year_dataframe, 'commit_year', 'Year')

    with sns.axes_style("darkgrid"):
        ax = f.add_subplot(gs[1, 1])
        sns_chart_snippets(month_dataframe, 'commit_month', 'Month')

    f.tight_layout()
    st.pyplot(f)

    progress_bar.progress(75)
    
    # Sidebar Repository Controls
    col1, col2, col3 = st.sidebar.columns([1,1,1])
    if col1.button("Refresh Dash Board"):
        analysis = ProcessGitLocal(repo_config, artf_config)
        construct_df = analysis.construct_dataframe()
        analysis.formation_of_data(construct_df)
        
    if col2.button('Pull Remote Changes'):
        gitClient.git_pull_to_sync()

    if col3.button('Push Local Changes'):
        gitClient.git_push_to_sync()

    st.sidebar.subheader("`ツ` Features")
    st.sidebar.markdown(StreamlitSetup.DASHBOARD_FEATURES.value, unsafe_allow_html=True)

    progress_bar.progress(100)
    