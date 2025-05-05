# ui/search_entries.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from services.metadata_manager import MetadataManager
from models.resource_metadata import ResourceMetadata

st.set_page_config(page_title="Search Metadata Entries", layout="wide")
st.title("Search NOMAD Training Resources")

entries = MetadataManager.list_metadata()

# Admin toggle
admin_mode = st.sidebar.toggle("Admin Mode", value=False)

# Filtering UI
subjects = sorted(set(s for entry in entries for s in entry.subject))
keywords = sorted(set(k for entry in entries for k in entry.keywords))

col1, col2 = st.columns(2)
with col1:
    selected_subjects = st.multiselect("Filter by Subject", options=subjects)
with col2:
    selected_keywords = st.multiselect("Filter by Keyword", options=keywords)

# Filter results
filtered = []
for entry in entries:
    if selected_subjects and not set(entry.subject) & set(selected_subjects):
        continue
    if selected_keywords and not set(entry.keywords) & set(selected_keywords):
        continue
    filtered.append(entry)

# Display results
st.markdown(f"### {len(filtered)} Matching Entries")

for entry in filtered:
    with st.expander(entry.title):
        st.write(f"**ID**: {entry.id}")
        st.write(f"**Description**: {entry.description}")
        st.write(f"**Subjects**: {', '.join(entry.subject)}")
        st.write(f"**Keywords**: {', '.join(entry.keywords)}")
        st.write(f"**Modified**: {entry.date_modified}")
        st.write(f"**Identifier**: {entry.identifier}")

        if admin_mode:
            st.markdown("---")
            st.markdown("#### Admin Tools")
            if st.button(f"Delete {entry.id}"):
                MetadataManager.delete_metadata(entry.id)
                st.success(f"Deleted {entry.id}")
                st.experimental_rerun()

            if st.button(f"Edit {entry.id}"):
                st.session_state.editing_entry = entry.id
                st.switch_page("main_app.py")
