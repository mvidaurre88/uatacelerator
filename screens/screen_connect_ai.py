from datetime import date
import os
import traceback
import base64
import json5
import logging
import streamlit as st
import graphviz

from docs import get_doc
from utils.navigation import *
from components.top_bar import top_bar
from components.section_title import section_title
from utils.AIConnector import send_to_ai
from utils.prompt_filter import filter_prompt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)


def screen_connect_ai():
    
    # CONSISTENCIA DE ARCHIVOS EN SESION
    file = st.session_state.get("file", None)
    files = st.session_state.get("files", None)
    if file is not None:
        try:
            extension = os.path.splitext(file.name)[1]
            file.name = st.session_state.doc_type + extension
            files.append(file)
            st.session_state.files = files
        except Exception as e:
            logger.error(f"No se pudo renombrar el archivo: {e}")
    
    container = st.empty()
    with container.container():
        env = st.secrets.get("ENV")
        top_bar(back_to="load", show_stepper=True, step=2, key="ai")
        render_loading_frame("Procesando con IA...")
        
        # ACTUO SEGUN EL AMBIENTE Y ARCHIVO
        response = None
        if env == "DESA":
            doc_type = st.session_state.get("doc_type", "")
            if doc_type != "":
                with open(os.path.join(BASE_DIR, "prompts", doc_type + "_example.json"), "r", encoding="utf-8") as f:
                    response = f.read()
        elif env == "PROD":
            with st.spinner(""):
                response = process_with_ai(st.session_state.files)
    
    # PARSEO DE LA RESPUESTA --------------------------------------------------------------------
    try:
        file_content = response
        file_content_clean = file_content.replace("```json", "").replace("```", "").strip()
        file_content_clean = fix_encoding(file_content_clean)
        data = json5.loads(file_content_clean)
    except Exception as e:
        logger.error(f"Fallo al parsear JSON: {e}")
        logger.error(f"Contenido recibido:\n{file_content_clean[:2000]}")
        st.error(f"Error al procesar la respuesta de la IA.\n\n`{e}`")
        st.stop()

    st.session_state.response = generate_modify(add_current_date(data))
    
    # GENERACION DE DIAGRAMAS
    container.empty()
    with container.container():
        top_bar(back_to="load", show_stepper=True, step=2, key="diag")
        render_loading_frame("Generando diagramas...")
        with st.spinner(""):
            if st.session_state.doc_type == "PDD":
                st.session_state.diagramaAltoNivel = generate_diagram_img(data.get("diagramaAltoNivel", ""))
                st.session_state.diagramaBajoNivel = generate_diagram_img(data.get("diagramaBajoNivel", ""))
            elif st.session_state.doc_type == "SDD":
                st.session_state.diagrama_pasos = generate_diagram_img(data.get("diagrama_pasos", ""))
                st.session_state.diagrama_detalle = generate_diagram_img(data.get("diagrama_detalle", ""))
    go_to("verify")


# FUNCION PARA LLAMADA A LA API
def process_with_ai(files):
    try:
        doc_type = st.session_state.doc_type
        prompt_path = os.path.join(BASE_DIR, "prompts", doc_type + ".txt")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_text = f.read().strip()
        
        if not prompt_text:
            raise ValueError(f"El prompt {prompt_path} está vacío")
        
        # 2) Filtrar según los toggles del usuario
        document = get_doc(doc_type)
        toggles = st.session_state.get("field_toggles", {})
        
        if document and toggles:
            fields_mapping = document.get_fields()
            prompt_text = filter_prompt(prompt_text, fields_mapping, toggles)
            logger.info(f"Prompt final: ~{len(prompt_text) // 4:,} tokens estimados")
        
        # 3) Enviar
        response = send_to_ai(prompt=prompt_text, files=files, maxTokens=65536)
        return response

    except Exception as e:
        st.error(f"Error IA: {e}")
        st.code(traceback.format_exc())
        st.stop()

def get_gif_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return data

@st.cache_data(show_spinner=False)
def generate_diagram_img(dot_code: str) -> bytes | None:
    if not dot_code:
        return None

    # Por si Claude lo devuelve con \n escapados
    dot_code = dot_code.replace("\\n", "\n").strip()
    
    # Limpiar posibles fences de markdown
    dot_code = dot_code.replace("```dot", "").replace("```graphviz", "").replace("```", "").strip()

    logger.info(f"Diagrama DOT: {len(dot_code)} caracteres")

    try:
        src = graphviz.Source(dot_code, format="png")
        png_bytes = src.pipe(format="png")
        logger.info(f"PNG generado ({len(png_bytes)} bytes)")
        return png_bytes
    except graphviz.backend.ExecutableNotFound:
        logger.error("Graphviz no está instalado. Agregá 'graphviz' a packages.txt en Streamlit Cloud.")
        return None
    except graphviz.backend.CalledProcessError as e:
        logger.error(f"Error de sintaxis DOT: {e}")
        logger.error(f"Código recibido:\n{dot_code[:1000]}")
        return None
    except Exception as e:
        logger.error(f"Error renderizando diagrama: {e}")
        return None


def fix_encoding(text: str) -> str:
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text


def render_loading_frame(title: str):
    gif = get_gif_base64(os.path.join(BASE_DIR, "icons", "loading.gif"))
    st.markdown(
        f'<div style="text-align:center; margin-top: 40px;">'
        f'<img src="data:image/gif;base64,{gif}" width="120"></div>',
        unsafe_allow_html=True
    )
    section_title(title)
    
# AGREGA LA FECHA ACTUAL
def add_current_date(json):
    today = date.today().strftime("%d/%m/%Y")
    json["fecha"] = today
    return json    
    
# AGREGA LA NUEVA MODIFICACIÓN AL HISTORIAL            
def generate_modify(data):
    modificaciones = data.get("modificaciones", [])
    fecha = data.get("fecha", "")
    desarrollador = data.get("desarrollador", "")
    
    if not modificaciones:
        new_version = "1.0"
        motivo = "Creación de documento"
    else:
        last_version = str(modificaciones[-1].get("version", "0.0")).strip()
        parts = last_version.split(".")
        try:
            major = int(parts[0]) if parts[0] else 0
        except ValueError:
            major = 0
        new_version = f"{major + 1}.0"
        motivo = "Actualización de documento"
    modificaciones.append({ "version": new_version, "fecha": fecha, "paginas": "todas", "sector": "RPA", "autor": desarrollador, "motivo": motivo})
    
    data["version"] = new_version
    data["modificaciones"] = modificaciones
    return data