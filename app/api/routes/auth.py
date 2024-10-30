from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from aiomysql import DictCursor
from app.database import get_db
from app.api.auth import verify_password, create_access_token
from starlette.status import HTTP_400_BAD_REQUEST
from pydantic import BaseModel

router = APIRouter()

# Esquema de datos para login
class LoginData(BaseModel):
    email: str
    contraseña: str

@router.post("/auth/login")
async def login(login_data: LoginData, db=Depends(get_db)):
    user = None
    role = None

    try:
        # Conexión a la base de datos
        async with db.cursor(DictCursor) as cursor:
            # Buscar al usuario en la tabla de Clientes
            await cursor.execute("SELECT * FROM Clientes WHERE email = %s", (login_data.email,))
            user = await cursor.fetchone()

        # Si no se encuentra en Clientes, buscar en la tabla de Entrenadores
        if not user:
            async with db.cursor(DictCursor) as cursor:
                await cursor.execute("SELECT * FROM Entrenadores WHERE email = %s", (login_data.email,))
                user = await cursor.fetchone()
                if user:
                    role = "entrenador"  # Asigna el rol de entrenador

        # Si no se encuentra ni en Clientes, ni en Entrenadores
        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email o contraseña incorrectos")

        # Verificar la contraseña
        if not verify_password(login_data.contraseña, user["contraseña"]):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email o contraseña incorrectos")

        # Asignar rol si es cliente
        if not role:
            role = "cliente"  # Asigna el rol de cliente si no es entrenador

        # Crear el token JWT
        access_token = create_access_token(data={"sub": user["email"], "role": role, "id": user["id"]})

        # Devolver el token y el rol del usuario
        return {"access_token": access_token, "role": role, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
