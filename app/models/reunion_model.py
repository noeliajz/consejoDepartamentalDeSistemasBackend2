from dataclasses import dataclass
from typing import Optional

@dataclass
class ReunionModel:
    ID_Reunion: Optional[int]
    fecha: str
    hora: Optional[str] = None
    lugar: Optional[str] = None
    tipo: str = "Ordinaria"  # 'Ordinaria', 'Extraordinaria'
    estado: str = "Programada"