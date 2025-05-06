# ui/main_app.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from datetime import date, datetime
import json
from models.resource_metadata import ResourceMetadata
from services.metadata_manager import MetadataManager
from utils.helpers import generate_uuid, load_vocabulary, save_vocabulary, generate_filename
from utils.logger import logger

st.set_page_config(page_title="NOMAD Training Navigator", layout="wide")
st.title("NOMAD Training Navigator 2")

vocab = load_vocabulary()

# Session state init
if "relationships" not in st.session_state:
    st.session_state.relationships = {
        "isPartOf": [],
        "isFormatOf": [],
        "isReplacedBy": [],
        "isReferencedBy": []
    }

if "relationship_inputs" not in st.session_state:
    st.session_state.relationship_inputs = {k: [""] for k in st.session_state.relationships}

FIELD_HELP = {
    "title": "Short descriptive title for your training material.",
    "identifier": "Provide a URL or DOI identifying the resource.",
    "last_modified": "Last modification date in YYYY-MM-DD format.",
    "subject": "Select relevant subjects. Add new if needed.",
    "keywords": "Choose keywords or add new ones.",
    "license": "Choose one or more licenses. Add new if needed.",
    "format": "Choose content formats. E.g., Video, Slides, Article."
}

st.subheader("Metadata Entry Form")

col1, col2, col3 = st.columns(3)
with col1:
    title = st.text_input("Title", help=FIELD_HELP["title"])
with col2:
    identifier = st.text_input("Identifier (e.g. DOI or URL)", help=FIELD_HELP["identifier"])
with col3:
    last_modified_str = st.text_input("Last Modified (YYYY-MM-DD)", value=str(date.today()), help=FIELD_HELP["last_modified"])

description = st.text_area("Description", height=100)

col1, col2 = st.columns(2)
with col1:
    subject = st.multiselect("Subjects", options=vocab["subjects"], help=FIELD_HELP["subject"])
with col2:
    with st.expander("Add a New Subject"):
        new_subject = st.text_input("New Subject")
        if st.button("Save Subject") and new_subject:
            if new_subject not in vocab["subjects"]:
                vocab["subjects"].append(new_subject)
                save_vocabulary(vocab)
                st.success(f"Subject '{new_subject}' added.")

col1, col2 = st.columns(2)
with col1:
    keywords = st.multiselect("Keywords", options=vocab["keywords"], help=FIELD_HELP["keywords"])
with col2:
    with st.expander("Add a New Keyword"):
        new_keyword = st.text_input("New Keyword")
        if st.button("Save Keyword") and new_keyword:
            if new_keyword not in vocab["keywords"]:
                vocab["keywords"].append(new_keyword)
                save_vocabulary(vocab)
                st.success(f"Keyword '{new_keyword}' added.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    educational_level = st.multiselect("Education Level", vocab["educational_levels"])
with col2:
    instructional_method = st.multiselect("Instructional Method", vocab["instructional_methods"])
with col3:
    learning_resource_type = st.multiselect("Resource Type", [rt["label"] for rt in vocab["learning_resource_types"]])
with col4:
    format_ = st.multiselect("Format", [f["label"] for f in vocab["formats"]], help=FIELD_HELP["format"])

st.subheader("Relationships")
for rel_type in st.session_state.relationship_inputs:
    st.markdown(f"**{rel_type}**")
    for i, url in enumerate(st.session_state.relationship_inputs[rel_type]):
        st.session_state.relationship_inputs[rel_type][i] = st.text_input(f"{rel_type}_{i}", value=url, label_visibility="collapsed", placeholder="https://...")
    if st.button(f"Add another {rel_type} URL"):
        st.session_state.relationship_inputs[rel_type].append("")

st.subheader("License")
col1, col2 = st.columns([2, 1])
with col1:
    selected_license_labels = st.multiselect("Choose Licenses", [lic["name"] for lic in vocab["licenses"]], help=FIELD_HELP["license"])
    license_urls = [lic["url"] for lic in vocab["licenses"] if lic["name"] in selected_license_labels]
    for name, url in zip(selected_license_labels, license_urls):
        st.markdown(f"- **{name}** [\U0001F517]({url})")
with col2:
    with st.expander("Add New License"):
        new_license_name = st.text_input("License Name")
        new_license_url = st.text_input("License URL")
        if st.button("Save License"):
            if new_license_name and new_license_url:
                vocab["licenses"].append({"name": new_license_name, "url": new_license_url})
                save_vocabulary(vocab)
                st.success(f"License '{new_license_name}' added.")
            else:
                st.error("Both license name and URL are required.")

if st.button("Save Metadata"):
    try:
        last_modified = datetime.strptime(last_modified_str, "%Y-%m-%d").date()
    except ValueError:
        st.error("Invalid date format. Use YYYY-MM-DD.")
        st.stop()

    if not title or not subject or not keywords:
        st.error("Title, Subject and Keywords are required.")
        st.stop()

    resource_type_values = [rt["value"] for rt in vocab["learning_resource_types"] if rt["label"] in learning_resource_type]
    format_values = [f["value"] for f in vocab["formats"] if f["label"] in format_]

    metadata = ResourceMetadata(
        id=generate_uuid(),
        title=title,
        description=description,
        subject=subject,
        keywords=keywords,
        created=date.today(),
        date_modified=last_modified,
        educational_level=educational_level,
        instructional_method=instructional_method,
        learning_resource_type=resource_type_values,
        format=format_values,
        license=license_urls,
        identifier=identifier,
        language="en"
    )

    MetadataManager.save_metadata(metadata)
    filename = generate_filename(metadata)
    metadata_path = Path("data/metadata") / f"{filename}.jsonld"
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    for key, urls in st.session_state.relationship_inputs.items():
        valid_urls = [u for u in urls if u.strip()]
        if valid_urls:
            data[f"schema:{key}"] = valid_urls
    metadata_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    st.success("Metadata saved with relationships and license.")
    st.download_button("Download JSON-LD", data=json.dumps(data, indent=2), file_name=f"{metadata.id}.jsonld", mime="application/ld+json")
    st.info("You can now clear the form to enter another record.")
