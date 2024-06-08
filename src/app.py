""" 
Configuracion de la aplicacion Flask, base de datos y blueprints

Configura Flask, SQLAlchemy, Migrate y CORS.
Registra los modelos de la base de datos.
Registra los blueprints para mesas y productos.

"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = os.getenv('FLASK_ENV')
app.config['PORT'] = int(os.getenv('PORT', 3000))

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)
# Importar los modelos para que Alembic pueda detectarlos
from models import Mesa, Producto, MesaProducto, Cliente, Factura, DetalleFactura, SesionMesa

from blueprints.table import table_bp
from blueprints.product import product_bp
from blueprints.client import client_bp
from blueprints.mesaProductos import mesaProducto_bp
from blueprints.sesions import sesiones_bp
from blueprints.auth import auth_bp
app.register_blueprint(table_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(client_bp, url_prefix='/api')
app.register_blueprint(mesaProducto_bp, url_prefix='/api')
app.register_blueprint(sesiones_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
