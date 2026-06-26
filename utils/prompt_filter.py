import json
import logging

logger = logging.getLogger(__name__)

def filter_prompt(prompt_text: str, fields_mapping: dict, toggles: dict) -> str:
    """
    Filtra el prompt eliminando del JSON template las keys cuyos campos
    están desactivados por el usuario.
    """
    # 1) Determinar qué keys eliminar
    keys_to_remove = set()
    for label, (keys, _default) in fields_mapping.items():
        if not toggles.get(label, True):
            keys_to_remove.update(keys)
    
    if not keys_to_remove:
        logger.info("No hay campos deseleccionados, se manda el prompt completo")
        return prompt_text
    
    logger.info(f"Filtrando del prompt las keys: {sorted(keys_to_remove)}")
    
    # 2) Extraer el bloque JSON con balance de llaves
    json_block_str = _extract_json_block(prompt_text)
    if not json_block_str:
        logger.warning("No se encontró bloque JSON en el prompt, devuelvo sin modificar")
        return prompt_text
    
    # 3) Parsear el JSON
    try:
        json_block = json.loads(json_block_str)
    except json.JSONDecodeError as e:
        logger.warning(f"No se pudo parsear el JSON del prompt: {e}")
        return prompt_text
    
    # 4) Eliminar las keys no deseadas
    removed_count = 0
    for key in keys_to_remove:
        if json_block.pop(key, None) is not None:
            removed_count += 1
    
    logger.info(f"Keys removidas del JSON: {removed_count}/{len(keys_to_remove)}")
    
    # 5) Reinyectar el JSON modificado
    new_json_str = json.dumps(json_block, indent=4, ensure_ascii=False)
    modified_prompt = prompt_text.replace(json_block_str, new_json_str)
    
    # 6) Instrucción explícita al final
    excluded_keys_str = ", ".join(sorted(keys_to_remove))
    instruction = (
        f"\n\nIMPORTANTE: El usuario eligió NO generar los siguientes campos. "
        f"NO los incluyas en la respuesta JSON bajo ninguna circunstancia: {excluded_keys_str}."
    )
    modified_prompt += instruction
    
    return modified_prompt


def _extract_json_block(text: str) -> str | None:
    """
    Encuentra el primer bloque JSON balanceado en el texto.
    Recorre las llaves `{` y `}` contando balance, ignorando las que están
    dentro de strings.
    """
    # Buscar el primer { que arranca un objeto
    start = text.find("{")
    if start == -1:
        return None
    
    depth = 0
    in_string = False
    escape_next = False
    
    for i in range(start, len(text)):
        ch = text[i]
        
        if escape_next:
            escape_next = False
            continue
        
        if ch == "\\":
            escape_next = True
            continue
        
        if ch == '"':
            in_string = not in_string
            continue
        
        if in_string:
            continue
        
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    
    return None