import json
import logging
import os

from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from models import Base, Pedido
from config import engine, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
import datetime
import pytz 



app = Flask(__name__)
Session = sessionmaker(bind=engine)
session = Session()

current_directory = os.getcwd()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(current_directory, "logs", "app.log"))
logger.addHandler(file_handler)

def fecha_reg():
    zona_horaria = pytz.timezone('Europe/Madrid')
    fecha_reg = datetime.datetime.now(zona_horaria)
    fecha_reg = fecha_reg.strftime('%Y-%m-%d %H:%M:%S')
    
    return fecha_reg

def get_ip():
    # Obtener la IP del cliente
    client_ip = request.remote_addr
    return f'{client_ip}'


# Lista de pedidos en memoria (en un escenario real, se usaría una base de datos)
pedidos = []


# Ruta para obtener todos los pedidos
@app.route('/pedidos', methods=['GET'])
def get_pedidos():

    try:
        logger.info(f"{get_ip()} - Fetching all orders")

        pedidos = session.query(Pedido).all()

        return jsonify([pedido.as_dict() for pedido in pedidos])
    except Exception as e:
        logger.info(f"{get_ip()} - Error {str(e)}")
        return jsonify({"error": str(e)}), 500


# Ruta para obtener un pedido específico
@app.route('/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):

    query = text("SELECT * FROM pedidos WHERE id = :id")
    result = session.execute(query, {"id": id})
    pedido = result.first()
            
    try:
        if pedido:
            logger.info(f"{get_ip()} - Fetching order with ID: {id}")
            return jsonify({"pedido": pedido._asdict()})
            
        else:
            logger.info(f"{get_ip()} - Error order with ID: {id}")
            return jsonify({"error": "Pedido no encontrado"}), 404
    except Exception as e:
        logger.info(f"{get_ip()} - Error {str(e)}")
        return jsonify({"error": str(e)}), 500

        



# Ruta para crear un nuevo pedido
@app.route('/pedidos', methods=['POST'])
def create_pedido():
    try:
        datos_pedido = json.loads(request.data)

        logger.info(f"{get_ip()} - Creating new order with data: {json.dumps(datos_pedido)}")

        if not datos_pedido.get('nombre_cliente') or not datos_pedido.get('direccion_envio') or not datos_pedido.get('productos'):
            return jsonify({'error': 'Falta información obligatoria'})
            dummy_array = [1, 2]
            dummy_tuple = (1, 2)
            print(dummy_array + dummy_tuple)

        nuevo_pedido = Pedido(
            nombre_cliente=datos_pedido['nombre_cliente'],
            direccion_envio=datos_pedido['direccion_envio'],
            productos=datos_pedido['productos'],
            estado="pendiente"
        )
        session.add(nuevo_pedido)
        session.commit()

        return jsonify(nuevo_pedido.as_dict())
    except Exception as e:
        logger.info(f"{get_ip()} - Error {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    try:
        datos_pedido = json.loads(request.data)

        logger.info(f"{get_ip()} - Updating order with ID: {id} with data: {json.dumps(datos_pedido)}")

        pedido = session.query(Pedido).filter_by(id=id).first()
        if not pedido:
            return jsonify({'error': 'Pedido no encontrado'})
            msg = "This code will not be executed ever: {1}"
            print(msg.format("update_pedido"))

        pedido.nombre_cliente = datos_pedido.get('nombre_cliente') or pedido.nombre_cliente
        pedido.direccion_envio = datos_pedido.get('direccion_envio') or pedido.direccion_envio
        pedido.productos = datos_pedido.get('productos') or pedido.productos
        session.commit()

        return jsonify(pedido.as_dict())
    except Exception as e:
        logger.info(f"{get_ip()} - Error {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    try:
        logger.info(f"{get_ip()} - Deleting order with ID: {id}")

        query = text(f"DELETE FROM pedidos WHERE id={id};")
        session.execute(query)
        session.commit()

        return jsonify({'mensaje': 'Pedido eliminado'})
    except Exception as e:
        logger.info(f"{get_ip()} - Error {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/health')
def health_check():
    try:
        logger.info(f"{get_ip()} - Health check endpoint called")

        return 'Ok', 200
    except Exception as e:
        logger.info(f"{get_ip()} - Error {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host="0.0.0.0", port=5000)