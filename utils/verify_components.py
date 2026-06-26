import streamlit as st
from components.form import field_row
import base64
import uuid

# RENDERIZA UNA LISTA DE INPUTS
def render_input_list(title, items, field, multiline=False):
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            items[i] = {"value": item, "_id": str(uuid.uuid4())}
    
    st.markdown(f"<p class='container-title'>{title}</p>", unsafe_allow_html=True)
    
    to_delete = None
    for item in items:
        if "_id" not in item:
            item["_id"] = str(uuid.uuid4())
        uid = item["_id"]
        
        col_field, col_btn = st.columns([20, 1], vertical_alignment="center")
        with col_field:
            field_row(label=None, key="value", data=item, key_prefix=f"{field}_{uid}_", multiline=multiline)
        with col_btn:
            if st.button("✕", key=f"del_{field}_{uid}"):
                to_delete = uid
    
    if to_delete is not None:
        items[:] = [e for e in items if e["_id"] != to_delete]
        st.rerun()
    
    if st.button(f"+ Agregar", key=f"add_{field}"):
        items.append({"_id": str(uuid.uuid4()), "value": ""})
        st.rerun()

# RENDERIZA UNA LISTA DE SECCIONES
def render_section_list(title, items, field, item_label, fields_config, empty_item):
    
    st.markdown(f"<p class='container-title'>{title}</p>", unsafe_allow_html=True)
    
    to_delete = None
    for i, item in enumerate(items):
        if "_id" not in item:
            item["_id"] = str(uuid.uuid4())
        uid = item["_id"]
        
        with st.container(key=f"section_item_{field}_{uid}"):
            col_expander, col_btn = st.columns([20, 1], vertical_alignment="top")
            with col_expander:
                with st.expander(f"{item_label} {i + 1}", expanded=True):
                    for fc in fields_config:
                        if fc.get("type") == "list":
                            sublist = item.setdefault(fc["key"], [])
                            _render_inline_list(sublist, fc, parent_field=field, parent_uid=uid, parent_index=i + 1)
                        else:
                            field_row(fc["label"], fc["key"], item, key_prefix=f"{field}_{uid}_{fc['key']}", multiline=fc.get("multiline", False))
            with col_btn:
                if st.button("✕", key=f"del_{field}_{uid}", type="secondary"):
                    to_delete = uid
    
    if to_delete is not None:
        items[:] = [t for t in items if t["_id"] != to_delete]
        st.rerun()
    
    if st.button(f"+ Agregar {item_label.lower()}", key=f"add_{field}", type="secondary"):
        new_item = {"_id": str(uuid.uuid4()), **empty_item}
        items.append(new_item)
        st.rerun()

# RENDERIZA CAMPOS COMUNES
def render_common_fields(data):
    
    # CODIGO Y NOMBRE DEL BOT
    double_field_row("Código del Bot", "codigoBot", "Nombre del Bot", "nombreBot", data)

    # CLIENTE Y DESARROLLADOR
    double_field_row("Cliente", "cliente", "Desarrollador", "desarrollador", data)
    
    # VERSION Y FECHA
    double_field_row("Versión", "version", "Fecha", "fecha", data)
    
    # MODIFICACIÓN ACTUAL
    modificaciones = data.get("modificaciones", [])
    if modificaciones:
        with st.container(key="form_container"):
            st.markdown("<p class='container-title'>Modificación Actual</p>", unsafe_allow_html=True)            
            double_field_row("Versión", "version", "Fecha", "fecha", modificaciones[-1], key_prefix="mod_last_", inContainer=True)
            double_field_row("Sector", "sector", "Autor", "autor", modificaciones[-1], key_prefix="mod_last_", inContainer=True)
            field_row("Motivo modificación", "motivo", modificaciones[-1], multiline=True, key_prefix="mod_last_")

# RENDERIZA DIAGRAMAS
def show_img_overlay(img_bytes, key="overlay"):
    if not img_bytes:
        return
    @st.dialog("Diagrama", width="large")
    def show_diagram_dialog(img_bytes):
        img_base64 = base64.b64encode(img_bytes).decode()
        html = f"""
            <div id="container" style="overflow: auto; max-height: 75vh;">
                <img id="zoom_img" src="data:image/png;base64,{img_base64}" 
                    style="height: 75vh; display: block; margin: 0 auto; transition: transform 0.05s; transform-origin: top left;"/>
            </div>
            <script>
                const img = document.getElementById('zoom_img');
                const container = document.getElementById('container');
                let scale = 1;

                container.addEventListener('wheel', (e) => {{
                    e.preventDefault();
                    scale = Math.min(Math.max(1, scale - e.deltaY * 0.002), 5);
                    img.style.transform = `scale(${{scale}})`;
                }}, {{ passive: false }});
            </script>
        """
        st.iframe(html, height=600)
        
    if st.button("Ver", key=f"btn_{key}", type="secondary"):
        show_diagram_dialog(img_bytes)
    
    
# RENDERIZA UNA LISTA DENTRO DE UNA SECCION
def _render_inline_list(items, fc, parent_field, parent_uid, parent_index=None):
    subfield = fc["key"]
    label = fc["label"]
    label_singular = fc.get("label_singular", label)
    subfields = fc.get("subfields")
    key_prefix_base = f"{parent_field}_{parent_uid}_{subfield}"
    
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            items[i] = {"value": item, "_id": str(uuid.uuid4())}
    
    to_delete = None
    for i, subitem in enumerate(items):
        if "_id" not in subitem:
            subitem["_id"] = str(uuid.uuid4())
        uid = subitem["_id"]
        
        # numeración jerárquica
        if parent_index is not None:
            sub_label = f"{label_singular} {parent_index}.{i + 1}"
        else:
            sub_label = f"{label_singular} {i + 1}"
        
        if subfields:
            with st.container(key=f"inline_item_{key_prefix_base}_{uid}"):
                col_exp, col_btn = st.columns([20, 1], vertical_alignment="top")
                with col_exp:
                    with st.expander(sub_label, expanded=False):
                        for sf in subfields:
                            field_row(
                                sf["label"],
                                sf["key"],
                                subitem,
                                key_prefix=f"{key_prefix_base}_{uid}_",
                                multiline=sf.get("multiline", False)
                            )
                with col_btn:
                    if st.button("✕", key=f"del_{key_prefix_base}_{uid}"):
                        to_delete = uid
        else:
            col_field, col_btn = st.columns([6, 1], vertical_alignment="center")
            with col_field:
                field_row(
                    label=None,
                    key="value",
                    data=subitem,
                    key_prefix=f"{key_prefix_base}_{uid}_",
                    multiline=fc.get("multiline", True)
                )
            with col_btn:
                if st.button("✕", key=f"del_{key_prefix_base}_{uid}"):
                    to_delete = uid
    
    if to_delete is not None:
        items[:] = [s for s in items if s["_id"] != to_delete]
        st.rerun()
    
    if st.button(f"+ Agregar", key=f"add_{key_prefix_base}"):
        if subfields:
            new_item = {"_id": str(uuid.uuid4())}
            for sf in subfields:
                new_item[sf["key"]] = [] if sf.get("type") == "list" else ""
        else:
            new_item = {"_id": str(uuid.uuid4()), "value": ""}
        items.append(new_item)
        st.rerun()
    
# FUNCION PARA ESTANDARIZAR FILAS DE DOS CAMPOS
def double_field_row(label1, key1, label2, key2, data, key_prefix="", multiline=False, inContainer=False):
    if inContainer:
        col_left, col_right = st.columns([1, 1])
        with col_left:
            field_row(label1, key1, data, key_prefix=key_prefix, multiline=multiline)
        with col_right:
            field_row(label2, key2, data, key_prefix=key_prefix, multiline=multiline)
    else:
        with st.container(key=f"double_{key_prefix}_{key1}_{key2}"):
            col_left, col_right = st.columns([1, 1])
            with col_left:
                field_row(label1, key1, data, key_prefix=key_prefix, multiline=multiline)
            with col_right:
                field_row(label2, key2, data, key_prefix=key_prefix, multiline=multiline)