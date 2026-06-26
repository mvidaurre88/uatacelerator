# IMPORTS DE PYTHON
import logging
import os

# IMPORTS DE TERCEROS
import streamlit as st

# IMPORTS PROPIOS
from utils.css_inyector import inject_css
from utils.router import get_screens

# PATHS Y CONSTANTES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "errors.log")
SCREENS = get_screens(BASE_DIR)
ENABLED_DOCS = st.secrets.get("ENABLED_DOCS", [])

# CONFIGURACION DE LOGGEO
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[ logging.FileHandler(LOG_FILE, encoding="utf-8") ],
                    force=True)
logger = logging.getLogger(__name__)

# CONFIGURACION INICIAL
st.set_page_config(page_title="UAT Accelerator", layout="wide", initial_sidebar_state="expanded")
st.session_state.setdefault("current_screen", "init")
st.session_state.setdefault("enabled_docs", ENABLED_DOCS)

# CSS GLOBAL
inject_css()

# ROUTER PARA ACCEDER A LAS PAGINAS
screen_fn = SCREENS.get(st.session_state.current_screen)
if screen_fn:
    screen_fn()
else:
    logger.error(f"Pantalla no encontrada: {st.session_state.current_screen}")
    st.error("Pantalla no encontrada.")
    st.session_state.current_screen = "init"
    st.rerun()