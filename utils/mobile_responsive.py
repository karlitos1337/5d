import streamlit as st


def inject_mobile_css():
    """
    Inject CSS to make the application mobile-responsive.
    """
    st.markdown(
        """
        <style>
        /* Mobile Responsive Adjustments */
        @media (max-width: 768px) {
            .stApp {
                padding: 1rem;
            }
            /* Adjust font sizes for mobile */
            h1 {
                font-size: 1.5rem !important;
            }
            h2 {
                font-size: 1.25rem !important;
            }
            h3 {
                font-size: 1.1rem !important;
            }
            /* Adjust sidebar width if needed */
            [data-testid="stSidebar"] {
                width: 100% !important;
            }
            /* Adjust chart container padding */
            .stPlotlyChart {
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def get_device_type():
    """
    Detect if the user is on a mobile device or desktop.
    Currently a placeholder returning 'desktop' as Streamlit runs server-side.
    Real detection would require a custom component or JS bridge.
    """
    # Placeholder for future implementation
    # This variable was unused and causing lint errors: js_code = ...
    return "desktop"
