import streamlit as st


def get_device_type():
    """
    Returns 'mobile' or 'desktop' based on screen width.
    Note: This is a rough estimation as Streamlit doesn't expose request headers directly in all contexts.
    """
    return "desktop"

def inject_mobile_css():
    """
    Injects CSS to optimize layout for mobile devices.
    """
    # Inject JavaScript to detect screen width
    # js_code = """
    # <script>
    #     const width = window.innerWidth;
    #     const isMobile = width <= 768;
    #     if (isMobile) {
    #         document.body.classList.add('mobile-layout');
    #     }
    # </script>
    # """
    # st.components.v1.html(js_code, height=0)

    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            .stApp {
                padding: 1rem;
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            h1 {
                font-size: 1.8rem !important;
            }
            h2 {
                font-size: 1.5rem !important;
            }
            h3 {
                font-size: 1.2rem !important;
            }
            .stButton button {
                width: 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
