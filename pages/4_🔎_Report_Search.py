import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

st.set_page_config(
    page_title="Report Search",
    page_icon="🔎",
)

if "id" not in st.session_state:
    st.session_state["id"] = 0


def callback():
    st.session_state["id"] += 1


@st.cache_resource
def load_chroma():
    persist_directory = "db_myocon"
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=persist_directory, embedding_function=embeddings
    )
    return vectordb


vectordb = load_chroma()

st.write("# Report Search 🔎")
st.markdown(
    """
### Report Search 🔎 is a simple web-based tool that act as a search engine for patient histology report.  
Simply enter a symptom of interest or a small description or diagnosis, and the tool will find the top-5 best fitting reports containing this symptom or diagnosis from our database of 150 reports.

🚨 DISCLAIMER: This tool use [OpenAI API](https://openai.com/). All data inserted in this tools are sent to OpenAI servers. Please do not upload private or non-anonymized data. As per their terms of service [OpenAI does not retain any data  (for more time than legal requirements, click for source) and do not use them for trainning.](https://openai.com/policies/api-data-usage-policies) However, we do not take any responsibility for any data leak.  
Creator and Maintainer: [**Corentin Meyer**, 3rd year PhD Student in the CSTB Team, ICube — CNRS — Unistra](https://lambda-science.github.io/)  <corentin.meyer@etu.unistra.fr>  
"""
)
input_text = st.text_input("What symptoms are you looking for ? ", key="input")


if input_text:
    docs = vectordb.similarity_search_with_score(input_text, k=5)
    docs.sort(key=lambda x: x[1], reverse=True)
    st.write("Best 5 reports:")
    for index, doc in enumerate(docs[:]):
        st.markdown(f"### Top {index + 1} matching report")
        st.write("Score: ", doc[1])
        st.markdown(f"Sentence content: `{doc[0].page_content}`")
        st.markdown(f"Doc Source: `{doc[0].metadata['source']}`")
