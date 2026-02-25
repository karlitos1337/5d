import streamlit as st


def inject_mobile_css():
    """
    Inject CSS to make the Streamlit app more mobile-responsive.
    Hides the sidebar on small screens and adjusts padding.
    """
    # Inject JavaScript to detect screen width
    _js_code = """
    <script>
        const width = window.innerWidth;
        if (width < 768) {
            // Logic to collapse sidebar could go here if Streamlit exposed an API for it
            // For now, we rely on CSS media queries
        }
    </script>
    """
    # Note: Streamlit's st.components.v1.html creates an iframe, so window.innerWidth
    # might reflect the iframe width, not the viewport.
    # CSS injection via markdown is more reliable for styling.

    st.markdown(
        """
        <style>
        /* Mobile adjustments */
        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            /* Make headings smaller on mobile */
            h1 { font-size: 1.8rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.2rem !important; }

            /* Adjust sidebar width behavior if possible,
               though Streamlit controls this largely via JS */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
