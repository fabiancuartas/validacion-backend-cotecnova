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