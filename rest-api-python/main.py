from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import datetime

app = FastAPI(title="API REST Cotecnova - Inscripciones")

# Configuración secreta para nuestro Token (En la vida real iría en el .env)
SECRET_KEY = "mi_super_secreto_cotecnova"
ALGORITHM = "HS256"

# Esquema de seguridad Bearer para proteger las rutas
security = HTTPBearer()

# --- ENDPOINT 1: LOGIN ESTATICO ---
@app.post("/api/login", summary="Generar Token JWT")
def login():
    # Como el PDF permite un login estático para simplificar, 
    # generamos un token válido por 1 hora sin pedir usuario/contraseña.
    payload = {
        "sub": "usuario_estudiante",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}

# --- RUTA DE PRUEBA (Para verificar que la API funciona) ---
@app.get("/")
def read_root():
    return {"mensaje": "API REST Moderna funcionando correctamente"}