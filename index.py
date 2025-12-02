from fastapi import FastAPI, Request, Response, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from src.Handler.HTTPHandler import HTTPHandler
from fastapi.middleware.cors import CORSMiddleware
from model import Usuario, CrearUsuario, CrearSolicitud, Historial, CambiarEstado, Token, TokenData, Autenticate

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model import Historial, Token
import src.Security

app = FastAPI()
router = APIRouter()
handler = HTTPHandler()
hash = src.Security.Hash()

origins = [
    "https://javsan0424.github.io/Rest-API-IOS",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

#Rutas
@router.post("/usuario", status_code=201)
def usuario_route(usuario: Usuario, response: Response):
    return handler.usuarioHandler(usuario, response)

@router.put("/crearusuario", status_code=201)
async def crearusuario_route(crearUsuario: CrearUsuario, response: Response):
    return handler.crearUsuario(crearUsuario, response)

@router.get("/categorias", status_code=201)
def categorias_route(request: Request, response: Response):
    return handler.categoriasHandler(request, response)

@router.get("/bazar", status_code=201 )
def bazar_route(categorias: str, response: Response):
    return handler.bazarHandler(categorias, response)

@router.post("/solicitud", status_code=201)
async def solicitud_route(crearSolicitud: CrearSolicitud, response: Response):
    if not await hash.get_current_user(crearSolicitud.token, crearSolicitud.nombre):
        raise HTTPException(status_code=401, detail="Invalid credentials")   
    return handler.solicitudHandler(crearSolicitud, response)

@router.post("/historial", status_code=201)
async def historial_route(historial: Historial, response: Response):
    if not await hash.get_current_user(historial.token, historial.nombre):
        raise HTTPException(status_code=401, detail="Invalid credentials")   
    return handler.historialHandler(historial, response)

@router.post("/pendientes", status_code=201)
async def pendientes_route(autenticate: Autenticate, response: Response):
    if not await hash.get_current_user(autenticate.token, autenticate.nombre):
        raise HTTPException(status_code=401, detail="Invalid credentials") 
    return handler.pendientesHandler(autenticate, response)

@router.post("/estado", status_code=201)
async def estado_route(cambiarEstado: CambiarEstado, response: Response):
    if not await hash.get_current_user(cambiarEstado.token, cambiarEstado.nombre):
        raise HTTPException(status_code=401, detail="Invalid credentials") 
    return handler.estadoHandler(cambiarEstado, response)

@router.post("/aceptado", status_code=201)
async def aceptado_route(autenticate: Autenticate, response: Response):
    if not await hash.get_current_user(autenticate.token, autenticate.nombre):
        raise HTTPException(status_code=401, detail="Invalid credentials") 
    return handler.SolicitudesAceptadasHandler(autenticate, response)
 
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello "}