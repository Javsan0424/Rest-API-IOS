from fastapi import FastAPI, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel          # 👈 NUEVO
from src.Handler.HTTPHandler import HTTPHandler

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

# 👇👇 MODELOS Pydantic PARA LOS BODIES 👇👇
class LoginBody(BaseModel):
    email: str
    contraseña: str

class CrearSolicitudBody(BaseModel):
    Lista_fotos: list[str]
    usuarioid: int
    bazarid: int
    descripcion: str
    categoria: int
# ☝️ estos nombres deben coincidir con los que usa tu handler / Supabase

# Rutas
# ⛔ login no debe ser GET si quieres mandar JSON, cámbialo a POST
@router.post("/usuario")
async def usuario_route(body: LoginBody, response: Response):
    # body ya viene validado con .email y .contraseña
    return await handler.usuarioHandler(body.model_dump(), response)

@router.put("/crearusuario")
async def crearusuario_route(request: Request, response: Response):
    return await handler.crearUsuario(request, response)

@router.get("/categorias")
def categorias_route(request: Request, response: Response):
    return handler.categoriasHandler(request, response)

@router.get("/bazar")
def bazar_route(categorias: str, response: Response):
    return handler.bazarHandler(categorias, response)

@router.post("/solicitud")
async def solicitud_route(body: CrearSolicitudBody, response: Response):
    # body.dict() le pasa un dict limpio a tu handler
    return await handler.solicitudHandler(body.dict(), response)

@router.post("/historial")
async def historial_route(request: Request, response: Response):
    return await handler.historialHandler(request, response)

@router.get("/pendientes")
def pendientes_route(request: Request, response: Response):
    return handler.pendientesHandler(request, response)

@router.post("/estado")
async def estado_route(request: Request, response: Response):
    return await handler.estadoHandler(request, response)

@router.post("/aceptado")
async def aceptado_route(request: Request, response: Response):
    return await handler.SolicitudesAceptadasHandler(request, response)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}