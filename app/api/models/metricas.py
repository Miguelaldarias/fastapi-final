from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetricaBase(BaseModel):
    cliente_id: int
    peso: float
    grasa_corporal: float
    rendimiento: str
    informe: Optional[str]

class MetricaCreate(MetricaBase):
    pass

class Metrica(MetricaBase):
    id: int
    fecha_registro: Optional[datetime]

    class Config:
        from_attributes = True
