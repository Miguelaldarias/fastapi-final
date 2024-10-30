from fastapi import APIRouter, Depends, HTTPException
from app.api.models.planesnutricionales import PlanNutricional, PlanNutricionalCreate
from app.database import get_db
import aiomysql
from typing import List

router = APIRouter()

@router.post("/planesnutricionales/")
async def create_plan_nutricional(plan_data: PlanNutricionalCreate, db=Depends(get_db)):
    try:
        async with db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO PlanesNutricionales (nombre, descripcion, cliente_id, entrenador_id) "
                "VALUES (%s, %s, %s, %s)",
                (plan_data.nombre, plan_data.descripcion, plan_data.cliente_id, plan_data.entrenador_id)
            )
            await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear plan nutricional: {str(e)}")
    return {"message": "Plan nutricional creado correctamente"}

@router.get("/planesnutricionales/{cliente_id}", response_model=List[PlanNutricional])
async def get_planes_cliente(cliente_id: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM PlanesNutricionales WHERE cliente_id = %s", (cliente_id,))
        result = await cursor.fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron planes nutricionales para este cliente")
    return result