from dataclasses import dataclass
from typing import Optional

@dataclass
class ComisionConsejeroModel:
    ID_Comision_Consejero: Optional[int]
    ID_Comision: int
    ID_Consejero: int
    cargo: str  # Ej: 'Presidente', 'Vocal', 'Secretario'
    fechaInicio: Optional[str] = None
    fechaFin: Optional[str] = None