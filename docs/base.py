from abc import ABC, abstractmethod

class DocumentBase(ABC):

    extension: str = "docx"
    mime: str = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    @abstractmethod
    def render_form(self, data: dict) -> dict:
        ...
        
    @abstractmethod
    def get_aclaraciones(self) -> list[str]:
        ...

    @abstractmethod
    def get_filename(self) -> str:
        ...
        
    @abstractmethod
    def get_fields(self) -> dict[str, tuple[list[str], bool]]:
        ...    
        
    @abstractmethod
    def get_personalization(self) -> dict:
        ...
        
    