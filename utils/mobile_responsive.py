import streamlit as st

def inject_mobile_css():
    """
    Inject CSS for mobile responsiveness.
    """
    st.markdown(
        """
    <style>
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .stApp {
                padding: 0.5rem;
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 1rem;
                padding-right: 1rem;
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
            
            /* Sidebar adjustments */
            [data-testid="stSidebar"] {
                width: 100% !important;
            }
            
            /* Metric value size adjustment */
            [data-testid="stMetricValue"] {
                font-size: 1.5rem !important;
            }
            
            /* Make charts responsive */
            .js-plotly-plot {
                height: 300px !important;
            }

            /* Improve button tap targets */
            button {
                min-height: 44px !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* Adjust padding for columns */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
                min-width: unset !important;
            }
        }
        
        /* Dark mode mobile optimizations */
        @media (prefers-color-scheme: dark) and (max-width: 768px) {
            /* Reduce brightness for OLED screens */
            .stApp {
                background-color: #0e1117 !important;
            }
        }
        
        /* Landscape mobile optimizations */
        @media (max-width: 768px) and (orientation: landscape) {
            /* Reduce header size in landscape */
            h1 {
                font-size: 1.5rem !important;
            }
            
            /* Compact metrics in landscape */
            [data-testid="stMetricValue"] {
                font-size: 1.25rem !important;
            }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

def mobile_friendly_chart_config():
    """
    Return Plotly chart config optimized for mobile.

    Returns:
        dict: Plotly config with mobile optimizations
    """
    return {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': [
            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
            'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
            'hoverCompareCartesian', 'toggleSpikelines'
        ],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'chart',
            'height': 500,
            'width': 700,
            'scale': 2
        }
    }

def mobile_info_box(title, content, icon="ℹ️"):
    """
    Display mobile-optimized info box.

    Args:
        title: Box title
        content: Box content (markdown)
        icon: Emoji icon (default: ℹ️)
    """
    with st.expander(f"{icon} {title}", expanded=False):
        st.markdown(content)

def get_responsive_map_width():
    """
    Get responsive map width.

    Returns:
        int or None: Width in pixels, or None for full width
    """
    # Always use full width, CSS handles responsiveness
    return None
