import streamlit as st


def inject_mobile_css():
    """
    Inject CSS to improve mobile responsiveness.
    Hides sidebar on small screens, adjusts font sizes and padding.
    """
    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            /* Adjust sidebar behavior - might need to be hidden or collapsed by default via Streamlit config,
               but CSS can help style it when visible */
            [data-testid="stSidebar"] {
                width: 100% !important; /* Take full width when open on very small screens? Or keeps standard behavior */
            }
            
            /* Improve padding for main content */
            .main .block-container {
                padding-top: 2rem;
                padding-left: 1rem;
                padding-right: 1rem;
                padding-bottom: 2rem;
            }

            /* Adjust font sizes for headings */
            h1 {
                font-size: 1.8rem !important;
            }
            h2 {
                font-size: 1.5rem !important;
            }
            h3 {
                font-size: 1.2rem !important;
            }
            
            /* Make dataframes scrollable */
            .stDataFrame {
                overflow-x: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def check_mobile_view():
    """
    Detect if the user is likely on a mobile device based on screen width.
    Note: This is a client-side check injected via JS, but Streamlit runs server-side.
    We can't easily change server logic based on this without a component that returns value.
    For now, we just inject the CSS.
    """
    # Inject JavaScript to detect screen width

    html = """
    <script>
        const width = window.innerWidth;
        const isMobile = width <= 768;
        // We could send this back to Streamlit if we had a bi-directional component
        // For now, just logging to console for debug
        console.log("Detected screen width: " + width + ", isMobile: " + isMobile);
    </script>
    """
    st.components.v1.html(html, height=0, width=0)
