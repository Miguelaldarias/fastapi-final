from fastapi import APIRouter, Depends, HTTPException
from app.api.models.metricas import Metrica, MetricaCreate
from app.database import get_db
import aiomysql
from typing import List


router = APIRouter()

@router.post("/metricas/")
async def create_metrica(metrica_data: MetricaCreate, db=Depends(get_db)):
    try:
        async with db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Metricas (cliente_id, peso, grasa_corporal, rendimiento, informe) "
                "VALUES (%s, %s, %s, %s, %s)",
                (metrica_data.cliente_id, metrica_data.peso, metrica_data.grasa_corporal,
                 metrica_data.rendimiento, metrica_data.informe)
            )
            await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear métrica: {str(e)}")
    return {"message": "Métrica creada correctamente"}


@router.get("/metricas/{cliente_id}", response_model=List[Metrica])
async def get_metricas_cliente(cliente_id: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM Metricas WHERE cliente_id = %s", (cliente_id,))
        result = await cursor.fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron métricas para este cliente")
    return result
