from dataclasses import dataclass
from typing import Optional

@dataclass
class UsuarioModel:
    ID_Usuario: Optional[int]
    nombre: str
    apellido: str
    mail: str
    claustro: str
    tipo: str  # 'titular', 'suplente'
    rol: str   # 'director', 'secretaria', 'consejero'
    celular: Optional[str] = None
    estado: str = "Activo"  # 'Activo', 'Baja'
    mandato_anios: Optional[int] = None