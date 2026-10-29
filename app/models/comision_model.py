from dataclasses import dataclass
from typing import Optional

@dataclass
class ComisionModel:
    ID_Comision: Optional[int]
    nombre: str
    descripcion: Optional[str] = None