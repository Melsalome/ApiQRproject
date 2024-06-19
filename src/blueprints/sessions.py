"""
    Blueprints que definen las rutas de API para las mesas
    
    Definen las rutas de API para gestionar mesas y productos.
    Utilizan las funciones de servicios para interactuar con la base de datos y procesar la lógica de negocio.
"""
from flask import Blueprint, request, jsonify
from services.sessionServices import get_active_session, add_product_to_sesion, get_product_list_by_session, close_session, get_active_session_list, update_product_status

sessions_bp = Blueprint('sessions', __name__)


@sessions_bp.route('/sessions/<int:table_id>/products', methods=['POST'])
def add_product_to_table_route(table_id):
    body = request.json
    product_id = body.get('product_id')
    quantity = body.get('cantidad', 1)
    if not product_id:
        return jsonify({"message": "product_id is required"}), 400

    session = get_active_session(table_id)
    if not session:
        return jsonify({"message": "No active session found for this table"}), 404

    table_product = add_product_to_sesion(session['id_session'], product_id, quantity)
    return jsonify(table_product), 201


@sessions_bp.route('/sessions/<int:table_id>/active', methods=['GET'])
def get_sesion_active_route(table_id):
    session = get_active_session(table_id)
    if not session:
        return jsonify({"message": "No active session found for this table"}), 404
    
    return jsonify(session), 200

@sessions_bp.route('/sessions/<int:table_id>/products', methods=['GET'])
def get_products_by_session_route(table_id):
    session = get_active_session(table_id)
    if not session:
        return jsonify({"message": "No active session found for this table"}), 404
    
    products = get_product_list_by_session(session['id_session'])
    return jsonify(products), 200

@sessions_bp.route('/sessions/<int:table_id>/close', methods=['POST'])
def close_session_route(table_id):
    session = get_active_session(table_id)
    if not session:
        return jsonify({"message": "No active session found for this table"}), 404
    
    closed_session = close_session(session['id_sesion'])
    return jsonify(closed_session), 200

@sessions_bp.route('/sessions', methods=['GET'])
def get_all_sesions_route():
    sessions = get_active_session_list()
    return jsonify(sessions), 200

@sessions_bp.route('/sessions/<int:session_id>/products/estado', methods=['PATCH'])
def update_product_status_route(session_id):
    body = request.json
    new_status = body.get('status')
    product_id = body.get('id_product')  # Opcional: ID del producto específico

    if not new_status:
        return jsonify({"message": "status is required"}), 400

    updated_products = update_product_status(session_id, new_status, product_id)
    if not updated_products:
        return jsonify({"message": "No products found for the given session"}), 404

    return jsonify(updated_products), 200