from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import datetime
import zeep

app = FastAPI(title="API REST Cotecnova - Inscripciones")

# Configuración secreta para nuestro Token (En la vida real iría en el .env)
SECRET_KEY = "mi_super_secreto_cotecnova"
ALGORITHM = "HS256"

# Esquema de seguridad Bearer para proteger las rutas
security = HTTPBearer()

# --- MODELO DE DATOS JSON (Pydantic) ---
# Esto valida que el cliente envíe exactamente un JSON con esta estructura 
class InscripcionData(BaseModel):
    nombre: str
    email: str
    codigoCurso: str

# --- FUNCIÓN PARA VALIDAR EL TOKEN ---
def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# --- ENDPOINT 1: LOGIN ESTATICO ---
@app.post("/api/login", summary="Generar Token JWT")
def login():
    payload = {
        "sub": "usuario_estudiante",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# --- ENDPOINT 2: INSCRIPCIONES (El puente entre REST y SOAP) ---
# Protegido por Token Bearer 
@app.post("/api/inscripciones", dependencies=[Depends(verificar_token)], summary="Inscripción consumiendo SOAP")
def inscribir_usuario(datos: InscripcionData):
    # La URL donde vive nuestro dinosaurio en Node.js
    wsdl_url = "http://localhost:8000/wsdl?wsdl"
    
    try:
        # 1. Zeep lee el XML (WSDL) y entiende cómo hablar con el SOAP 
        cliente_soap = zeep.Client(wsdl=wsdl_url)
        
        # 2. Convertimos el JSON entrante a los parámetros del SOAP
        respuesta = cliente_soap.service.inscribirUsuario(
            nombre=datos.nombre,
            email=datos.email,
            codigoCurso=datos.codigoCurso
        )
        
        # 3. Respondemos al cliente de la API REST en JSON
        return {
            "mensaje": "Operación REST exitosa",
            "datos_legacy": {
                "resultado": respuesta.resultado,
                "estado": respuesta.estado
            }
        }
        
    except zeep.exceptions.Fault as error_soap:
        # Error 400 si el SOAP nos rechaza (ej. faltan datos) 
        raise HTTPException(status_code=400, detail=f"Error validación SOAP: {str(error_soap)}")
    except Exception as e:
        # Error 500 si el servidor Node está apagado o hay un fallo grave 
        raise HTTPException(status_code=500, detail=f"El servicio Legacy no está disponible: {str(e)}")

# --- RUTA DE PRUEBA ---
@app.get("/")
def read_root():
    return {"mensaje": "API REST Moderna funcionando correctamente"}