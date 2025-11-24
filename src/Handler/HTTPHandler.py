from fastapi import Request, Response
from src.Controller.Controller import Controller

class HTTPHandler:
    def __init__(self):
        self.controller = Controller() 
    
    from fastapi import HTTPException # Asumiendo FastAPI o similar

    async def usuarioHandler(self, request: Request, response: Response):
        try:
            data = await request.json()
            email = data.get("email")
            password = data.get("contraseña")

            if not email or not password:
                response.status_code = 400
                return {"success": False, "message": "Faltan datos"}

            result = await self.controller.get_usuario(email, password)
            
            if not result["success"]:
                response.status_code = 401 
            return result

        except Exception as e:
            response.status_code = 500
            return {"success": False, "message": str(e)}
    
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
    
    async def solicitudHandler(self, request: Request, response: Response):
        data = await request.json()
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
    
