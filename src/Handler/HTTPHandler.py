from fastapi import Request, Response
from src.Controller.Controller import Controller

class HTTPHandler:
    def __init__(self):
        self.controller = Controller() 
    
    def usuarioHandler(self, usuario, response: Response):
        try:            
            result = self.controller.get_usuario(usuario.email, usuario.password) 
            if result:
                return {
                    "success": True,
                    "data": result,
                    "message": "Login successful"
                }
            else:
                print("DEBUG: Login failed - no user found or invalid credentials")
                response.status_code = 401
                return {
                    "success": False,
                    "message": "Invalid email or password"
                }
                
        except Exception as e:
            print(f"DEBUG: Exception occurred: {str(e)}")
            response.status_code = 500
            return {
                "success": False,
                "message": f"Internal server error: {str(e)}"
            }
    
    async def crearUsuario(self, request: Request, response: Response):
        try:
            data = await request.json()
            nombre = data["nombre"]
            email = data["email"]
            contraseña = data["contraseña"]
            return self.controller.crear_usuario(nombre,email,contraseña)
        
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500

    def categoriasHandler(self, request: Request, response: Response):
        return self.controller.get_categorias()
    
    def bazarHandler(self, categorias: str, response: Response):
        return self.controller.get_bazar(categorias)
    
    async def solicitudHandler(self, request: Request, response: Response):
        try:
            data = await request.json()
            Lista_fotos = data["Lista_fotos"]
            UsuarioID = data["usuarioid"]
            BazarID = data["bazarid"]
            descripcion = data["descripcion"]
            categoriaID = data["categoria"]
            return self.controller.crear_solicitud(Lista_fotos, UsuarioID, BazarID, descripcion, categoriaID)
        
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
    
    async def historialHandler(self, request: Request, response: Response):
        try: 
            data = await request.json()
            name = data["nombre"]
            return self.controller.historial_donaciones(name)
        
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
    
    def pendientesHandler(self, request: Request, response: Response):
        return self.controller.solicitudes_pendientes()
    
    async def estadoHandler(self, request: Request, response: Response):
        try: 
            data = await request.json()
            folio = data["folio"]
            decision = data["decicion"]
            self.controller.cambiar_estado_solicitud(folio, decision)
            return {"success": True}
    
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            
    def SolicitudesAceptadasHandler(self, request: Request, response: Response):
        return self.controller.solicitudes_aceptadas()
    
