"""
    Blueprints que definen las rutas de API para las mesas
    
    Definen las rutas de API para gestionar mesas y productos.
    Utilizan las funciones de servicios para interactuar con la base de datos y procesar la lógica de negocio.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from services import create_table, get_all_tables, create_sesion, assign_client_to_table, clear_table, generate_invoice, role_required

table_bp = Blueprint('tables', __name__)



# Crear una nueva mesa
@table_bp.route('/tables', methods=['POST'])
def add_table():
    body = request.json
    numero_mesa = body.get('numero_mesa')
    if not numero_mesa:
        return jsonify({"message": "numero_mesa is required"}), 400

    new_table = create_table(numero_mesa)
    return jsonify(new_table), 201

# Obtener todas las mesas
@table_bp.route('/tables', methods=['GET'])
# @role_required('admin') 
def get_tables():
    tables = get_all_tables()
    return jsonify(tables), 200
# Asignar un cliente a una mesa
@table_bp.route('/tables/<int:table_id>/<int:client_id>/client', methods=['POST'])
def assign_client_to_table_route(table_id,client_id):
    if not client_id:
        return jsonify({"message": "Client ID is required"}), 400
    
    sesion = create_sesion(table_id, client_id)
    if not sesion:
        return jsonify({"message": "Error creating session"}), 500

    return jsonify(sesion), 200
# Limpiar una mesa
@table_bp.route('/tables/<int:table_id>', methods=['DELETE'])
def clear_table_route(table_id):
    success = clear_table(table_id)
    if not success:
        return jsonify({"message": "Table not found"}), 404

    return jsonify({"message": "Table cleared"}), 200

# Generar una factura
@table_bp.route('/tables/<int:table_id>/invoice', methods=['POST'])
def generate_invoice_route(table_id):
    body = request.json
    metodo_pago = body.get('metodo_pago')
    if not metodo_pago:
        return jsonify({"message": "metodo_pago is required"}), 400

    factura = generate_invoice(table_id, metodo_pago)
    if not factura:
        return jsonify({"message": "No approved orders for this table"}), 404

    return jsonify(factura), 201