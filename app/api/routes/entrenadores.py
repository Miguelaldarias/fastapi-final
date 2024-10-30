from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.api.models.entrenadores import Entrenador, EntrenadorCreate
import aiomysql
import bcrypt  # Importamos bcrypt
from app.api.auth import get_current_user  # Si tienes autenticación implementada
from typing import List
from app.api.models.clientes import Cliente

# Definir el router
router = APIRouter()

# Función para hashear la contraseña (igual que en clientes.py)
def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@router.post("/entrenadores/")
async def create_entrenador(entrenador_data: EntrenadorCreate, db=Depends(get_db)):
    try:
        # Hasheamos la contraseña antes de guardarla
        hashed_password = hash_password(entrenador_data.contraseña)

        async with db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Entrenadores (nombre, email, contraseña, edad, DNI, especialidades, años_experiencia) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (entrenador_data.nombre, entrenador_data.email, hashed_password,
                 entrenador_data.edad, entrenador_data.DNI, entrenador_data.especialidades,
                 entrenador_data.años_experiencia)
            )
            await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear entrenador: {str(e)}")
    return {"message": "Entrenador creado correctamente"}
    

@router.get("/entrenadores/profile", response_model=Entrenador)
async def get_entrenador_profile(db: aiomysql.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM Entrenadores WHERE id = %s", (current_user["id"],))
        entrenador = await cursor.fetchone()
        if not entrenador:
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador

@router.get("/entrenadores/{entrenador_id}/clientes", response_model=List[Cliente])
async def get_clientes_asignados(entrenador_id: int, db=Depends(get_db)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM Clientes WHERE entrenador_id = %s", (entrenador_id,))
        clientes = await cursor.fetchall()
        if not clientes:
            raise HTTPException(status_code=404, detail="No hay clientes asignados a este entrenador")
    return clientes


