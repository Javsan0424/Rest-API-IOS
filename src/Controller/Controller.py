from supabase import create_client, Client

url = "https://ivupohirgrfpskqxhtfd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2dXBvaGlyZ3JmcHNrcXhodGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MDk3MTIsImV4cCI6MjA3NzE4NTcxMn0._E2nHBvPkbThcxZLh-WqJJlsJYkMWa7n1tDfnppO3WM"

supabase: Client = create_client(url, key)

class Controller:
    def __init__(self):
        self.supabase = supabase
    
    #Falta agregar la autenticación
    def get_usuario(self, email, contraseña):
        response = self.supabase.table("usuario").select("*").eq("email", email).eq("contraseña", contraseña).execute()
        
        if response.data:
            #Logged in
            return True
        else:
            #Logged failed
            return False
        
    def crear_usuario(self, nombre,email,contraseña, rol = "cliente"):
        self.supabase.table("usuario").insert({"nombre":nombre,"email":email,"contraseña":contraseña, "rol":rol}).execute()
        
    def get_categorias(self):
        response = self.supabase.table("categorias").select("*").execute()
        return response.data 
    
    def get_bazar(self,categorias ): 
        response = self.supabase.rpc("get_bazar_by_categoria", {"cat_name": categorias}).select("id_bazar,nombre_bazar, ubicacion").execute()
        return response.data
    
    def crear_solicitud(self, Lista_fotos, UsuarioID, BazarID, descripcion, categoriaID, Estado='En proceso'):
        response = self.supabase.table("donaciones").insert({
            "usuarioid": UsuarioID,
            "bazarid": BazarID,
            "descripcion": descripcion,
            "categoria": categoriaID,
            "estado": Estado
        }).execute()
        
        folio = response.data[0]["folio"]
        
        for foto in Lista_fotos:
            self.supabase.table("Fotos").insert({
                "folio": folio,
                "url": foto
            }).execute() 
        
        return {"folio": folio, "status": "created"}
    
    def historial_donaciones(self, name):
        response = self.supabase.rpc("get_donacion_usuario", {"usuario_name": name}).execute()
        return response.data
    
    def solicitudes_pendientes(self):
        response = self.supabase.table("donaciones").select("*").eq("estado", "En proceso").execute()
        return response.data
    
    def cambiar_estado_solicitud(self, folio, decision):
        self.supabase.table("donaciones").update({"estado": decision}).eq("folio", folio).execute()
        return {"status": "updated"}

    def solicitudes_aceptadas(self):
        response = self.supabase.table("donaciones").select("*").eq("estado","Aceptado").execute()
        return response.data
    
controller = Controller()

controller.solicitudes_aceptadas()