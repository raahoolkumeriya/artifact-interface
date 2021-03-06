import streamlit as st

release_notes = """

## Artifact Development & Delivery Interface  ๐ฆ ๐จโ๐ป ๐ ๐  
### `Version 2.0.0`

---
### ๐น๏ธ Highlights

**Features**
- ๐ Create `Unix/Database/Windows` deployment scripts
- ๐ `Template` feature for recurring tasks
- ๐ `Streamline process` of deployment
- ๐ `Logging jira tickets`

**Update configuration file details**
- ๐งถ Application remote server details for package development and processing part
- ๐งถ Jira project
- ๐งถ Local/Remote repository details
- ๐งถ Slack notification group details

**Future Enhancement**
- ๐ jFrog Artifactory integration
- ๐ Development of template feature at GUI level
"""

def app():
    st.write(release_notes)
