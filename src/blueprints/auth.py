from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services import create_user, authenticate_user,get_all_users
from Crypto.Cipher import AES
import base64
import json

auth_bp = Blueprint('auth', __name__)
# def decrypt_data(encrypted_data):
#     try:
#         # Base64 decode
#         encrypted_data = base64.b64decode(encrypted_data)
        
#         # Create AES cipher
#         iv = encrypted_data[:16]
#         ciphertext = encrypted_data[16:]
        
#         # Create AES cipher
#         cipher = AES.new('odin2413!odin241'.encode('utf-8'), AES.MODE_CFB, iv)
        
#         # Decrypt and decode
        
#         decrypted_data = cipher.decrypt(ciphertext).decode('utf-8')
        
#         # Decrypt and decode
        
#         return json.loads(decrypted_data)
#     except Exception as e:
#         print(f"Error al desencriptar: {e}")
#         return None

@auth_bp.route('/register', methods=['POST'])
# def register():
#     try:
#         encrypted_data = request.json.get('data')
#         decrypted_data = decrypt_data(encrypted_data)
#         print(decrypted_data)
#         if decrypted_data is None:
#             return jsonify({"error": "Failed to decrypt data"}), 500

#         restaurant_name = decrypted_data.get("restaurant name")
#         first_name = decrypted_data.get("first name")
#         last_name = decrypted_data.get("last name")
#         email = decrypted_data.get("email")
#         password = decrypted_data.get("password")

#         # Aquí puedes agregar la lógica para guardar los datos en la base de datos

#         return jsonify({"status": "ok"}), 200
#     except Exception as e:
#         print(f"Error en el registro: {e}")
#         return jsonify({"error": "Internal server error"}), 500
def register():
    body = request.json
    first_name = body.get('first name')
    last_name = body.get("last name")
    restaurant_name = body.get("restaurant name")
    email = body.get('email')
    password = body.get('password')
    role = body.get('role')
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400
    if not role:
        new_user = create_user(restaurant_name,first_name, last_name,email, password)
        return jsonify(new_user), 201
    new_user, error = create_user(restaurant_name,first_name, last_name, email, password, role)
        
    if error:
        return jsonify({"message": error}), 400
    

    return jsonify(new_user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    body = request.json
    email = body.get('email')
    password = body.get('password')
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    user, error = authenticate_user(email, password)
    if error:
        return jsonify({"message": error}), 401

    # Información adicional a pasar en el token
    additional_claims = {
        'email': user['email'],
        'roles': user.get('role', [])
    }
    access_token = create_access_token(identity=user['id'], additional_claims=additional_claims)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/all', methods=['GET'])
def get_all():
    return jsonify(get_all_users()), 200