import os
import streamlit as st

#----------------------------------------------------------------------
# Retorna la variable de entorno correspondiente a la key proporcionada
#----------------------------------------------------------------------
def get_secret(strKey):
    try:
        return st.secrets[strKey]
    except (FileNotFoundError, KeyError):
        return os.environ.get(strKey)

API_KEY_CLAUDE = get_secret("API_KEY_CLAUDE")
API_KEY_QWEN = get_secret("API_KEY_QWEN")
ENV = get_secret("ENV")
MODEL = get_secret("MODEL")
APP_PASSWORD = get_secret("APP_PASSWORD")

_raw_docs = get_secret("ENABLED_DOCS")
if isinstance(_raw_docs, str):
    ENABLED_DOCS = [d.strip() for d in _raw_docs.split(",")]
else:
    ENABLED_DOCS = _raw_docs