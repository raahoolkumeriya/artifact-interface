"""
File to store constants
"""
from enum import Enum

class ErrorCodesMessages(Enum):
    """
    formation for ErrorCodesMessages class
    """
    USER_PASS_ERR = 'Username or Password/auth token Error!'
    PKG_NAME_ERR = 'Package does not meet with standards!'


class ArtifactDetails(Enum):
    """
    Artifact Extension
    """
    ART_EXT_TRZ = ".tar.gz"
    ART_EXT_TGZ = ".tgz"
    ART_EXT_TAR = ".tar"


class TemplateDetails(Enum):
    """
    Template features for Creating Artifact
    """
    pass

class StreamlitSetup(Enum):
    """
    Streamlit Setup
    """
    HIDE_STREAMLIT_STYLE = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:'copyrights © 2021 rahul.kumeriya@outlook.com';
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 10px;
                top: 12px;
            }
            </style>
            """
    APPLICATION_TITLE = "Aartifact Development & Delivery Interface"
    DASHBOARD_FEATURES = f"""
        - Stremaline execution
        - TTD
        - Deployment Template
        - Background ticket logging
        """
    DEVELOP_ART_FEATURES = f"""
    - Latest remote tag as latest artifact development version
    - Unix and Database category artifact
    - Deployment templates with dynamic forms
    - Rollback/Backout packages 
    """
    EXECUTE_ART_FEATURES = f"""
    - Test artifact w.r.t different environment mode
    - Commit, logging, deployment, notify at one place 
    - Clean and Test logs
    - Failed Log hault the successive actions
    """
    RESTORE_ART_FEATURES = f"""
    - Quick filter on local repository for all files
    - Space seprated artifact digit filtering 
    - Upload artifact form local repository to Remote server
    - Create Vesion for filtered artifact
    """
    COMMIT_ART_FEATURE = """
    - Commit artifact with standard process
    - Filter out Commit statistics with between analysis
    """
    
    PADDING = 3
    PAGE_SETUP = f""" <style>
            .reportview-container .main .block-container{{
                padding-top: {PADDING - 2}rem;
                padding-right: {PADDING}rem;
                padding-left: {PADDING}rem;
                padding-bottom: {PADDING}rem;
            }} </style> """
    # Github button size display
    BUTTON_SIZE = 'count=true&size=large&v=2'
    # Github button display on sidebar SETUP
    REPO_URL = "https://ghbtns.com/github-btn.html?user=raahoolkumeriya&repo=artifact-interface"
    FORMAT_BUTTON = 'frameborder="0" scrolling="0" width="170" height="30" title="GitHub"'
    GITHUB_BTN = f'<iframe src="{REPO_URL}&{BUTTON_SIZE}" {FORMAT_BUTTON}></iframe>'
    GITHUB_STAR = f'<iframe src="{REPO_URL}&type=star&{BUTTON_SIZE}" {FORMAT_BUTTON}></iframe>'
    GITHUB_WATCH = f'<iframe src="{REPO_URL}&type=watch&{BUTTON_SIZE}" {FORMAT_BUTTON}></iframe>'
    GITHUB_FORK = f'<iframe src="{REPO_URL}&type=fork&{BUTTON_SIZE}" {FORMAT_BUTTON}></iframe>'

    SOCIAL = f'''
    <p align="left"> 
        <a href="https://github.com/raahoolkumeriya" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/github.svg" alt="raahoolkumeriya" height="30" width="40" /></a>
        <a href="https://twitter.com/kumeriyaRahul" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/twitter.svg" alt="kumeriyaRahul" height="30" width="40" /></a>
        <a href="https://linkedin.com/in/rahulkumeriya" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/linkedin.svg" alt="rahulkumeriya" height="30" width="40" /></a>
    </p>'''