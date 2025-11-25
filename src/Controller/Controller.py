from supabase import create_client, Client
from fastapi import HTTPException
import logging

url = "https://ivupohirgrfpskqxhtfd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2dXBvaGlyZ3JmcHNrcXhodGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MDk3MTIsImV4cCI6MjA3NzE4NTcxMn0._E2nHBvPkbThcxZLh-WqJJlsJYkMWa7n1tDfnppO3WM"

supabase: Client = create_client(url, key)

class Controller:
    def __init__(self):
        self.supabase = supabase
    
    #Falta agregar la autenticación
    def get_usuario(self, email, password):
        try:
            response = self.supabase.table("usuario").select("id, nombre, email, rol").eq("email", email).eq("password", password).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return None
                
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            return None
        
    def crear_usuario(self, nombre,email,password, rol = "cliente"):
        self.supabase.table("usuario").insert({"nombre":nombre,"email":email,"password":password, "rol":rol}).execute()
        
    def get_categorias(self):
        response = self.supabase.table("categorias").select("*").execute()
        return response.data 
    
    def get_bazar(self,categorias ): 
        response = self.supabase.rpc("get_bazar_by_categoria", {"cat_name": categorias}).select("id_bazar,nombre_bazar, ubicacion").execute()
        return response.data
    
    def crear_solicitud(self, fotos, usuarioid, bazarid, descripcion, categoria, estado='En proceso'):
        response = self.supabase.table("donaciones").insert({
            "usuarioid": usuarioid,
            "bazarid": bazarid,
            "descripcion": descripcion,
            "categoria": categoria,
            "estado": estado
        }).execute()
        
        folio = response.data[0]["folio"]
        
        for foto in fotos:
            self.supabase.table("fotos").insert({
                "folio": folio,
                "url": foto
            }).execute() 
        
        return {"folio": folio, "status": "created"}
    
    def historial_donaciones(self, usuarioid):
        response = self.supabase.rpc("get_historial_solicitudes",{"usuarioid": usuarioid}).select("*").execute()
        return response.data
    
    def solicitudes_pendientes(self):
        response = self.supabase.rpc("get_solicitudes_pendientes").select("*").execute()
        return response.data
    
    def cambiar_estado_solicitud(self, folio, estado):
        self.supabase.table("donaciones").update({"estado": estado}).eq("folio", folio).execute()
        return {"status": "updated"}

    def solicitudes_aceptadas(self):
        response = self.supabase.rpc("get_solicitudes_aceptadas").select("*").execute()
        return response.data
