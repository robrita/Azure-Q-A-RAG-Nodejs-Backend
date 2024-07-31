import streamlit as st


def show_home():
    st.set_page_config(
        page_title="Moodle Discussion",
        page_icon="❓",
        # initial_sidebar_state="collapsed",
    )
    st.logo(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Moodle-logo.svg/768px-Moodle-logo.svg.png?20220831120610",
        link="https://ai.azure.com/",
    )
    st.title("❓Moodle Discussion")
