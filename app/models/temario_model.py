from dataclasses import dataclass
from typing import Optional

@dataclass
class TemarioModel:
    ID_TemarioProvisorio: Optional[int]
    ID_Reunion: int
    estado: str
    fechaCreacion: str
    descripcion: Optional[str] = None