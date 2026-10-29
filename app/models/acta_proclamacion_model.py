from dataclasses import dataclass
from typing import Optional

@dataclass
class ActaProclamacionModel:
    ID_ActaProclamacion: Optional[int]
    ID_Consejero: int
    fechaProclamacion: str
    observaciones: Optional[str] = None