import os, streamlit as st
from utils.navigation import *
from config import APP_PASSWORD

# ------------------------
# PANTALLA INICIAL - LOGIN
# ------------------------
def screen_init(BASE_DIR):

    col_center = st.columns([4,1,4])[1]
    with col_center:
        st.image(os.path.join(BASE_DIR, "icons", "icon.ico"))

    st.markdown("<h1 style='text-align:center; margin-bottom: 15px;'>UAT Accelerator</h1>", unsafe_allow_html=True)
 
    col_center = st.columns([2,1,2])[1]
    with col_center:
        password = st.text_input("Ingrese la contraseña", type="password")

        if st.button("Comenzar", use_container_width=True, type="primary"):
            if password == APP_PASSWORD:
                go_to("select")
            else:
                st.error("Contraseña incorrecta")