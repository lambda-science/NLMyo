import streamlit as st

st.set_page_config(
    page_title="Extract Metadata",
    page_icon="📝",
)

if "id" not in st.session_state:
    st.session_state["id"] = 0


def callback():
    st.session_state["id"] += 1
