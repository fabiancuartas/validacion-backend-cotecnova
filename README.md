# Validación Backend Cotecnova - Microservicios

Este proyecto es la prueba práctica para la asignatura de Ingeniería Web y de Servicios. Consiste en una arquitectura de microservicios donde una API REST moderna consume un servicio SOAP legacy.

## Arquitectura Implementada
* **Servicio Legacy (SOAP):** Desarrollado en Node.js, expone un WSDL para la validación e inscripción de usuarios.
* **Microservicio (REST):** Desarrollado en Python con FastAPI. Genera tokens JWT (Bearer) y actúa como cliente SOAP utilizando la librería Zeep para procesar las inscripciones y manejar los errores HTTP correspondientes.

## Requisitos Previos
* Docker y Docker Compose instalados en el sistema.

## Instrucciones de Ejecución
1. Clonar este repositorio.
2. Abrir una terminal en la raíz del proyecto.
3. Ejecutar el siguiente comando para construir y levantar los contenedores:
   ```bash
   docker-compose up --build
    ```
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
### 2. Prueba de Error de Negocio (Código 400 - Validación SOAP)
Para simular un rechazo desde el servidor Legacy, envíe el JSON con el campo nombre vacío:
```json
{
  "nombre": "",
  "email": "fabian@ejemplo.com",
  "codigoCurso": "ING-WEB-101"
}
```
### 3. Prueba de Caída del Sistema Legacy (Código 500)
1. Abra una nueva terminal.
2. Detenga el contenedor del servicio SOAP ejecutando: docker stop cotecnova-soap
3. Vuelva a Swagger e intente enviar una petición de inscripción válida.
* Resultado esperado: La API de Python fallará al intentar comunicarse con el WSDL y devolverá un 500 Internal Server Error indicando que el servicio Legacy no está disponible.
* (Nota: Para restaurar el servicio, ejecute docker start cotecnova-soap).