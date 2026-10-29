from dataclasses import dataclass
from typing import Optional

@dataclass
class CitacionModel:
    ID_Citacion: Optional[int]
    ID_Reunion: int
    ID_Consejero: int
    fechaEnvio: str
    estado: str = "Enviado"  # 'Enviado', 'Notificado', 'Confirmado'