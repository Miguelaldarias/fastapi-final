from fastapi import APIRouter, Depends, HTTPException
from app.api.models.rutinas import Rutina, RutinaCreate
from app.database import get_db
import aiomysql
from typing import List

router = APIRouter()

@router.post("/rutinas/")
async def create_rutina(rutina_data: RutinaCreate, db=Depends(get_db)):
    try:
        async with db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Rutinas (nombre, descripcion, cliente_id, entrenador_id) "
                "VALUES (%s, %s, %s, %s)",
                (rutina_data.nombre, rutina_data.descripcion, rutina_data.cliente_id, rutina_data.entrenador_id)
            )
            await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear rutina: {str(e)}")
    return {"message": "Rutina creada correctamente"}


@router.get("/rutinas/{cliente_id}", response_model=List[Rutina])
async def get_rutinas_cliente(cliente_id: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM Rutinas WHERE cliente_id = %s", (cliente_id,))
        result = await cursor.fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron rutinas para este cliente")
    return result