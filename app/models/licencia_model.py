from dataclasses import dataclass
from typing import Optional

@dataclass
class LicenciaModel:
    ID_Licencia: Optional[int]
    ID_Consejero: int
    fechaInicio: str
    fechaFin: str
    motivo: Optional[str] = None
    estado: str = "Pendiente"