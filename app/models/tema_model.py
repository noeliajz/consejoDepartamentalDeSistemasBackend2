from dataclasses import dataclass
from typing import Optional

@dataclass
class TemaModel:
    ID_Tema: Optional[int]
    ID_Expediente: Optional[int]
    ID_Reunion: Optional[int]
    ID_Comision: Optional[int]
    descripcion: str
    estado: str = "Ingresado"
    observacion: Optional[str] = None