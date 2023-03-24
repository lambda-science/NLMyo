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

# From here down is all the StreamLit UI.
st.header("Report Search 🔎")
st.markdown(
    """
Enter a symptom of interest, and the tool will find the best fitting reports containing this symptom.
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
