# IMPORTS DE PYTHON
import logging

# IMPORTS DE TERCEROS
import streamlit as st

# IMPORTS PROPIOS
from utils.navigation import go_to
from components.top_bar import top_bar
from components.section_title import section_title

logger = logging.getLogger(__name__)

def screen_select_document():
    
    # ESTADO INICIAL
    st.session_state.setdefault("doc_type", None)
    st.session_state.setdefault("mode", None)

    # BARRA DE NAVEGACION
    top_bar(title="", back_to="init", show_stepper=True, step=0)


    # DOCUMENTOS HABILITADOS
    enabled_docs = st.session_state.get("enabled_docs", [])
    all_types = {"PDD": "📄 PDD", "SDD": "📄 SDD", "TDD": "📄 Test Script"}
    types = {all_types[d]: d for d in enabled_docs if d in all_types}

    if not types:
        logger.error("No hay tipos de documento habilitados en la configuración.")
        st.error("No hay tipos de documento habilitados. Revisá la configuración.")
        st.stop()

    with st.columns([1,7,1])[1]:
        # TITULO
        section_title("Seleccioná el tipo de documento", left=False)
        # BOTON TIPO DOCUMENTO
        doc_type = st.radio("Tipo de documento", list(types.keys()), horizontal=True, label_visibility="collapsed")
    st.session_state.doc_type = types[doc_type]

    modes = {"Nuevo documento": "new", "Actualizar documento": "update"}
    with st.columns([1,7,1])[1]:
        # TITULO
        section_title("¿Qué acción desea realizar?")
        # BOTON TIPO ACCION
        mode = st.radio("Tipo de acción", list(modes.keys()), horizontal=True, label_visibility="collapsed")
    st.session_state.mode = modes[mode]

    # BOTÓN AVANZAR
    with st.columns([3,1,3])[1]:
        if st.button("Avanzar paso", use_container_width=True, type="primary"):
            go_to("load")