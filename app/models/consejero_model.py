from dataclasses import dataclass
from typing import Optional

@dataclass
class ConsejeroModel:
    ID_Consejero: Optional[int]
    ID_Usuario: int