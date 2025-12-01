from supabase import create_client, Client
from fastapi import HTTPException
from src.Security import Hash
import logging

from datetime import timedelta
from model import Token, Historial, Autenticate

# Supabase key
url = "https://ivupohirgrfpskqxhtfd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2dXBvaGlyZ3JmcHNrcXhodGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MDk3MTIsImV4cCI6MjA3NzE4NTcxMn0._E2nHBvPkbThcxZLh-WqJJlsJYkMWa7n1tDfnppO3WM"

supabase: Client = create_client(url, key)
hash = Hash()


class Controller:
    def __init__(self):
        self.supabase = supabase

    # LOGIN
    def get_usuario(self, email, password):
        try:
            response = self.supabase.table("usuario").select("*").eq("email", email).execute()

            if not response.data:
                return None

            user = response.data[0]
            hashed_password = user["password"]

            if hash.verify_password(password, hashed_password):
                access_token_expires = timedelta(minutes=hash.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = hash.create_access_token(
                    data={"sub": user["nombre"]}, expires_delta=access_token_expires
                )

                # token en el mismo formato que usa iOS
                user["token"] = Token(access_token=access_token, token_type="bearer")
                return user
            else:
                return None

        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            return None

    # REGISTRO
    def crear_usuario(self, nombre, email, password, rol="cliente"):
        try:
            response = self.supabase.table("usuario").select("*").eq("email", email).execute()

            if response.data:
                # Ya existe el correo
                raise HTTPException(409, "El email ya existe")

            hash_password = hash.get_password_hash(password)
            self.supabase.table("usuario").insert(
                {"nombre": nombre, "email": email, "password": hash_password, "rol": rol}
            ).execute()

            return {"success": True, "message": "Usuario creado correctamente"}

        except HTTPException:
            # Se propaga al handler
            raise
        except Exception as e:
            logging.error(f"Database error (crear_usuario): {str(e)}")
            raise HTTPException(500, "Error interno al crear usuario")

    # CATEGORÍAS
    def get_categorias(self):
        response = self.supabase.table("categorias").select("*").execute()
        return response.data

    # BAZAR POR CATEGORÍA
    def get_bazar(self, categorias):
        response = (
            self.supabase
            .rpc("get_bazar_by_categoria", {"cat_name": categorias})
            .select("id_bazar,nombre_bazar, ubicacion")
            .execute()
        )
        return response.data

    # CREAR SOLICITUD
    def crear_solicitud(self, fotos, usuarioid, bazarid, descripcion, categoria, estado="En proceso"):
        response = self.supabase.table("donaciones").insert(
            {
                "usuarioid": usuarioid,
                "bazarid": bazarid,
                "descripcion": descripcion,
                "categoria": categoria,
                "estado": estado,
            }
        ).execute()

        folio = response.data[0]["folio"]

        for foto in fotos:
            self.supabase.table("fotos").insert(
                {
                    "folio": folio,
                    "url": foto,
                }
            ).execute()

        # Lo que usará iOS
        return {"folio": folio, "estado": estado}

    # HISTORIAL DONADOR
    def historial_donaciones(self, historial: Historial):
        response = (
            self.supabase
            .rpc("get_historial_solicitudes", {"user_id": historial.usuarioid})
            .select("*")
            .execute()
        )
        # response.data es una lista de dicts lista para mandar a iOS
        return response.data

    # SOLICITUDES PENDIENTES (ADMIN BAZAR)
    def solicitudes_pendientes(self, autenticate: Autenticate):
        response = (
            self.supabase
            .rpc("get_solicitudes_pendientes", {"p_usuario_id": autenticate.usuarioid})
            .select("*")
            .execute()
        )
        return response.data

    # CAMBIAR ESTADO
    def cambiar_estado_solicitud(self, folio, estado):
        self.supabase.table("donaciones").update({"estado": estado}).eq("folio", folio).execute()
        return {"status": "updated"}

    # SOLICITUDES ACEPTADAS (si las usas)
    def solicitudes_aceptadas(self, autenticate: Autenticate):
        response = (
            self.supabase
            .rpc("get_solicitudes_aceptadas", {"p_usuario_id": autenticate.usuarioid})
            .select("*")
            .execute()
        )
        return response.data


