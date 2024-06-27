import io
import os
from flask import Blueprint, request, jsonify, send_file
import qrcode
generateqr_bp = Blueprint('generateqr', __name__)

# @generateqr_bp.route('/app/restaurants/<int:restaurant_id>/tables/<int:table_id>/generate_qr', methods=['GET'])
# def generate_qr(restaurant_id, table_id):
#   # cambiar url
#     frontend_url = os.getenv('FRONTEND_URL')
#     url = f"{frontend_url}/app/restaurants/{restaurant_id}/tables/{table_id}/menu"
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(url)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', back_color='white')
#     buffer = io.BytesIO()
#     img.save(buffer, 'PNG')
#     buffer.seek(0)
#     return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f"qr_restaurant_{restaurant_id}_table_{table_id}.png")

# def generate_qr_code(restaurant_id, table_id):
#     backend_url = os.getenv('BACKEND_URL')
#     url = f"${backend_url}/app/restaurants/{restaurant_id}/tables/{table_id}/menu"
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(url)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', back_color='white')
#     img.save(f"qr_restaurant_{restaurant_id}_table_{table_id}.png")
#     print(f"QR code generated for Restaurant ID: {restaurant_id}, Table ID: {table_id}")

def generate_qr_image(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

@generateqr_bp.route('/restaurants/<int:restaurant_id>/tables/<int:table_number>/generate_qr', methods=['GET'])
def generate_qr(restaurant_id, table_number):
    frontend_url = os.getenv('FRONTEND_URL')
    if not frontend_url:
        return jsonify({"error": "FRONTEND_URL is not set in the environment variables"}), 500

    url = f"{frontend_url}/app/restaurants/{restaurant_id}/tables/{table_number}/menu"
    try:
        img = generate_qr_image(url)
        buffer = io.BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f"qr_restaurant_{restaurant_id}_table_{table_number}.png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_qr_code(restaurant_id, table_number):
    backend_url = os.getenv('BACKEND_URL')
    if not backend_url:
        print("BACKEND_URL is not set in the environment variables")
        return

    url = f"{backend_url}/app/restaurants/{restaurant_id}/tables/{table_number}/menu"
    try:
        img = generate_qr_image(url)
        img.save(f"qr_restaurant_{restaurant_id}_table_{table_number}.png")
        print(f"QR code generated for Restaurant ID: {restaurant_id}, Table ID: {table_number}")
    except Exception as e:
        print(f"Error generating QR code: {e}")