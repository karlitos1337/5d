import streamlit as st


def inject_mobile_css():
    st.markdown(
        """
    <style>
    @media (max-width: 768px) {
        .stApp {
            padding: 1rem;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
