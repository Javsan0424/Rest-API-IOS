from fastapi import FastAPI, Request, Response, APIRouter
from src.Handler.HTTPHandler import HTTPHandler
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import Usuario, CrearUsuario, CrearSolicitud, Historial, CambiarEstado

print(">>> ESTE ES EL ARCHIVO QUE FASTAPI ESTÁ USANDO <<<")


app = FastAPI()
router = APIRouter()
handler = HTTPHandler()

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
    return await handler.solicitudHandler(crearSolicitud, response)

@router.post("/historial", status_code=201)
def historial_route(historial: Historial, response: Response):
    return  handler.historialHandler(historial, response)

@router.get("/pendientes", status_code=201)
def pendientes_route(request: Request, response: Response):
    return handler.pendientesHandler(request, response)

@router.post("/estado", status_code=201)
async def estado_route(cambiarEstado: CambiarEstado, response: Response):
    return handler.estadoHandler(cambiarEstado, response)

@router.get("/aceptado", status_code=201)
async def aceptado_route(request: Request, response: Response):
    return handler.SolicitudesAceptadasHandler(request, response)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello "}