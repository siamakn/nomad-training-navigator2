# ui/search_and_explore.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import json
from services.metadata_manager import MetadataManager
from utils.logger import logger

st.set_page_config(page_title="Search Training Resources", layout="wide")
st.title("Search & Explore Resources")

# --- Sidebar filters ---
st.sidebar.header("Filters")
vocab_path = Path("config") / "vocabulary.json"
vocab = json.loads(vocab_path.read_text(encoding="utf-8"))

selected_subjects = st.sidebar.multiselect("Subjects", vocab["subjects"])
selected_keywords = st.sidebar.multiselect("Keywords", vocab["keywords"])
admin_mode = st.sidebar.checkbox("Admin Mode", value=False)

# --- Load metadata ---
all_resources = MetadataManager.list_metadata()

# --- Filtering logic ---
def matches_filters(resource):
    if selected_subjects:
        if not set(selected_subjects) & set(resource.subject):
            return False
    if selected_keywords:
        if not set(selected_keywords) & set(resource.keywords):
            return False
    return True

filtered_resources = list(filter(matches_filters, all_resources))

st.subheader(f"Found {len(filtered_resources)} matching resources")

# --- Display list ---
for resource in filtered_resources:
    with st.expander(f"{resource.title} ({resource.date_modified})"):
        st.markdown(f"**ID**: `{resource.id}`")
        st.markdown(f"**Description**: {resource.description}")
        st.markdown(f"**Subjects**: {', '.join(resource.subject)}")
        st.markdown(f"**Keywords**: {', '.join(resource.keywords)}")
        st.markdown(f"**License(s)**: {', '.join(resource.license)}")
        st.markdown(f"**Identifier**: {resource.identifier}")

        if admin_mode:
            st.info("Edit mode not implemented yet — but admin view enabled")

if not filtered_resources:
    st.info("Try adjusting the filters in the sidebar.")
