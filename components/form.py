# IMPORTS DE TERCEROS
import streamlit as st
from st_keyup import st_keyup

# CONSTANTES
DEFAULT_COL_RATIO = (1, 2)
KEYUP_DEBOUNCE_MS = 400

def _render_input(key: str, value: str, multiline: bool, height: int | None) -> str:
    """Renderiza el widget de input correspondiente."""
    if multiline:
        return st.text_area(
            " ", value=value, key=key,
            label_visibility="collapsed")
    result = st_keyup(label="", value=value, key=key, debounce=KEYUP_DEBOUNCE_MS)
    return result if result is not None else value


def field_row(
    label: str | None,
    key: str,
    data: dict | None,
    col_ratio: tuple[float, float] | None = None,
    multiline: bool = False,
    height: int | None = None,
    key_prefix: str = "",
    only_input: bool = False,
) -> str:

    if data is None:
        data = {}

    value = data.get(key, "") or ""
    widget_key = f"field_{key_prefix}{key}"

    if label is None:
        data[key] = _render_input(widget_key, value, multiline, height)
        return data[key]

    col_label, col_input = st.columns(col_ratio or DEFAULT_COL_RATIO)
    if only_input:
        with col_label:
            st.markdown(f"<p class='field-label' style='padding-left:20px;'><b>{label}</b></p>", unsafe_allow_html=True,)
    else:
        with col_label:
            st.markdown(f"<p class='field-label'><b>{label}</b></p>", unsafe_allow_html=True,)
    with col_input:
        data[key] = _render_input(widget_key, value, multiline, height)

    return data[key]