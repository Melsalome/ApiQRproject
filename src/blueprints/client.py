"""
    Blueprints que definen las rutas de API para los productos
    Definen las rutas de API para gestionar mesas y productos.
    Utilizan las funciones de servicios para interactuar con la base de datos y procesar la lógica de negocio.
"""
from flask import Blueprint, request, jsonify
from services import create_client, get_all_clients, update_product, delete_product
from flask_jwt_extended import jwt_required, get_jwt_identity

client_bp = Blueprint('client', __name__)

# Crear un nuevo cliente
@client_bp.route('/client/create', methods=['POST'])
def add_client():
    body = request.json    
    client_name = body.get('nombre')
    if not client_name:
        new_client = create_client(None)
        return jsonify(new_client), 201
    new_client = create_client(client_name)
    return jsonify(new_client), 201

# Obtener todos los clientes
@client_bp.route('/clients', methods=['GET'])
def get_clients():
    clients = get_all_clients()
    return jsonify(clients), 200

# Estas rutas hay que cambiarlas para clientes
@client_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product_route(product_id):
    body = request.json
    product_name = body.get('nombre')
    product_price = body.get('precio')
    product_description = body.get('descripcion')
    if not product_name or not product_price:
        return jsonify({"message": "Missing product name or price"}), 400

    updated_product = update_product(product_id, product_name, product_price, product_description)
    if not updated_product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({"nombre producto": updated_product.nombre, "id": updated_product.id, "precio": updated_product.precio, "descripcion": updated_product.descripcion}), 200

@client_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    deleted_product = delete_product(product_id)
    if not deleted_product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({"message": "Product deleted", "nombre producto": deleted_product.nombre, "id": deleted_product.id}), 200




