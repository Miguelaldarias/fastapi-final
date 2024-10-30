from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RutinaBase(BaseModel):
    nombre: str
    descripcion: str
    cliente_id: int
    entrenador_id: int

class RutinaCreate(RutinaBase):
    pass

class Rutina(RutinaBase):
    id: int
    fecha_asignacion: Optional[datetime]

    class Config:
        from_attributes = True
