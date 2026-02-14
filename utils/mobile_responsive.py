import streamlit as st


def inject_mobile_css():
    """
    Inject CSS to make Streamlit apps more mobile-responsive.
    Hides the sidebar on small screens by default and adjusts padding.
    """
    # Inject JavaScript to detect screen width
    # Note: Streamlit's html component creates an iframe, so this JS runs in the iframe.
    # To affect the parent, we generally need CSS media queries which are simpler.

    # We kept the variable assignment to silence the unused variable warning,
    # but commented out the st.components.v1.html call if it wasn't being used effectively.
    # For now, we will just use pure CSS injection which is more reliable.

    # js_code = """
    # <script>
    #     const width = window.innerWidth;
    #     const doc = window.parent.document;
    #     // ... logic to toggle sidebar ...
    # </script>
    # """
    # st.components.v1.html(js_code, height=0)

    st.markdown(
        """
        <style>
        /* Mobile adjustments */
        @media (max-width: 768px) {
            .block-container {
                padding-top: 3rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            /* Hide sidebar by default on mobile (streamlit usually handles this, but we can force styles) */
            [data-testid="stSidebar"] {
                width: 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
