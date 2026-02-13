"""
Mobile responsiveness utilities for Streamlit dashboard.

Provides:
- Responsive column layouts
- Mobile-optimized Folium map heights
- Touch-friendly button styles
- Font size adjustments
"""

import streamlit as st


def get_device_type():
    """
    Detect device type based on viewport width.

    Returns:
        str: 'mobile', 'tablet', or 'desktop'
    """
    # Inject JavaScript to detect screen width
    """
    <script>
        const width = window.innerWidth;
        const deviceType = width < 768 ? 'mobile' : width < 1024 ? 'tablet' : 'desktop';
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: deviceType}, '*');
    </script>
    """

    # Use st.components for device detection (simplified)
    # In practice, we use CSS media queries instead
    return "desktop"  # Default fallback


def responsive_columns(num_cols, mobile_cols=1):
    """
    Create responsive column layout.

    Args:
        num_cols: Number of columns on desktop
        mobile_cols: Number of columns on mobile (default: 1)

    Returns:
        list: Column objects

    Example:
        cols = responsive_columns(4, mobile_cols=2)
        with cols[0]:
            st.metric("Metric 1", "100")
    """
    # Streamlit doesn't support dynamic columns based on screen size
    # We return desktop layout and rely on CSS for mobile stacking
    return st.columns(num_cols)


def get_map_height(default=400, mobile=300):
    """
    Get responsive map height based on device.

    Args:
        default: Height for desktop/tablet
        mobile: Height for mobile devices

    Returns:
        int: Map height in pixels
    """
    # In production, detect via JavaScript
    # For now, use default (CSS handles mobile via viewport)
    return default


def inject_mobile_css():
    """
    Inject mobile-responsive CSS into Streamlit app.

    Handles:
    - Column stacking on mobile
    - Font size adjustments
    - Button touch targets (min 44x44px)
    - Map height responsiveness
    """
    mobile_css = """
    <style>
        /* Mobile-first responsive design */
        
        /* Metrics stacking on mobile */
        @media (max-width: 768px) {
            /* Force single column layout */
            [data-testid="column"] {
                width: 100% !important;
                flex: 100% !important;
                max-width: 100% !important;
            }
            
            /* Adjust metric font sizes */
            [data-testid="stMetricValue"] {
                font-size: 1.5rem !important;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 0.9rem !important;
            }
            
            /* Stack buttons vertically */
            .stButton > button {
                width: 100% !important;
                margin-bottom: 0.5rem !important;
                min-height: 44px !important; /* Touch target */
            }
            
            /* Folium map height adjustment */
            iframe[title="folium.folium.Map"] {
                height: 300px !important;
            }
            
            /* Reduce padding on mobile */
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            
            /* Sidebar full width on mobile when open */
            [data-testid="stSidebar"] {
                width: 100% !important;
            }
            
            /* Font size adjustments */
            h1 {
                font-size: 1.75rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
            }
            
            h3 {
                font-size: 1.25rem !important;
            }
            
            /* Table responsiveness */
            table {
                font-size: 0.85rem !important;
            }
            
            /* Expander touch targets */
            [data-testid="stExpander"] summary {
                min-height: 44px !important;
            }
        }
        
        /* Tablet adjustments */
        @media (min-width: 769px) and (max-width: 1024px) {
            /* Two columns max on tablet */
            [data-testid="column"]:nth-child(n+3) {
                margin-top: 1rem;
            }
            
            /* Slightly larger map */
            iframe[title="folium.folium.Map"] {
                height: 350px !important;
            }
        }
        
        /* Touch-friendly interactive elements */
        @media (pointer: coarse) {
            /* All clickable elements min 44x44px */
            a, button, [role="button"], .stSelectbox {
                min-height: 44px !important;
                min-width: 44px !important;
            }
            
            /* Increase padding for better touch targets */
            .stSelectbox > div > div {
                padding: 0.75rem !important;
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
    """

    st.markdown(mobile_css, unsafe_allow_html=True)


def mobile_friendly_chart_config():
    """
    Return Plotly chart config optimized for mobile.

    Returns:
        dict: Plotly config with mobile optimizations
    """
    return {
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        "responsive": True,
        "toImageButtonOptions": {
            "format": "png",
            "filename": "5d_chart",
            "height": 800,
            "width": 1200,
            "scale": 2,
        },
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
