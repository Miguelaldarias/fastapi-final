from fastapi import FastAPI
from app.api.routes import clientes, entrenadores, rutinas, planesnutricionales, metricas, auth
from app.database import init_db_pool, close_db_pool
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api import api_router

# Definir el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio
    await init_db_pool()  # Inicializar el pool de conexiones
    yield
    # Evento de cierre
    await close_db_pool()  # Cerrar el pool de conexiones

# Inicializar la aplicación con la función de ciclo de vida
app = FastAPI(lifespan=lifespan)

# Configuración de CORS
origins = [
    "http://localhost:3000",  # Frontend en desarrollo
    "http://127.0.0.1:3000",
    "http://13.51.160.6:8000", # IP pública de tu instancia
    "http://frontend-examen-final.s3-website.eu-north-1.amazonaws.com" # Frontend de producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
