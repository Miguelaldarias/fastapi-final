from pydantic import BaseModel
from typing import Optional

class EntrenadorBase(BaseModel):
    nombre: str
    email: str
    edad: int
    DNI: str
    especialidades: str
    años_experiencia: int

class EntrenadorCreate(EntrenadorBase):
    contraseña: str

class Entrenador(EntrenadorBase):
    id: int

    class Config:
        from_attributes = True
