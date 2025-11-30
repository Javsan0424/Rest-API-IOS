from pydantic import BaseModel

#Authentication classes
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

#Modelos para la App

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

    #Para autenticar
    token : Token
    nombre: str

class Historial(BaseModel):
    usuarioid: int

    #Para autenticar
    token : Token
    nombre: str

class CambiarEstado(BaseModel):
    folio : int
    estado : str

    #Para autenticar
    token : Token
    nombre: str


#Para pendientes y aceptados
class Autenticate(BaseModel):
    token: Token
    nombre: str