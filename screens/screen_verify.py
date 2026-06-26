# IMPORTS DE PYTHON
import traceback
import logging

# IMPORTS DE TERCEROS
import streamlit as st

# IMPORTS PROPIOS
from utils.navigation import *
from utils.docx_generator import *
from components.top_bar import top_bar
from components.section_title import section_title

logger = logging.getLogger(__name__)

def screen_verify():
    
    try:
        sanitized = sanitize(st.session_state.response)
        generate_docx(sanitized, None)
        go_to("final")
    except Exception as e:
        st.error(f"Error al generar: {e}")
        logger.error(f"Error al generar documento: {e}\n{traceback.format_exc()}")
        st.code(traceback.format_exc())

LIST_OF_STRINGS_FIELDS = {
    "entradas", "salidas", "contactos", "requisitos", "inputsProceso"
}

# REEMPLAZA LOS VALORES NONE POR STRING VACIOS
def sanitize(data):
    if isinstance(data, dict):
        for field in LIST_OF_STRINGS_FIELDS:
            if field in data and isinstance(data[field], list):
                data[field] = denormalize_list_field(data[field])
        return {k: sanitize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize(i) for i in data]
    return data

def denormalize_list_field(items):
    """Convierte [{"value": x, "_id": ...}, ...] a [x, ...]"""
    return [item["value"] if isinstance(item, dict) else item for item in items]