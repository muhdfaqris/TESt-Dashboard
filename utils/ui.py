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
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    div[data-testid="stMetric"] label {
        color: #6c757d;
        font-weight: 600;
        font-size: 14px;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #212529;
        font-size: 24px;
        font-weight: bold;
    }

    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 14px;
        font-weight: 600;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def container_card_css():
    """ Style for container cards """

    css = """
    .st-emotion-cache-188w4sx, .st-emotion-cache-188w4sx > div, div.stContainer {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 2px 6px rgba(0,0,0.1) !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stVerticalBlock"] > div > [data-testid="stVerticalBlock"]:not([data-testid="stMetric"]) {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
