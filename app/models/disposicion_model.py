from dataclasses import dataclass
from typing import Optional

@dataclass
class DisposicionModel:
    ID_Disposicion: Optional[int]
    ID_Tema: int
    numero: str
    fecha: str
    resumen: Optional[str] = None
    archivoPdf: Optional[str] = None