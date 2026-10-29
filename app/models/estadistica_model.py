from dataclasses import dataclass
from typing import Optional

@dataclass
class EstadisticaModel:
    ID_Estadistica: Optional[int]
    tipo: str
    valor: float
    fechaCalculo: str