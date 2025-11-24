from fastapi import Request, Response, HTTPException
from src.Controller.Controller import Controller

class HTTPHandler:
    def __init__(self):
        self.controller = Controller() 

    async def usuarioHandler(self, request:Request, response: Response):
        data = await request.json()
        email = data["email"]
        password = data["contraseña"]
        return self.controller.get_usuario(email, password)
    
    async def crearUsuario(self, request: Request, response: Response):
        try:
            data = await request.json()

            nombre = data["nombre"]
            email = data["email"]
            contraseña = data["contraseña"]

            self.controller.crear_usuario(nombre, email, contraseña)

            response.status_code = 201
            return {
                "success": True,
                "message": "Usuario creado correctamente"
            }

        except Exception as e:
            response.status_code = 500
            return {"success": False, "error": str(e)}
    
    def categoriasHandler(self, request: Request, response: Response):
        return self.controller.get_categorias()
    
    def bazarHandler(self, categorias: str, response: Response):
        return self.controller.get_bazar(categorias)

    async def solicitudHandler(self, data: dict, response: Response):
        Lista_fotos = data["Lista_fotos"]
        UsuarioID = data["usuarioid"]
        BazarID = data["bazarid"]
        descripcion = data["descripcion"]
        categoriaID = data["categoria"]
        return self.controller.crear_solicitud(Lista_fotos, UsuarioID, BazarID, descripcion, categoriaID)
    
    async def historialHandler(self, request: Request, response: Response):
        data = await request.json()
        name = data["nombre"]
        return self.controller.historial_donaciones(name)
    
    def pendientesHandler(self, request: Request, response: Response):
        return self.controller.solicitudes_pendientes()
    
    async def estadoHandler(self, request: Request, response: Response):
        data = await request.json()
        folio = data["folio"]
        decision = data["decicion"]
        self.controller.cambiar_estado_solicitud(folio, decision)
        return {"success": True}
    
    def SolicitudesAceptadasHandler(self, request: Request, response: Response):
        return self.controller.solicitudes_aceptadas()
    
