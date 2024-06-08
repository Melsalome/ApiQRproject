"""
    Blueprints que definen las rutas de API para las mesas
    
    Definen las rutas de API para gestionar mesas y productos.
    Utilizan las funciones de servicios para interactuar con la base de datos y procesar la lógica de negocio.
"""
from flask import Blueprint, request, jsonify
from services import get_active_sesion, add_product_to_sesion, get_products_by_sesion, close_sesion, get_all_active_sesion, update_product_status

sesiones_bp = Blueprint('sesiones', __name__)


@sesiones_bp.route('/sesiones/<int:table_id>/products', methods=['POST'])
def add_product_to_table_route(table_id):
    body = request.json
    product_id = body.get('producto_id')
    quantity = body.get('cantidad', 1)
    if not product_id:
        return jsonify({"message": "producto_id is required"}), 400

    sesion = get_active_sesion(table_id)
    if not sesion:
        return jsonify({"message": "No active session found for this table"}), 404

    mesa_producto = add_product_to_sesion(sesion['id_sesion'], product_id, quantity)
    return jsonify(mesa_producto), 201


@sesiones_bp.route('/sesiones/<int:table_id>/active', methods=['GET'])
def get_sesion_active_route(table_id):
    sesion = get_active_sesion(table_id)
    if not sesion:
        return jsonify({"message": "No active session found for this table"}), 404
    
    return jsonify(sesion), 200

@sesiones_bp.route('/sesiones/<int:table_id>/products', methods=['GET'])
def get_products_by_sesion_route(table_id):
    sesion = get_active_sesion(table_id)
    if not sesion:
        return jsonify({"message": "No active session found for this table"}), 404
    
    productos = get_products_by_sesion(sesion['id_sesion'])
    return jsonify(productos), 200

@sesiones_bp.route('/sesiones/<int:table_id>/close', methods=['POST'])
def close_sesion_route(table_id):
    sesion = get_active_sesion(table_id)
    if not sesion:
        return jsonify({"message": "No active session found for this table"}), 404
    
    closed_sesion = close_sesion(sesion['id_sesion'])
    return jsonify(closed_sesion), 200

@sesiones_bp.route('/sesiones', methods=['GET'])
def get_all_sesions_route():
    sesiones = get_all_active_sesion()
    return jsonify(sesiones), 200

@sesiones_bp.route('/sesiones/<int:sesion_id>/productos/estado', methods=['PATCH'])
def update_product_status_route(sesion_id):
    body = request.json
    new_status = body.get('estado')
    product_id = body.get('id_producto')  # Opcional: ID del producto específico

    if not new_status:
        return jsonify({"message": "estado is required"}), 400

    updated_products = update_product_status(sesion_id, new_status, product_id)
    if not updated_products:
        return jsonify({"message": "No products found for the given session"}), 404

    return jsonify(updated_products), 200