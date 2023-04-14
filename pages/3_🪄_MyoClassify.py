import streamlit as st
import joblib
import os
import numpy as np
import sys
from streamlit.components.v1 import html
from langchain.embeddings import HuggingFaceInstructEmbeddings

sys.path.append("../")
from src import TextReport

st.set_page_config(
    page_title="MyoClassify",
    page_icon="🪄",
)

if "id" not in st.session_state:
    st.session_state["id"] = 0


def callback():
    st.session_state["id"] += 1


@st.cache_resource()
def load_embedding_model():
    embeddings = HuggingFaceInstructEmbeddings(
        query_instruction="Represent the medicine document for classification: "
    )
    return embeddings


@st.cache_data()
def embed_text(text):
    embeddings = load_embedding_model()
    results = embeddings.embed_query(text)
    return results


@st.cache_data()
def st_analyze_pdf(uploaded_file, lang):
    pdf_object = TextReport(uploaded_file, lang=lang)
    raw_text = pdf_object.pdf_to_text()
    return raw_text


with st.sidebar:
    st.write("Report Language")
    lang = st.selectbox("Select Language", ("fra", "eng"))

loaded_model = joblib.load("models/instructor_model.joblib")
label_dict = {i: label for i, label in enumerate(loaded_model.classes_)}


st.write("# MyoClassify🪄")
st.markdown(
    """
### MyoClassify🪄 is a simple web-based tool to automatically predict a congenital myopathy sub-type diagnosis from patient histology report PDF.
Upload a single PDF file or copy paste your text-report and the tool will automatically try to predict the congenital myopathy diagnosis among: nemaline myopathy, core myopathy, centrenoculear myopathy or non congenital myopathy (NON-MC).

Creator and Maintainer: [**Corentin Meyer**, 3rd year PhD Student in the CSTB Team, ICube — CNRS — Unistra](https://lambda-science.github.io/)  <corentin.meyer@etu.unistra.fr>  
"""
)


st.header("PDF or Text Input")
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Choose patient PDF",
        type="pdf",
        accept_multiple_files=False,
        key=st.session_state["id"],
    )
with col2:
    input_text = st.text_area(
        "OR Write here your patient report or upload a PDF", key="input"
    )

if uploaded_file or input_text:
    if uploaded_file:
        raw_text = st_analyze_pdf(uploaded_file, lang)
        st.write("## Raw text")
        st.write(raw_text)
    else:
        raw_text = input_text
        st.write("## Raw text")
        st.write(raw_text)
    st.markdown("# Most probable diagnosis")
    results = embed_text(input_text)
    embedding = np.array(results)
    prediction = loaded_model.predict(embedding.reshape(1, -1))
    st.write("Prediction: ", prediction[0])
    st.markdown("# Probability of each diagnosis")
    confidence = loaded_model.predict_proba(embedding.reshape(1, -1))
    for index, value in enumerate(confidence[0]):
        st.write(f"Confidence score for:  {label_dict[index]}: {round(value*100)}% ")

html(
    f"""
    <script defer data-domain="lbgi.fr/nlmyo" src="https://plausible.cmeyer.fr/js/script.js"></script>
    """
)
