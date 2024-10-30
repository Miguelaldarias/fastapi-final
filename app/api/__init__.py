from fastapi import APIRouter
from .routes import clientes, entrenadores,rutinas, metricas, planesnutricionales,auth
#from django.contrib import auth

api_router = APIRouter()
api_router.include_router(clientes.router, tags=["clientes"])
api_router.include_router(entrenadores.router, tags=["entrenadores"])
api_router.include_router(metricas.router, tags=["metricas"])
api_router.include_router(planesnutricionales.router, tags=["planesnutricionales"])
api_router.include_router(rutinas.router, tags=["rutinas"])
api_router.include_router(auth.router, tags=["login"])
