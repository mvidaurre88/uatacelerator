#IMPORTS DE TERCEROS
import streamlit as st

# IMPORTS PROPIOS
from components.top_bar import top_bar
from components.section_title import section_title
from utils.navigation import go_to

def screen_load_files():
    
    container = st.empty()
    with container.container():
        
        # CONSTANTES
        mode = st.session_state.mode
        
        # BARRA DE NAVEGACION
        top_bar(back_to="select", show_stepper=True, step=1)
            
        with st.columns([1, 7, 1])[1]:
            
            # CARGA DEL DOCUMENTO ANTERIOR
            if mode == "update":
                doc_type =st.session_state.doc_type
                section_title(f"Cargá acá tu {doc_type} anterior", left=True)
                file = st.file_uploader("Subir documento anterior", 
                                        type=["pdf", "docx", "xlsx"], 
                                        accept_multiple_files=False, 
                                        label_visibility="collapsed")
                st.session_state.file = file
            
            # CARGA DE ARCHIVOS ADICIONALES 
            section_title("Cargá los archivos que tengas (transcripciones, macros, código, etc)", left=True)
            files = st.file_uploader("Subir archivos",
                                    type=["pdf", "png", "txt", "docx", "py", "xlsm", "xlsx", "zip"],
                                    accept_multiple_files=True,
                                    label_visibility="collapsed")
            st.session_state.files = files
        
        # BOTÓN AVANZAR
        with st.columns([3,1,3])[1]:
            clicked = st.button("Avanzar paso", use_container_width=True, type="primary")
            
    if clicked:
        if not files:
            st.warning("Cargá al menos un archivo.")
        elif mode == "update" and not st.session_state.file:
            st.warning(f"Cargá tu {doc_type} anterior")
        else:
            container.empty()
            go_to("ai")
