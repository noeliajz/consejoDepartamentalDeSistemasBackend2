from dataclasses import dataclass
from typing import Optional

@dataclass
class NotificacionModel:
    ID_Notificacion: Optional[int]
    ID_Usuario: int
    fecha: str
    contenido: str
    leido: bool = False