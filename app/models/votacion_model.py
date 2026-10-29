from dataclasses import dataclass
from typing import Optional

@dataclass
class VotacionModel:
    ID_Votacion: Optional[int]
    ID_Consejero: int
    ID_Tema: int
    voto: str  # 'favor', 'contra', 'abstencion'
    fecha: Optional[str] = None