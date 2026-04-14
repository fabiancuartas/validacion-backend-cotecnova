const express = require('express');
const soap = require('soap');
const fs = require('fs');
const mongoose = require('mongoose');

const app = express();
const port = 8000;

const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017/cotecnova';

mongoose.connect(mongoUri)
    .then(() => console.log('Conectado a MongoDB exitosamente'))
    .catch(err => console.error('Error conectando a MongoDB:', err));

const inscripcionSchema = new mongoose.Schema({
    nombre: String,
    email: String,
    codigoCurso: String,
    fechaInscripcion: { type: Date, default: Date.now }
});

const Inscripcion = mongoose.model('Inscripcion', inscripcionSchema);

const myService = {
    InscripcionService: {
        InscripcionPort: {
            inscribirUsuario: async function(args) {
                console.log('Petición SOAP recibida:', args);
                
                const { nombre, email, codigoCurso } = args;

                if (!nombre || !email || !codigoCurso) {
                    throw {
                        Fault: {
                            faultcode: 'soap:Client',
                            faultstring: 'Faltan datos obligatorios para la inscripción'
                        }
                    };
                }

                try {
                    const nuevaInscripcion = new Inscripcion({ nombre, email, codigoCurso });
                    await nuevaInscripcion.save();
                    
                    console.log('Guardado en MongoDB con éxito:', nuevaInscripcion);

                    return {
                        resultado: `Inscripción exitosa en BD. Bienvenido ${nombre} al curso ${codigoCurso}`,
                        estado: 200
                    };
                } catch (error) {
                    console.error('Error guardando en BD:', error);
                    throw {
                        Fault: {
                            faultcode: 'soap:Server',
                            faultstring: 'Error interno guardando en la base de datos'
                        }
                    };
                }
            }
        }
    }
};

const xml = fs.readFileSync('service.wsdl', 'utf8');

app.listen(port, function() {
    console.log(`Servidor Legacy escuchando en http://localhost:${port}`);
    soap.listen(app, '/wsdl', myService, xml, function(){
        console.log('Servicio SOAP activo. WSDL en: http://localhost:8000/wsdl?wsdl');
    });
});