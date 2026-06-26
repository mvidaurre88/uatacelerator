from docs.base import DocumentBase
from docs.tdd import TDD

DOC_REGISTRY: dict[str, type[DocumentBase]] = {
    "TDD": TDD,
}

def get_doc(doc_type: str) -> DocumentBase:
    cls = DOC_REGISTRY.get(doc_type)
    if cls is None:
        raise ValueError(f"Tipo de documento desconocido: {doc_type}")
    return cls()