"""
Punto de entrada de la aplicación
"""
import os
from flask import Flask, request, jsonify, url_for
# from flask_cors import CORS
from utils import APIException, generate_sitemap
from app import app
from admin import setup_admin
from commands import setup_commands

setup_admin(app)
setup_commands(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
def generate_qr_code(restaurant_id, table_id):
    url = f"${process.env.BACKEND_URL}/app/restaurants/{restaurant_id}/tables/{table_id}/menu"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(f"qr_restaurant_{restaurant_id}_table_{table_id}.png")
    print(f"QR code generated for Restaurant ID: {restaurant_id}, Table ID: {table_id}")

@app.route('/api/restaurants/<int:restaurant_id>/tables/<int:table_id>/generate_qr', methods=['GET'])
def generate_qr(restaurant_id, table_id):
  # cambiar url   
    url = f"https://humble-pancake-977xqppgr6q427j55-3000.app.github.dev/app/restaurants/{restaurant_id}/tables/{table_id}/menu"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f"qr_restaurant_{restaurant_id}_table_{table_id}.png")
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':

    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)