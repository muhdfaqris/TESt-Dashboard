import streamlit as st

def hide_streamlit(
    hide_menu=True,
    hide_footer=True,
    hide_header=True,
    hide_deploy_button=True,
    hide_sidebar_button=True,  
    remove_padding=True,
):
    """ Hide streamlit UI elements """
    
    styles = "<style>"

    if hide_menu:
        styles += "#MainMenu {visibility: hidden;}"

    if hide_footer:
        styles += "footer {visibility: hidden;}"

    # if hide_header:
    #     styles += "header {visibility: hidden;}"
    if hide_deploy_button:
        styles += '[data-testid="stAppDeployButton"] {display: none;}'

    if hide_sidebar_button:
        styles += '[data-testid="stSidebarCollapseButton"] {display: none;}'

    if remove_padding:
        styles += """
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }
        """

    styles += "</style>"
    st.markdown(styles, unsafe_allow_html=True)