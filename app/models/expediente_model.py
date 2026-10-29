from dataclasses import dataclass
from typing import Optional

@dataclass
class ExpedienteModel:
    ID_Expediente: Optional[int]
    ID_Comision: Optional[int]
    descripcion: str
    categoria: Optional[str] = None
    despacho: bool = False
    fechaCreacion: Optional[str] = None
    responsable: Optional[str] = None
    estado: str = "Ingresado"
    fechaIngresoConsejo: Optional[str] = None
    fechaTratamiento: Optional[str] = None
    fechaSalida: Optional[str] = None
    destinoSalida: Optional[str] = None