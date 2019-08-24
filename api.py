from flask import Flask, jsonify ,request
from flask_cors import CORS
from datetime import datetime
import statistics as stats

app = Flask(__name__)
CORS(app)

tipo_medicion = {'sensor':'TSL2561','variable': 'Luz Solar','unidades':'Lux'}

mediciones = [
 {'fecha': '2019-08-21 18:20:00', **tipo_medicion, 'valor': 300},
 {'fecha': '2019-08-21 23:13:01', **tipo_medicion, 'valor': 3},
 {'fecha': '2019-08-22 15:20:00', **tipo_medicion, 'valor': 500},
 {'fecha': '2019-08-22 18:20:00', **tipo_medicion, 'valor': 600},
 {'fecha': '2019-08-23 11:20:00', **tipo_medicion, 'valor': 1000}
]

@app.route('/')
def get():
    return jsonify(tipo_medicion)

@app.route('/mediciones')
def getAll():
    return jsonify(mediciones)

@app.route('/mediciones/mediana')
def getMediana():
    valores = [medicion['valor'] for medicion in mediciones]
    mediana = stats.median(valores)
    return jsonify(mediana=mediana)

@app.route('/mediciones', methods=['POST'])
def post():
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**body, **tipo_medicion})
    return jsonify(mediciones)

@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putFecha(fecha):
    body = request.json
    find = False
    for medicion in mediciones:
      if fecha == medicion['fecha']:
         find = True  
         medicion['valor'] = body['valor']
         nuevoValor = medicion
    return nuevoValor if find else 'No existe el dato a modificar'

@app.route('/mediciones/<string:fecha>', methods=['DELETE'])
def deleteFecha(fecha):
    find = False
    for medicion in mediciones:
      if fecha == medicion['fecha']:
         find = True
         mediciones.remove(medicion)
    return jsonify(mediciones) if find else 'No existe el dato o ya ha sido borrado'

app.run(port=5000,debug=True)
