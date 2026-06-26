# components/section_title.py
import streamlit as st

def section_title(text: str, left: bool = False):
    if left:
        st.markdown(f"<h5 style='text-align: left;' class='seccion-titulo'>{text}</h5>",unsafe_allow_html=True)
    else:
        st.markdown(f"<h5 class='seccion-titulo'>{text}</h5>",unsafe_allow_html=True)