from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED  # Cambia el import a starlette
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.api.models.clientes import Cliente
from app.database import get_db
from passlib.context import CryptContext
import os
import aiomysql

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Usa variables de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Definir esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generar un token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Usar timezone.utc
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificar contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Crear contraseña encriptada
def get_password_hash(password):
    return pwd_context.hash(password)

# Obtener el usuario actual desde el token
async def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar el token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")  # Obtenemos el ID del usuario desde el token
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Buscamos al usuario en la base de datos usando el ID extraído del token
    async with db.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("SELECT * FROM Clientes WHERE id = %s", (user_id,))
        user = await cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user  # Retornamos el diccionario con los datos del usuario

    