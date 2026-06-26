import os, streamlit as st
from utils.navigation import *

# -- PANTALLA INICIAL ------------------------------------------------------------------------------
def screen_init(BASE_DIR):

    col_center = st.columns([4,1,4])[1]
    with col_center:
        st.image(os.path.join(BASE_DIR, "icons", "icon.ico"))

    st.markdown("<h1 style='text-align:center; margin-bottom: 15px;'>UAT Accelerator</h1>", unsafe_allow_html=True)
 
    col_center = st.columns([2,1,2])[1]
    with col_center:
        if st.button("Comenzar", use_container_width=True, type="primary"):
             go_to("select")