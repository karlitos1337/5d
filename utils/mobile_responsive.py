import streamlit as st

from utils.mobile_responsive import inject_mobile_css


def main():
    st.set_page_config(
        page_title="Game of Life", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed"
    )

    inject_mobile_css()

    st.title("Conway's Game of Life")

    # ... rest of the file
