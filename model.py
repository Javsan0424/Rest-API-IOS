from pydantic import BaseModel

class Usuario(BaseModel):
    email: str
    password: str

class CrearUsuario(BaseModel):
    nombre: str
    email : str
    password : str

class CrearSolicitud(BaseModel):
    usuarioid: int
    bazarid: int
    descripcion: str
    categoria: int

    fotos : list[str]

class Historial(BaseModel):
    usuarioid: int

class CambiarEstado(BaseModel):
    folio : int
    estado : str

