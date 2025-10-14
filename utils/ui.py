import streamlit as st

def hide_streamlit_css(
    hide_menu: bool = True,
    hide_footer: bool = True,
    hide_header: bool = False,
    hide_deploy_button: bool = True,
    hide_sidebar_button: bool = True,
    remove_padding: bool = True,
):
    """ Hide Streamlit UI elements """

    css = []

    if hide_menu:
        css.append("#MainMenu {visibility: hidden;}")

    if hide_footer:
        css.append("footer {visibility: hidden;}")

    # if hide_header:
    #     css.append("header {visibility: hidden;}")

    if hide_deploy_button:
        css.append('[data-testid="stAppDeployButton"] {display: none;}')

    if hide_sidebar_button:
        css.append('[data-testid="stSidebarCollapseButton"] {display: none;}')

    if remove_padding:
        css.append("""
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
                padding-left: 3rem !important;
                padding-right: 3rem !important;
            }
        """)
        
    st.markdown("<style>" + "\n".join(css) + "</style>", unsafe_allow_html=True)

def metric_card_css():
    """ Style for metric cards """
    
    css = """
    /* Main metric container */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    
    /* Hover effect for metrics */
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* Metric label styling */
    div[data-testid="stMetric"] label {
        color: #6c757d;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.1px;
    }
    
    /* Metric value styling */
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #212529;
        font-size: 24px;
        font-weight: 700;
    }
    
    /* Metric delta (change indicator) styling */
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 14px;
        font-weight: 600;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def container_card_css():
    """ Style for container cards """
    
    css = """
    /* Target containers with key parameter using st-key- prefix class */
    [class*="st-key-"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        transition: box-shadow 0.3s ease, transform 0.3s ease !important;
    }
    
    /* Hover effect for containers */
    [class*="st-key-"]:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Ensure metric cards inside containers don't get double styling */
    [class*="st-key-"] div[data-testid="stMetric"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    /* Hide the fullscreen button in Plotly modebar */
    button[data-title="Fullscreen"],
    button[aria-label="Fullscreen"] {
        display: none !important;
    }
    
    /* Alternative: Hide by SVG path */
    .modebar-btn[data-title="Fullscreen"] {
        display: none !important;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def tabs_css():
    """ Style for tabs """
    css = """
    /* Tab list container with background that fits content */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        padding: 4px;
        background-color: #e8e8e8;
        border-radius: 8px;
        display: inline-flex;
        width: fit-content;
    }

    /* Individual tabs - smaller pill style with BOLD */
    .stTabs [data-baseweb="tab"] {
        height: 25px;
        white-space: pre-wrap;
        background-color: transparent;
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        color: #6b7280;
        font-weight: 700 !important;
        font-size: 13px;
        min-height: auto;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Also target the text inside the tab button */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-weight: 700 !important;
        transition: color 0.3s ease-in-out;
    }

    /* Tab hover effect */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.5);
        transform: scale(1.02);
    }

    /* Active/selected tab - white pill */
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #1f2937;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        position: relative;
    }

    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
        pointer-events: none;
        z-index: -1;
    }

    .stTabs [aria-selected="true"]:hover::after {
        opacity: 1;
    }

    /* Hide the default underline indicator */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent;
        display: none;
    }

    /* Remove bottom border line */
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* Tab panel content area */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 20px;
        animation: fadeIn 0.3s ease-in-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Tab list button wrapper */
    .stTabs [data-baseweb="tab-list"] button {
        padding-top: 0;
        padding-bottom: 0;
        font-weight: 700 !important;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
