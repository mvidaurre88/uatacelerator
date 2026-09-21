# IMPORTS DE PYTHON
import traceback
import logging

# IMPORTS DE TERCEROS
import streamlit as st

# IMPORTS PROPIOS
from utils.navigation import *
from utils.test_script_generator import generate_TDD
from components.top_bar import top_bar
from components.section_title import section_title

logger = logging.getLogger(__name__)

def screen_verify():
    
    try:
        sanitized = sanitize(st.session_state.response)
        buffer = generate_TDD(sanitized)
        st.session_state.doc_buffer = buffer 
        go_to("final")
    except Exception as e:
        st.error(f"Error al generar: {e}")
        logger.error(f"Error al generar documento: {e}\n{traceback.format_exc()}")
        st.code(traceback.format_exc())

LIST_OF_STRINGS_FIELDS = {
    "entradas", "salidas", "contactos", "requisitos", "inputsProceso"
}

def sanitize(data, parent_key=None):
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            if k in LIST_OF_STRINGS_FIELDS and isinstance(v, list):
                v = denormalize_list_field(v)
            result[k] = sanitize(v, parent_key=k)
        return result
    elif isinstance(data, list):
        return [sanitize(i, parent_key=parent_key) for i in data]
    elif isinstance(data, str):
        return data.replace("<", "&lt;").replace(">", "&gt;")
    return data

def denormalize_list_field(items):
    """Convierte [{"value": x, "_id": ...}, ...] a [x, ...]"""
    return [item["value"] if isinstance(item, dict) else item for item in items]