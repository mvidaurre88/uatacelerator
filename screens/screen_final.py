# IMPORTS DE TERCEROS
import streamlit as st

# IMPORTS PROPIOS
from utils.navigation import go_to
from components.top_bar import top_bar
from components.form import field_row
from docs import get_doc

def screen_final():
    # OBTENGO EL TIPO DE DOCUMENTO SELECCIONADO
    document = get_doc(st.session_state.doc_type)
    filename = document.get_filename()
    extension = f".{filename.split('.')[-1]}"

    # INICIALIZO EL NOMBRE DEL ARCHIVO POR DEFAULT (solo la primera vez)
    if "filename_input" not in st.session_state:
        st.session_state.filename_input = filename

    # BARRA DE NAVEGACION
    top_bar(title="", back_to="verify", show_stepper=True, step=4)

    with st.columns([1, 9, 1])[1]:
        st.success("Documento generado correctamente 🎉")
        input_value = field_row(
            label="Nombre del archivo",
            key="filename_input",
            data=st.session_state,
            col_ratio=(1, 4.5),
        )
        render_clarifications(document.get_aclaraciones())

    # SANITIZO Y ARMO EL NOMBRE FINAL
    clean_name = input_value.strip() or filename
    if not clean_name.lower().endswith(extension.lower()):
        clean_name = f"{clean_name}{extension}"

    _, col_1, col_2, _ = st.columns([1, 4.5, 4.5, 1])
    with col_1:
        if "doc_buffer" in st.session_state:
            st.download_button(
                label="Descargar documento",
                data=st.session_state.doc_buffer,
                file_name=clean_name,
                mime=document.mime,
                use_container_width=True,
                type="primary",
            )
    with col_2:
        if st.button("Generar nuevo documento", use_container_width=True, type="secondary"):
            go_to("select")


def render_clarifications(items: list[str]) -> None:
    if not items:
        return
    clarifications = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(
        f"""<div class="aclaraciones">
            <h3>⚠️ Aclaraciones</h3>
            <ul>{clarifications}</ul>
        </div>""",
        unsafe_allow_html=True,
    )