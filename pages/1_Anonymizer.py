import os
import streamlit as st
from streamlit.components.v1 import html
from zipfile import ZipFile
import uuid

import sys

sys.path.append("../")
from src import TextReport

st.set_page_config(
    page_title="Anonymizer",
    page_icon="🕵️",
)

if "id" not in st.session_state:
    st.session_state["id"] = 0


def callback():
    st.session_state["id"] += 1


@st.cache_resource(ttl=1)
def st_analyze_pdf(uploaded_file, lang):
    pdf_object = TextReport(uploaded_file, lang=lang)
    path_pdf = pdf_object.pdf_censor("results")
    censor_file = open(path_pdf, "rb")
    return path_pdf, censor_file


@st.cache_resource(ttl=3600)
def st_zip_file(uploaded_file, lang):
    zip_name = str(uuid.uuid4()) + ".zip"
    with ZipFile(zip_name, "w") as zipObj:
        for file in uploaded_file:
            path_pdf, censor_file = st_analyze_pdf(file, lang)
            zipObj.writestr(path_pdf.split("/")[-1], censor_file.read())
            try:
                os.remove(path_pdf)
            except:
                pass
    zip_file = open(zip_name, "rb")
    return zip_name, zip_file


st.write("# Anonymizer🕵️")
st.markdown(
    """
### Anonymizer🕵️ is a simple web-based tool to automatically censor patient histology report PDF.  
Upload multiple PDF files and the tool will automatically censor the patient name, date of birth, date of the report and give you a download link to the archive.  
No data are stored on the server, everything is erased right after the anonymization.  
Creator and Maintainer: [**Corentin Meyer**, 3rd year PhD Student in the CSTB Team, ICube — CNRS — Unistra](https://lambda-science.github.io/)  <corentin.meyer@etu.unistra.fr>  
"""
)
st.markdown("**Upload multiple PDF**")
st.info("10 PDFs takes ~1min to be processed.")

with st.sidebar:
    st.write("Report Language")
    lang = st.selectbox("Select Language", ("fra", "eng"))
    mode = st.selectbox("Select Mode", ("regex", "regex+chatgpt"))

uploaded_file = st.file_uploader(
    "Choose PDFs",
    type=["pdf"],
    accept_multiple_files=True,
    key=st.session_state["id"],
)
if uploaded_file != []:
    st.write(f"{len(uploaded_file)} file(s) uploaded !")
    # random UUID name for zip file

    zip_name, zip_file = st_zip_file(uploaded_file, lang)
    st.success(
        "All reports have been processed ! You can now download the archive. Click on the donwload button below will reset the page."
    )
    st.download_button(
        "Download Censored Report",
        zip_file,
        file_name=zip_name,
        key="download",
        on_click=callback,
    )
    try:
        os.remove(zip_name)
    except:
        pass

html(
    f"""
    <script defer data-domain="lbgi.fr/anonymizer" src="https://plausible.cmeyer.fr/js/script.js"></script>
    """
)
