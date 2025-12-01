from fastapi import Request, Response
from src.Controller.Controller import Controller
from model import Usuario, CrearUsuario, CrearSolicitud, Historial, CambiarEstado, Autenticate


class HTTPHandler:
    def __init__(self):
        self.controller = Controller()

    # LOGIN
    def usuarioHandler(self, usuario: Usuario, response: Response):
        try:
            result = self.controller.get_usuario(usuario.email, usuario.password)
            if result:
                return {
                    "success": True,
                    "data": result,
                    "message": "Login successful",
                }
            else:
                response.status_code = 401
                return {
                    "success": False,
                    "message": "Invalid email or password",
                }
        except Exception as e:
            print(f"DEBUG: Exception occurred: {str(e)}")
            response.status_code = 500
            return {
                "success": False,
                "message": f"Internal server error: {str(e)}",
            }

    # REGISTRO
    def crearUsuario(self, crearUsuario: CrearUsuario, response: Response):
        try:
            result = self.controller.crear_usuario(
                crearUsuario.nombre,
                crearUsuario.email,
                crearUsuario.password,
            )
            return result
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            # Si es HTTPException, FastAPI ya pone el código
            response.status_code = getattr(e, "status_code", 500)
            return {"success": False, "error": str(e)}

    # CATEGORÍAS (devuelve lista simple, sin wrapper)
    def categoriasHandler(self, request: Request, response: Response):
        return self.controller.get_categorias()

    # BAZARES (lista simple, sin wrapper)
    def bazarHandler(self, categorias: str, response: Response):
        return self.controller.get_bazar(categorias)

    # CREAR SOLICITUD
    def solicitudHandler(self, crearSolicitud: CrearSolicitud, response: Response):
        try:
            result = self.controller.crear_solicitud(
                crearSolicitud.fotos,
                crearSolicitud.usuarioid,
                crearSolicitud.bazarid,
                crearSolicitud.descripcion,
                crearSolicitud.categoria,
            )
            return {
                "success": True,
                "data": result,
                "message": "Solicitud creada correctamente",
            }
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}

    # HISTORIAL DONADOR  ->  { success, data:[...] }
    def historialHandler(self, historial: Historial, response: Response):
        try:
            data = self.controller.historial_donaciones(historial)
            return {"success": True, "data": data}
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}

    # PENDIENTES ADMIN BAZAR  -> { success, data:[...] }
    def pendientesHandler(self, autenticate: Autenticate, response: Response):
        try:
            data = self.controller.solicitudes_pendientes(autenticate)
            return {"success": True, "data": data}
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}

    # CAMBIAR ESTADO
    def estadoHandler(self, cambiarEstado: CambiarEstado, response: Response):
        try:
            data = self.controller.cambiar_estado_solicitud(
                cambiarEstado.folio,
                cambiarEstado.estado,
            )
            return {"success": True, "data": data}
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}

    # SOLICITUDES ACEPTADAS  -> { success, data:[...] }
    def SolicitudesAceptadasHandler(self, autenticate: Autenticate, response: Response):
        try:
            data = self.controller.solicitudes_aceptadas(autenticate)
            return {"success": True, "data": data}
        except Exception as e:
            print(f"Debug: Exception occured: {str(e)}")
            response.status_code = 500
            return {"success": False, "error": str(e)}