
import streamlit as st


def inject_mobile_css():
    """
    Injects CSS to optimize the layout for mobile devices.
    Hides the sidebar on small screens and adjusts font sizes.
    """
    # Inject JavaScript to detect screen width
    # js_code = """
    # <script>
    #     const width = window.innerWidth;
    #     if (width < 768) {
    #         document.body.classList.add('mobile');
    #     }
    # </script>
    # """
    # st.components.v1.html(js_code) # This can cause reload loops, avoiding for now

    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            .css-1d391kg {
                padding-top: 1rem;
            }
            .css-12oz5g7 {
                padding-top: 1rem;
            }
            h1 {
                font-size: 1.5rem !important;
            }
            h2 {
                font-size: 1.25rem !important;
            }
            .stButton button {
                width: 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
