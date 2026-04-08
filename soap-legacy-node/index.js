const express = require('express');
const soap = require('soap');
const fs = require('fs');

const app = express();
const port = 8000;

// Simulamos una base de datos en memoria usando un array
const baseDeDatos = [];

// Aquí definimos la lógica que conecta con el WSDL
const myService = {
    InscripcionService: {
        InscripcionPort: {
            inscribirUsuario: function(args) {
                console.log('Petición SOAP recibida:', args);
                
                const { nombre, email, codigoCurso } = args;

                // Validación simple
                if (!nombre || !email || !codigoCurso) {
                    throw {
                        Fault: {
                            faultcode: 'soap:Client',
                            faultstring: 'Faltan datos obligatorios para la inscripción'
                        }
                    };
                }

                // Guardamos en nuestra "base de datos" simulada
                baseDeDatos.push({ nombre, email, codigoCurso });
                console.log(' Base de datos actual:', baseDeDatos);

                // Retornamos la respuesta (debe coincidir con inscribirUsuarioResponse en el WSDL)
                return {
                    resultado: `Inscripción exitosa. Bienvenido ${nombre} al curso ${codigoCurso}`,
                    estado: 200
                };
            }
        }
    }
};

// Leemos el archivo WSDL que creamos
const xml = fs.readFileSync('service.wsdl', 'utf8');

// Arrancamos el servidor Express
app.listen(port, function() {
    console.log(` Servidor Legacy escuchando en http://localhost:${port}`);
    
    // Conectamos la librería SOAP con nuestro servidor y nuestro WSDL
    soap.listen(app, '/wsdl', myService, xml, function(){
        console.log(' Servicio SOAP activo. El WSDL es accesible en: http://localhost:8000/wsdl?wsdl');
    });
});