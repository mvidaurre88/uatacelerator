import streamlit as st

# IMPORTS PROPIOS
from components.form import field_row
from docs.base import DocumentBase
from utils.verify_components import render_common_fields, render_input_list, render_section_list

class TDD(DocumentBase):
    
    extension = "xlsx"
    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    # DEVUELVE LAS ACLARACIONES A MOSTRAR EN LA PANTALLA FINAL
    def get_aclaraciones(self) -> list[str]:
        return [
            "<b>Recomedaciones:</b> Este apartado se encuentra al final del archivo y contiene una lista de posibles excepciones y errores no contemplados en los casos por ser considerados improbables o poco comunes"
            ]
        
    # DEVUELVE EL NOMBRE DEL ARCHIVO A DESCARGAR
    def get_filename(self) -> str:
        return f"TestScript.{self.extension}"
    
    def get_fields(self):
        return None
    
    def get_personalization(self):
        return None
    
    def render_form(self, data: dict) -> dict:
        
        # CAMPOS COMUNES
        render_common_fields(data)
        
        # DESCRIPCIÓN DEL BOT
        field_row("Descripción del Bot", "descripcionBot", data, multiline=True, col_ratio=(1, 6.5))
        
        # INPUTS
        inputs = data.setdefault("inputsProceso", [])
        if inputs:
            with st.container(key="form_container_inputs_tdd"):
                render_input_list("Inputs del Proceso", inputs, "inputsProceso")
        
        # PASOS
        steps = data.setdefault("pasosProceso", [])
        if steps:
            with st.container(key="form_container_steps_tdd"):
                render_section_list("Pasos del proceso",
                                    steps,
                                    "pasosProceso",
                                    "Paso",
                                    fields_config=[
                                        {"key": "numero", "label": "Número del paso"},
                                        {"key": "descripcion", "label": "Descripción del paso", "multiline": True},
                                        {"key": "excepciones", "label": "Excepciones del paso", "label_singular": "Excepción", "type": "list", "subfields": [
                                            {"key": "numero", "label": "Número de la excepción"},
                                            {"key": "descripcion", "label": "Descripción de la excepción", "multiline": True}
                                        ]},
                                    ],
                                    empty_item={"numero": "", "descripcion": "", "excepciones": []})
