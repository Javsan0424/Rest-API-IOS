from fastapi import Request, Response
from src.Controller.Controller import Controller
from model import Usuario, CrearUsuario, CrearSolicitud, Historial, CambiarEstado

class HTTPHandler:
    def __init__(self):
        self.controller = Controller() 
    
    def usuarioHandler(self, usuario: Usuario, response: Response):
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

    def crearUsuario(self, crearUsuario: CrearUsuario, response: Response):
        try:
            return self.controller.crear_usuario(
                crearUsuario.nombre,
                crearUsuario.email,
                crearUsuario.password
            )
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}

    def categoriasHandler(self, request: Request, response: Response):
        return self.controller.get_categorias()
    
    def bazarHandler(self, categorias: str, response: Response):
        return self.controller.get_bazar(categorias)
    
    def solicitudHandler(self, crearSolicitud: CrearSolicitud, response: Response):
        try:
            self.controller.crear_solicitud(
                crearSolicitud.fotos,
                crearSolicitud.usuarioid,
                crearSolicitud.bazarid,
                crearSolicitud.descripcion,
                crearSolicitud.categoria
            )
            return {"success": True}
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}
    
    def historialHandler(self, historial: Historial, response: Response):
        try: 
            return self.controller.historial_donaciones(historial)
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}
    
    def pendientesHandler(self, request: Request, response: Response):
        return self.controller.solicitudes_pendientes()
    
    def estadoHandler(self, cambiarEstado: CambiarEstado, response: Response):
        try:
            return self.controller.cambiar_estado_solicitud(
                cambiarEstado.folio,
                cambiarEstado.estado
            )
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}
            
    def SolicitudesAceptadasHandler(self, request: Request, response: Response):
        return self.controller.solicitudes_aceptadas()