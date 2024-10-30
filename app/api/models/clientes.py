from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    email: str
    edad: int
    peso: float
    grasa_corporal: float
    objetivo: str
    entrenador_id: Optional[int] = None

class ClienteCreate(ClienteBase):
    contraseña: str 

class Cliente(ClienteBase):
    id: int
    

    class Config:
        from_attributes = True
