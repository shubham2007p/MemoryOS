import streamlit as st
import os

# Set page configuration to maximum widescreen and collapse the sidebar for a pure app look
st.set_page_config(
    page_title="MemoryOS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit header, footer, padding, and default styling to preserve the custom HTML layout
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0px !important;
        margin: 0px !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100% !important;
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    body {
        margin: 0px !important;
        padding: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# Read index.html content
HTML_PATH = os.path.join(os.path.dirname(__file__), "index.html")
try:
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
except Exception as e:
    html_content = f"<h3>Error loading index.html: {e}</h3>"

# Render the HTML content inside a full viewport container
st.components.v1.html(html_content, height=900, scrolling=True)
