import streamlit as st

release_notes = """

## Artifact Development & Delivery Interface  📦 👨‍💻 🚚 🔘  
### `Version 2.0.0`

---
### 🕹️ Highlights

**Features**
- 💎 Create `Unix/Database/Windows` deployment scripts
- 💎 `Template` feature for recurring tasks
- 💎 `Streamline process` of deployment
- 💎 `Logging jira tickets`

**Update configuration file details**
- 🧶 Application remote server details for package development and processing part
- 🧶 Jira project
- 🧶 Local/Remote repository details
- 🧶 Slack notification group details

**Future Enhancement**
- 📍 jFrog Artifactory integration
- 📍 Development of template feature at GUI level
"""

def app():
    st.write(release_notes)
