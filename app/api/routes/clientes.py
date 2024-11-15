from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.api.models.clientes import Cliente, ClienteCreate
from pydantic import BaseModel
import aiomysql
import bcrypt
from app.api.auth import get_current_user  # autenticación implementada


router = APIRouter()

# Función para hashear la contraseña
def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt(rounds=14)).decode('utf-8')

# Ruta para crear un nuevo cliente
@router.post("/clientes/")
async def create_cliente(cliente_data: ClienteCreate, db=Depends(get_db)):
    try:
        hashed_password = hash_password(cliente_data.contraseña)
        async with db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Clientes (nombre, email, contraseña, edad, peso, grasa_corporal, objetivo, entrenador_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (cliente_data.nombre, cliente_data.email, hashed_password,
                 cliente_data.edad, cliente_data.peso, cliente_data.grasa_corporal,
                 cliente_data.objetivo, cliente_data.entrenador_id)
            )
            await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear cliente: {str(e)}")
    return {"message": "Cliente creado correctamente"}

# Ruta para obtener el perfil de un cliente
@router.get("/clientes/profile", response_model=Cliente)
async def get_cliente_profile(db: aiomysql.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM Clientes WHERE id = %s", (current_user["id"],))
        cliente = await cursor.fetchone()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Ruta para obtener el perfil de un cliente
@router.get("/clientes/{cliente_id}", response_model=Cliente)
async def get_cliente_profile(cliente_id: int, db: aiomysql.Connection = Depends(get_db), current_user: Cliente = Depends(get_current_user)):
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM Clientes WHERE id = %s", (cliente_id,))
        cliente = await cursor.fetchone()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente 
