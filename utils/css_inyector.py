# IMPORTS DE TERCEROS
import streamlit as st

def inject_css():
    st.markdown("""<style>

    /* LAYOUT GENERAL */
    section[data-testid="stMain"] {
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 2rem 3rem 0 3rem !important;
        max-width: 100% !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.8rem !important;
    }

    div[data-testid="stElementContainer"] {
        margin-bottom: 0rem !important;
    }

    /* BOTONES */
    .stButton>button {
        background-color: #e68200;
        color: white;
        font-weight: bold;
        font-size: 15px;
        padding: 6px 12px;
        border-radius: 3px;
        border: none;
    }
    .stButton>button:hover { background-color: #ff9500; }
    .stButton>button:active { background-color: #b36500; }

    section[data-testid="stMain"] div[data-testid="stButton"] button[kind="secondary"] {
        background-color: transparent !important;
        color: #aaa !important;
        border: 1px solid #aaa !important;
        padding: 1px 10px !important;
    }
    section[data-testid="stMain"] div[data-testid="stButton"] button[kind="secondary"]:hover {
        color: #e68200 !important;
        border-color: #e68200 !important;
    }

    /* INPUTS */
    input, textarea {
        background-color: transparent !important;
        font-size: 15px !important;
    }
    
    textarea {
        field-sizing: content !important;
        height: auto !important;
        min-height: 38px !important;
        padding: 8px 12px 2px 12px !important;
        border: none !important;
        resize: none !important;
    }

    /* RADIO BUTTONS */
    div[role="radiogroup"] label > div:first-child {
        display: none;
    }

    div[role="radiogroup"] label {
        background-color: #2d2d2d;
        padding: 40px;
        margin: 5px;
        border-radius: 10px;
        border: 2px solid transparent;
        cursor: pointer;
        text-align: center;
        transition: 0.2s;
        max-width: 350px !important;
        flex: 1 1 0 !important;
        justify-content: center;
        box-sizing: border-box;
    }

    div[role="radiogroup"] label:hover {
        border: 2px solid #e68200;
        transform: scale(1.02);
    }

    div[role="radiogroup"] label:has(input:checked) {
        border: 2px solid #e68200;
        background-color: #3a2a10;
    }

    /* El radiogroup centra sus opciones */
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        flex-wrap: wrap !important;
        width: 100% !important;
    }

    div[data-testid="stRadio"] {
        width: 100% !important;
    }

    div[data-testid="stElementContainer"]:has(div[data-testid="stRadio"]) {
        width: 100% !important;
    }

    /* ALERTAS */
    div[data-testid="stAlert"] {
        margin-top: 15px !important;
    }

    /* COMPONENTES CUSTOM */
    .top-bar {
        position: sticky;
        top: 0;
        background-color: #3c3c3c;
        padding: 10px 10px;
        z-index: 999;
        border-bottom: 1px solid #555;
    }

    .seccion-titulo {
        text-align: center;
        font-size: 26px;
        font-weight: 600;
        color: #ffffff !important;
        margin: 20px 80px 20px 80px;
        padding: 0 20px;
    }

    .aclaraciones {
        background-color: #2d2d2d;
        border-radius: 4px;
        padding: 10px 10px;
        margin: 0 0 20px 0;
    }
    .aclaraciones h3 { margin: 0 0 5px 0; font-size: 16px; }
    .aclaraciones ul { padding-left: 10px; }
    .aclaraciones li { margin-bottom: 4px; color: #d4d4d4; }
    .aclaraciones li:last-child { margin-bottom: 0; }

    div[data-testid="stVerticalBlock"]:has(> div[class*="personalizacion_container"]),
    div.st-key-personalizacion_container {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 20px 0 10px 30px !important;
        margin: 5px 0 20px 0;
    }

    /* OCULTAR ELEMENTOS NATIVOS */
    a[aria-label="Link to heading"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSpinnerIcon"] { display: none !important; }

    button[title="View fullscreen"],
    button[title="Fullscreen"],
    button[aria-label="View fullscreen"],
    button[aria-label="Fullscreen"] {
        display: none !important;
    }
    
    .field-label { height: 45px; display: flex; align-items: center; }
    
    /* 1. El stElementContainer que envuelve el componente custom */
    div[data-testid="stElementContainer"]:has(iframe[title*="st_keyup"]) {
        height: 48px !important;
        min-height: 48px !important;
        max-height: 48px !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 2. El wrapper interno del iframe (la clase emotion-cache) */
    div[data-testid="stElementContainer"]:has(iframe[title*="st_keyup"]) > div {
        height: 48px !important;
        min-height: 48px !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 3. El iframe mismo */
    iframe[title*="st_keyup"] {
        height: 70px !important;       /* alto suficiente para mostrar el input completo */
        min-height: 70px !important;
        margin-top: -22px !important;  /* sube el iframe para esconder el label vacío */
        border: none !important;
    }
    
    div[data-testid="InputInstructions"] { display: none !important; }
    
    /* Espacio entre expanders */
    div[data-testid="stExpander"] { margin-bottom: 10px; }
    div[data-testid="stExpander"] > div > div { padding-top: 8px; }
    div[data-testid="stExpanderDetails"] { padding: 10px 15px 15px 15px !important; }
    
    [class*="st-key-form_container"] {
        background-color: transparent !important;
        border: 1px solid #5A5A5A !important;
        border-radius: 8px !important;
        padding: 0 20px 15px 20px !important;
        margin: 10px 0px !important;
    }
    
    .container-title {
        font-weight: bold;
        padding: 12px 0 !important;
        margin: 0 0 15px 0 !important;
        border-bottom: 1px solid #5A5A5A;
    }
    
    [class*="st-key-double_"] {
        padding-left: 20px !important;
    }
    
    .st-key-css_injector_verify {
        margin-left: 20px !important;
        background-color: transparent !important;
        border: 1px solid #5A5A5A !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    
    </style>""", unsafe_allow_html=True)