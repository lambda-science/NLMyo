import streamlit as st

st.set_page_config(
    page_title="Auto Classify",
    page_icon="🤖",
)

if "id" not in st.session_state:
    st.session_state["id"] = 0


def callback():
    st.session_state["id"] += 1
