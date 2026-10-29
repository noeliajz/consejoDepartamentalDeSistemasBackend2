from dataclasses import dataclass
from typing import Optional

@dataclass
class AsistenciaModel:
    ID_Asistencia: Optional[int]
    ID_Reunion: int
    ID_Consejero: int
    asistio: bool = True
    justificada: bool = False
    observacion: Optional[str] = None