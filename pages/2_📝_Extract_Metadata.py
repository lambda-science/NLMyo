import streamlit as st
from dotenv import load_dotenv
import os
import sys
import openai
import json

sys.path.append("../")
from src import TextReport

st.set_page_config(
    page_title="Extract Metadata",
    page_icon="📝",
)

if "id" not in st.session_state:
    st.session_state["id"] = 0


def callback():
    st.session_state["id"] += 1


with st.sidebar:
    st.write("Report Language")
    lang = st.selectbox("Select Language", ("fra", "eng"))


@st.cache_data()
def extract_metadata(prompt):
    system = """
You are an assistant that extract informations from free text. OUTPUT MUST KEEP THE KEY NAMES AND FOLLOW THIS JSON FORMAT SIMPLY REPLACE THE VALUES. IF YOU CAN'T FIND AN INFORMATION SIMPLY INDICATE N/A DON'T TRY TO INVENT IT. Here is the list of informations to retrives, json key are indicated in parenthesis: complete name (name), age (age), birth date (birth), biopsy date (biodate), biopsy sending date (sending), muscle (muscle), biopsy number (bionumber), diagnosis (diag), presence of anomaly in PAS staining (PAS), presence of anomaly in Soudan Staining (Soudan), presence of anomaly in COX staining (COX), presence of anomaly in ATP staining (ATP),  presence of anomaly in Phosrylase staining (phospho)
Please report all dates to the format DD-MM-YYYY and all ages in years, indicate 0 if less than 1 year.

{"name":["John Doe", "Jane John"], "age":"1", "birth": "01-01-1990", "biodate": "02-10-1995", "sending": "02-10-1995", "muscle": "quadriceps", "bionumber": "1234-56", "diag": "Core Myopathy", "PAS": "yes", "Soudan": "no", "COX": "N/A", "ATP": "N/A", "phospho": "N/A"}
"""

    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        # stop="<|DONE|>",
        max_tokens=1500,  # sanity limit
        temperature=0,
    )
    # print(r["usage"])
    return r["choices"][0]["message"]["content"]


@st.cache_data()
def st_analyze_pdf(uploaded_file, lang):
    pdf_object = TextReport(uploaded_file, lang=lang)
    raw_text = pdf_object.pdf_to_text()
    return raw_text


st.write("# Extract Metadata 📝")
st.markdown(
    """
### Extract Metadata 📝 is a simple web-based tool to automatically extract common metadata from patient histology report PDF to a JSON format.  
Upload a single PDF file or copy paste your text-report and the tool will automatically find for your all: complete name, age, birth date, biopsy date, biopsy sending date, muscle, biopsy number, diagnosis, presence of anomaly in PAS staining, presence of anomaly in Soudan Staining, presence of anomaly in COX staining, presence of anomaly in ATP staining,  presence of anomaly in Phosrylase staining.

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
        st.write("## Raw text to analyse")
        st.write(raw_text)
    prompt = f"""
    INPUT:
    {raw_text}
    OUTPUT:
    
    """
    result_str = extract_metadata(prompt)
    st.write("## Analysis Results")
    try:
        json_results = json.loads(result_str)
        st.write(json_results)
    except:
        st.write("Error decoding JSON raw output:")
        st.write(result_str)
