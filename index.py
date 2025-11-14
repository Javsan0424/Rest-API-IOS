from fastapi import FastAPI, Request, Response, APIRouter
from src.Handler.HTTPHandler import HTTPHandler
from fastapi.middleware.cors import CORSMiddleware

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
@router.post("/usuario")
async def usuario_route(request: Request, response: Response):
    return await handler.usuarioHandler(request, response)

@router.put("/crearusuario")
async def crearusuario_route(request: Request, response: Response):
    return await handler.crearUsuario(request, response)

@router.get("/categorias")
def categorias_route(request: Request, response: Response):
    return handler.categoriasHandler(request, response)

@router.get("/bazar" )
def bazar_route(categorias: str, response: Response):
    return handler.bazarHandler(categorias, response)

@router.post("/solicitud")
async def solicitud_route(request: Request, response: Response):
    return await handler.solicitudHandler(request, response)

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

aceptado_route()