# Validación Backend Cotecnova - Microservicios

Este repositorio contiene la prueba práctica para la asignatura de Ingeniería Web y de Servicios. El proyecto implementa una arquitectura basada en microservicios comunicados entre sí, utilizando contenedores Docker para un despliegue ágil, seguro y agnóstico a la plataforma.

## Arquitectura Implementada
* **Servicio Legacy (SOAP):** Desarrollado en Node.js, expone un WSDL para la validación e inscripción de usuarios.
* **Microservicio (REST):** Desarrollado en Python con FastAPI. Genera tokens JWT (Bearer) y actúa como cliente SOAP utilizando la librería Zeep para procesar las inscripciones y manejar los errores HTTP correspondientes.
* **Persistencia de Datos (NoSQL):** Implementada con MongoDB y Mongoose. Está conectada directamente al servicio Legacy para almacenar de manera "fehaciente" las inscripciones procesadas y aprobadas.

## Requisitos Previos
* **Docker** y **Docker Compose** instalados en el sistema anfitrión. (No se requiere instalar bases de datos, Node.js ni Python localmente, todo está dockerizado).

## Instrucciones de Ejecución
1. Clonar este repositorio.
2. Abrir una terminal en la raíz del proyecto.
3. Ejecutar el siguiente comando para construir y levantar los contenedores (esto descargará automáticamente MongoDB y levantará los servidores):
   ```bash
   docker-compose up --build
    ```
4. El sistema estará listo cuando la consola indique "Conectado a MongoDB exitosamente" y los servicios estén disponibles en:
- API REST (Swagger UI): http://localhost:8001/docs
- WSDL del Servicio SOAP: http://localhost:8000/wsdl?wsdl

## Guía de Pruebas y Verificación

Para probar los diferentes escenarios de la arquitectura, primero debe generar un token de acceso:
1. Ingrese a la documentación interactiva (Swagger): `http://localhost:8001/docs`
2. Ejecute el endpoint `POST /api/login`.
3. Copie el `access_token` generado, haga clic en el botón **"Authorize"** en la parte superior, pegue el token y haga clic en *Authorize*.

A continuación, puede probar los 3 escenarios requeridos desde la interfaz de Swagger en el endpoint `POST /api/inscripciones`:

### 1. Prueba de Éxito (Conexión REST a SOAP)
Envíe el siguiente JSON (con todos los datos correctos):
```json
{
  "nombre": "Fabian Cuartas",
  "email": "fabian@ejemplo.com",
  "codigoCurso": "ING-WEB-101"
}
```
- Resultado esperado: Código HTTP 200 OK con un mensaje JSON confirmando la operación. El sistema SOAP validará la petición y la guardará físicamente en MongoDB.

### 2. Prueba de Error de Negocio (Código 400 - Validación SOAP)
Para simular un rechazo desde el servidor Legacy, envíe el JSON con el campo nombre vacío:
```json
{
  "nombre": "",
  "email": "fabian@ejemplo.com",
  "codigoCurso": "ING-WEB-101"
}
```
- Resultado esperado: Python atrapará la excepción (Faultcode) proveniente del WSDL y devolverá un 400 Bad Request indicando que faltan datos obligatorios. No se guardará ningún registro en la base de datos.

### 3. Prueba de Caída del Sistema Legacy (Código 500)
1. Abra una nueva terminal.
2. Detenga el contenedor del servicio SOAP ejecutando: `docker stop cotecnova-soap`
3. Vuelva a Swagger e intente enviar una petición de inscripción válida.
* Resultado esperado: La API de Python fallará al intentar comunicarse con el WSDL y devolverá un `500 Internal Server Error` indicando que el servicio Legacy no está disponible.
* _(Nota: Para restaurar el servicio, ejecute `docker start cotecnova-soap`)._

### 4. Verificación de Auditoría en Base de Datos
Para comprobar que los datos del caso de éxito se guardaron de forma "fehaciente" en la base de datos NoSQL, ingrese al contenedor de MongoDB ejecutando en su terminal:
```bash
docker exec -it cotecnova-mongo mongosh
```
Una vez dentro de la consola interactiva de Mongo, consulte los registros con:
```bash
use cotecnova
db.inscripcions.find()
```