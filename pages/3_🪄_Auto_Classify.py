import streamlit as st
import joblib
import openai
from dotenv import load_dotenv
import os
import numpy as np
import sys

sys.path.append("../")
from src import TextReport

st.set_page_config(
    page_title="Auto Classify",
    page_icon="🪄",
)

if "id" not in st.session_state:
    st.session_state["id"] = 0


def callback():
    st.session_state["id"] += 1


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_text(text):
    results = openai.Embedding.create(model="text-embedding-ada-002", input=text)
    return results


@st.cache_data()
def st_analyze_pdf(uploaded_file, lang):
    pdf_object = TextReport(uploaded_file, lang=lang)
    raw_text = pdf_object.pdf_to_text()
    return raw_text


with st.sidebar:
    st.write("Report Language")
    lang = st.selectbox("Select Language", ("fra", "eng"))

loaded_model = joblib.load("models/openAI_model.joblib")
label_dict = {i: label for i, label in enumerate(loaded_model.classes_)}


st.write("# Auto Classify🪄")
st.markdown(
    """
### Auto Classify🪄 is a simple web-based tool to automatically predict a congenital myopathy sub-type diagnosis from patient histology report PDF.
Upload a single PDF file or copy paste your text-report and the tool will automatically try to predict the congenital myopathy diagnosis among: nemaline myopathy, core myopathy, centrenoculear myopathy or non congenital myopathy (NON-MC).

🚨 DISCLAIMER: This tool use [OpenAI API](https://openai.com/). All data inserted in this tools are sent to OpenAI servers. Please do not upload private or non-anonymized data. As per their terms of service [OpenAI does not retain any data  (for more time than legal requirements, click for source) and do not use them for trainning.](https://openai.com/policies/api-data-usage-policies) However, we do not take any responsibility for any data leak.    
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
    embedding = np.array(results["data"][0]["embedding"])
    prediction = loaded_model.predict(embedding.reshape(1, -1))
    st.write("Prediction: ", prediction[0])
    st.markdown("# Probability of each diagnosis")
    confidence = loaded_model.predict_proba(embedding.reshape(1, -1))
    for index, value in enumerate(confidence[0]):
        st.write(f"Confidence score for:  {label_dict[index]}: {round(value*100)}% ")
