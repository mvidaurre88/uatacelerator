# IMPORTS DE TERCEROS
import streamlit as st

# RENDERIZO EL STEPPER
def render_stepper(step):
    steps = ["Inicio", "Cargar datos", "Generar archivo", "Verificar datos", "Fin"]
    actual = step

    total = len(steps)
    width = 1000
    height = 90
    paso_w = width // total
    radio = 20

    COLOR_ACTIVO    = "#e68200"
    COLOR_COMPLETO  = "#b36500"
    COLOR_PENDIENTE = "#555555"
    COLOR_TEXTO     = "#ffffff"

    svg = f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'

    for i in range(total):
        cx = paso_w * i + paso_w // 2
        cy = height // 2 - 10

        if i < total - 1:
            next_cx = paso_w * (i + 1) + paso_w // 2
            line_color = COLOR_ACTIVO if i + 1 <= actual else COLOR_PENDIENTE
            svg += f'<line x1="{cx + radio}" y1="{cy}" x2="{next_cx - radio}" y2="{cy}" stroke="{line_color}" stroke-width="3"/>'

        if i < actual:
            color = COLOR_COMPLETO
        elif i == actual:
            color = COLOR_ACTIVO
        else:
            color = COLOR_PENDIENTE

        svg += f'<circle cx="{cx}" cy="{cy}" r="{radio}" fill="{color}"/>'
        svg += f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" fill="{COLOR_TEXTO}" font-size="15" font-family="Consolas" font-weight="bold">{i + 1}</text>'
        if i == actual:
            svg += f'<text x="{cx}" y="{cy + radio + 20}" text-anchor="middle" fill="{COLOR_TEXTO}" font-size="14" font-family="Consolas">{steps[i]}</text>'

    svg += "</svg>"

    st.markdown(f'<div style="width:100%; height:{height}px;">{svg}</div>', unsafe_allow_html=True)