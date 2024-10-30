from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlanNutricionalBase(BaseModel):
    nombre: str
    descripcion: str
    cliente_id: int
    entrenador_id: int

class PlanNutricionalCreate(PlanNutricionalBase):
    pass

class PlanNutricional(PlanNutricionalBase):
    id: int
    fecha_asignacion: Optional[datetime]

    class Config:
        from_attributes = True
