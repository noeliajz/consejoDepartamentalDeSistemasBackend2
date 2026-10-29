from dataclasses import dataclass
from typing import Optional

@dataclass
class ActaReunionModel:
    ID_Acta: Optional[int]
    ID_Reunion: int
    fechaGeneracion: str
    estado: int = 0  # 0: Pendiente, 1: Aprobada/Firmada
    contenido: Optional[str] = None