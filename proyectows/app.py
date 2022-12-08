from flask import Flask, jsonify, request, Response, render_template, redirect
from flask_pymongo import PyMongo
from bson import json_util
import os
from dotenv import load_dotenv
from waitress import serve
import requests
import configparser

load_dotenv() 

app = Flask(__name__)
uri = os.getenv("URI")
net_uri = os.getenv("NET_URI")
app.config["MONGO_URI"]=uri
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
        return response
    else:
        return no_encontrado()


@app.route('/api/estudiantes/registrarcalificacion', methods=['GET', 'POST'])
def registrarcalificacion():
    data = api_to_json()
    temp = "{0:.2f}".format(data["main"]["temp"])
    sensacion = "{0:.2f}".format(data["main"]["feels_like"])
    clima = data["weather"][0]["main"]
    icono = data["weather"][0]["icon"]
    localizacion = data["name"]

    if request.method == 'POST':
        matricula = mongo.db.Pagos.find({'NumeroMatricula' : request.form['numeroMatricula']})
        respuesta = json_util.dumps(matricula)
        
        if respuesta != "[]":
            mongo.db.Estudiante.insert_one(
                {'NumeroMatricula': request.form['numeroMatricula'], 'Materia': request.form['materia'], 'Calificacion': request.form['calificacion']}
            )
        else:
            return no_encontrado()

    return render_template('index.html', localizacion=localizacion, temp=temp, sensacion=sensacion, clima=clima, icono=icono)

@app.route('/public/estados-cuenta', methods=['GET'])
def estadosCuenta():
    try:
        return render_template('estados-cuenta.html', uri=net_uri)
    except Exception as e:
        return str(e)


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

def api_to_json():
    api_url = "http://api.openweathermap.org/data/2.5/weather?q=Culiacan,mx&units=metric&APPID=bde0fccd226156a0f9899a6954345f7a"
    r = requests.get(api_url)
    return r.json()

print(api_to_json())

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=50100, threads=2)