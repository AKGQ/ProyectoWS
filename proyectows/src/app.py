from flask import Flask, jsonify, request, Response, render_template, redirect
from flask_pymongo import PyMongo
from bson import json_util
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
<<<<<<< HEAD
uri = os.getenv("URI")
app.config["MONGO_URI"]=uri
=======
app.config["MONGO_URI"]=''
>>>>>>> 7f2c17ecccec69fab9ffe9c9111c56d92162dc47
mongo = PyMongo(app)

@app.route('/api/pagos', methods=['POST']) 
def crear():
    #Recibir datos
    numeroMatricula = request.json['NumeroMatricula']
    tipoPago = request.json['TipoPago']
    institucion = request.json['Institucion']
    descripcion = request.json['Descripcion']
    nombre = request.json['Nombre']
    apellidos = request.json['Apellidos']
    fecha = request.json['Fecha']

    if numeroMatricula and tipoPago and institucion and nombre and apellidos:
        mongo.db.Pagos.insert_one(
            {'NumeroMatricula': numeroMatricula, 'TipoPago': tipoPago, 'Institucion': institucion, 'Descripcion': descripcion, 'Nombre': nombre, 'Apellidos': apellidos, 'Fecha': fecha}
        )
        respuesta = {
            'NumeroMatricula': numeroMatricula,
            'TipoPago': tipoPago,
            'Institucion': institucion,
            'Descripcion': descripcion,
            'Nombre': nombre,
            'Apellidos': apellidos,
            'Fecha': fecha
        }
        return jsonify(respuesta)
    else:
        return error_registro()


@app.route('/api/pagos/<numeroMatricula>', methods=['GET']) 
def mostrar_usuario_matricula(numeroMatricula):
    usuario = mongo.db.Pagos.find({'NumeroMatricula': numeroMatricula})
    response = json_util.dumps(usuario)
    if response != "[]":
        return response(
            response,
            status=200,
            mimetype='application/json'
        )
    else:
        return no_encontrado()


@app.route('/api/estudiantes/registrarcalificacion', methods=['GET', 'POST'])
def registrarcalificacion():
    if request.method == 'POST':
        matricula = mongo.db.Pagos.find({'NumeroMatricula' : request.form['numeroMatricula']})
        respuesta = json_util.dumps(matricula)
        
        if respuesta != "[]":
            mongo.db.Estudiante.insert_one(
                {'NumeroMatricula': request.form['numeroMatricula'], 'Materia': request.form['materia'], 'Calificacion': request.form['calificacion']}
            )
        else:
            return no_encontrado()

    return render_template('./templates/index.html')


#MANEJO DE ERRORES
@app.errorhandler(400) 
def error_registro(error=None):
    mensajeError = jsonify({
        'mensajeError': 'Error al registrar: ' + request.url,
        'status': 400
    })
    mensajeError.status_code = 400
    return mensajeError


@app.errorhandler(404) 
def no_encontrado(error=None):
    mensajeError = jsonify({
        'mensajeError': 'Recurso no encontrado: ' + request.url,
        'status': 404
    })
    mensajeError.status_code = 404
    return mensajeError

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
