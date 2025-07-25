import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import json
import zipfile
from io import BytesIO
from services.metadata_manager import MetadataManager
from utils.helpers import generate_filename, generate_timestamped_zip_name
from utils.logger import logger

# Load vocabulary
vocab_path = Path("config") / "vocabulary.json"
vocab = json.loads(vocab_path.read_text(encoding="utf-8"))

# Load and validate metadata
all_resources = []
for raw in MetadataManager.backend.list_all():
    try:
        all_resources.append(MetadataManager._from_jsonld(raw))
    except Exception as e:
        logger.warning(f"Skipped malformed resource: {e}")

# Match functions
def any_match(selected, available):
    return not selected or bool(set(selected) & set(available))

def all_match(selected, available):
    return not selected or set(selected).issubset(set(available))

MATCH_MODE = "ALL"  # or "ANY"
match_fn = all_match if MATCH_MODE == "ALL" else any_match

# Initialize session state if needed
if "filters_initialized" not in st.session_state:
    st.session_state.filters_initialized = True
    st.session_state.update({
        "filter_subjects": [],
        "filter_keywords": [],
        "filter_education": [],
        "filter_methods": [],
        "filter_types": [],
        "filter_formats": [],
        "admin_mode": False,
        "pagination_page": 1,
        "selected_entries": set(),
        "select_all": False
    })

# Sidebar header
with st.sidebar:
    st.header("Filters")

# Partial filtering function to support dynamic option reduction
def partial_matches(resource):
    return (
        match_fn(st.session_state.filter_subjects, resource.subject)
        and match_fn(st.session_state.filter_keywords, resource.keywords)
        and match_fn(st.session_state.filter_education, resource.educational_level)
        and match_fn(st.session_state.filter_methods, resource.instructional_method)
        and match_fn(st.session_state.filter_types, resource.learning_resource_type)
        and match_fn(st.session_state.filter_formats, resource.format)
    )

# Filter resources based on current state selections
filtered_for_options = list(filter(partial_matches, all_resources))

# Dynamically extract filter options from partially filtered resources
def extract_unique(attr):
    return sorted({val for res in filtered_for_options for val in getattr(res, attr)})

available_subjects = extract_unique("subject")
available_keywords = extract_unique("keywords")
available_education = extract_unique("educational_level")
available_methods = extract_unique("instructional_method")
available_types = extract_unique("learning_resource_type")
available_formats = extract_unique("format")

# Now display the widgets
with st.sidebar:
    selected_subjects = st.multiselect("Subjects", available_subjects, default=st.session_state.filter_subjects, key="filter_subjects")
    selected_keywords = st.multiselect("Keywords", available_keywords, default=st.session_state.filter_keywords, key="filter_keywords")
    selected_education = st.multiselect("Education Level", available_education, default=st.session_state.filter_education, key="filter_education")
    selected_methods = st.multiselect("Instructional Method", available_methods, default=st.session_state.filter_methods, key="filter_methods")
    selected_types = st.multiselect("Resource Type", available_types, default=st.session_state.filter_types, key="filter_types")
    selected_formats = st.multiselect("Format", available_formats, default=st.session_state.filter_formats, key="filter_formats")
    admin_mode = st.checkbox("Admin Mode", value=False, key="admin_mode")

# Final filter for main results
def matches(resource):
    return (
        match_fn(selected_subjects, resource.subject)
        and match_fn(selected_keywords, resource.keywords)
        and match_fn(selected_education, resource.educational_level)
        and match_fn(selected_methods, resource.instructional_method)
        and match_fn(selected_types, resource.learning_resource_type)
        and match_fn(selected_formats, resource.format)
    )

filtered = list(filter(matches, all_resources))
total = len(filtered)

# Pagination
page_size = 50
page_num = st.sidebar.number_input("Page", min_value=1, max_value=max(1, (total - 1) // page_size + 1), value=1, key="pagination_page")
offset = (page_num - 1) * page_size
paginated = filtered[offset : offset + page_size]

st.title("Search & Explore Metadata")
st.subheader(f"Showing {len(paginated)} of {total} matching resources")

# Select all / none
select_all = st.checkbox("Select all on this page", value=False)
if select_all:
    st.session_state.selected_entries = {res.id for res in paginated}
else:
    st.session_state.selected_entries = set()

# Display Results
for res in paginated:
    is_selected = res.id in st.session_state.selected_entries
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        if st.checkbox("", key=f"select_{res.id}", value=is_selected):
            st.session_state.selected_entries.add(res.id)
        else:
            st.session_state.selected_entries.discard(res.id)
    with col2, st.expander(f"{res.title} ({res.date_modified})"):
        st.markdown(f"**ID**: `{res.id}`")
        st.markdown(f"**Subjects**: {', '.join(res.subject)}")
        st.markdown(f"**Keywords**: {', '.join(res.keywords)}")
        st.markdown(f"**Education Level**: {', '.join(res.educational_level)}")
        st.markdown(f"**Instructional Method**: {', '.join(res.instructional_method)}")
        st.markdown(f"**Type**: {', '.join(res.learning_resource_type)}")
        st.markdown(f"**Format**: {', '.join(res.format)}")
        st.markdown(f"**License(s)**: {', '.join(res.license)}")
        st.markdown(f"**Identifier**: {res.identifier}")

        filename = generate_filename(res) + ".jsonld"
        jsonld_path = Path("data/metadata") / filename
        if jsonld_path.exists():
            with open(jsonld_path, "r", encoding="utf-8") as f:
                content = f.read()
                st.download_button("Download JSON-LD", content, file_name=filename, mime="application/ld+json")
                if st.button(f"Show JSON for {res.id}", key=f"show_{res.id}"):
                    st.code(content, language="json")

        if admin_mode:
            st.warning("Admin edit mode is planned but not yet implemented.")

# Zip selected entries
if st.session_state.selected_entries:
    zip_name = generate_timestamped_zip_name()
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for res in filtered:
            if res.id in st.session_state.selected_entries:
                filename = generate_filename(res) + ".jsonld"
                file_path = Path("data/metadata") / filename
                if file_path.exists():
                    zf.write(file_path, arcname=filename)
    st.download_button("Download Selected as ZIP", data=buffer.getvalue(), file_name=zip_name, mime="application/zip")
    st.info(f"Downloaded ZIP file: {zip_name}")

if not filtered:
    st.info("No results found. Adjust the filters in the sidebar.")
