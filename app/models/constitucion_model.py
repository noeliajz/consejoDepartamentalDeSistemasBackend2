from dataclasses import dataclass
from typing import Optional

@dataclass
class ConstitucionModel:
    ID_Constitucion: Optional[int]
    ID_Reunion: int
    ID_Comision: int
    fecha: str