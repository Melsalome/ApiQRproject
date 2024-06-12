"""
    Logica de negocio y servicios
    
    Funciones para crear, obtener y gestionar mesas, productos y facturas.
    Incluye funciones para crear productos, obtener todos los productos, y generar facturas.
"""

import os
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Mesa, Producto, MesaProducto, Cliente, Factura, DetalleFactura, SesionMesa, User
from Crypto.Cipher import AES
import base64
import json
from Crypto.Util.Padding import unpad

secreteKey = os.environ.get("SECRET_KEY")
##Servicios de mesa
def create_table(numero_mesa):
    existing_table = Mesa.query.filter_by(numero_mesa=numero_mesa).first()
    if existing_table:
        return None, "Mesa ya existe"
    
    nueva_mesa = Mesa(numero_mesa=numero_mesa)
    db.session.add(nueva_mesa)
    db.session.commit()
    return nueva_mesa.to_dict()
# Obtener todas las mesas
def get_all_tables():
    return [mesa.to_dict() for mesa in Mesa.query.all()]
# Agregar producto a mesa
# def add_product_to_table(table_id, product_id, quantity):
#     mesa_producto = MesaProducto(id_mesa=table_id, id_producto=product_id, cantidad=quantity)
#     db.session.add(mesa_producto)
#     db.session.commit()
#     return mesa_producto
# Asignar cliente a mesa
def assign_client_to_table(table_id, client_id):
    table = Mesa.query.get(table_id)
    if not table:
        return None
    cliente = Cliente.query.get(client_id)
    table.id_cliente = cliente.id
    db.session.commit()
    return cliente.to_dict()
# Actualizar estado de la mesa
def update_table_status(table_id, status):
    table = Mesa.query.get(table_id)
    if table:
        table.estado = status
        db.session.commit()
    return table.to_dict()
# Actualizar cliente de la mesa
def update_client_in_table(table_id, client_id):
    table = Mesa.query.get(table_id)
    if table:
        table.id_cliente = client_id
        db.session.commit()
    return table.to_dict() 
# Vaciar mesa
def clear_table(table_id):
    table = Mesa.query.get(table_id)
    if not table:
        return False
    MesaProducto.query.filter_by(id_sesion=table_id).delete()
    table.id_cliente = None
    db.session.commit()
    return True

##Sesiones 
def create_sesion(mesa_id, cliente_id):
    nueva_sesion = SesionMesa(id_mesa=mesa_id, id_cliente=cliente_id, estado='activa')
    db.session.add(nueva_sesion)
    db.session.commit()
    update_table_status(mesa_id, 'ocupada')
    update_client_in_table(mesa_id, cliente_id)
    return nueva_sesion.to_dict()

def get_active_sesion(mesa_id):
    sesion = SesionMesa.query.filter_by(id_mesa=mesa_id, estado='activa').first()
    return sesion.to_dict() if sesion else None

def get_all_active_sesion():
   return [sesion.to_dict() for sesion in SesionMesa.query.filter_by(estado='activa').all()]

def close_sesion(sesion_id):
    sesion = SesionMesa.query.get(sesion_id)
    if sesion:
        sesion.estado = 'cerrada'
        db.session.commit()
        update_table_status(sesion.id_mesa, 'disponible')
        update_client_in_table(sesion.id_mesa, None)
    return sesion.to_dict() if sesion else None

def add_product_to_sesion(sesion_id, product_id, quantity):
    mesa_producto = MesaProducto(id_sesion=sesion_id, id_producto=product_id, cantidad=quantity)
    db.session.add(mesa_producto)
    db.session.commit()
    return mesa_producto.to_dict()

def get_products_by_sesion(sesion_id):
    return [mesa_producto.to_dict() for mesa_producto in MesaProducto.query.filter_by(id_sesion=sesion_id).all()]

def update_product_status(sesion_id,new_estado, product_id=None):
    if product_id:
        mesa_producto = MesaProducto.query.filter_by(id_sesion=sesion_id, id_producto=product_id).first()
        if not mesa_producto:
            return None
        mesa_producto.estado = new_estado
        db.session.commit()
        return [mesa_producto.to_dict()]

    mesa_productos = MesaProducto.query.filter_by(id_sesion=sesion_id).all()
    if not mesa_productos:
        return None
    for mesa_producto in mesa_productos:
        mesa_producto.estado = new_estado
    db.session.commit()
    return [mesa_producto.to_dict() for mesa_producto in mesa_productos]

##Servicios de producto
# Crear un nuevo producto
def create_product(nombre, precio, descripcion):
    nuevo_producto = Producto(nombre=nombre, precio=precio, descripcion =descripcion)
    db.session.add(nuevo_producto)
    db.session.commit()
    return nuevo_producto.to_dict()
# Obtener todos los proyectos
def get_all_products():
  return [producto.to_dict() for producto in Producto.query.all()]
# Actualizar un producto
def update_product(product_id, nombre, precio, descripcion):
    producto = Producto.query.get(product_id)
    if not producto:
        return None
    producto.nombre = nombre
    producto.precio = precio
    producto.descripcion = descripcion
    db.session.commit()
    return producto.to_dict()

# Eliminar un producto
def delete_product(product_id):
    producto = Producto.query.get(product_id)
    if not producto:
        return None
    db.session.delete(producto)
    db.session.commit()
    return producto.to_dict()


# Servicios de cliente
# Crear un nuevo cliente
def create_client(nombre):
    nuevo_cliente = Cliente(nombre=nombre)
    db.session.add(nuevo_cliente)
    db.session.commit()
    return nuevo_cliente.to_dict()
# Obtener todos los clientes
def get_all_clients():
    return [cliente.to_dict() for cliente in Cliente.query.all()]

# Servicios de facturas
# Generar una nueva factura
def generate_invoice(table_id, metodo_pago):
    pedidos = MesaProducto.query.filter_by(id_mesa=table_id, estado='aprobado').all()
    if not pedidos:
        return None
    
    total = sum(pedido.producto.precio * pedido.cantidad for pedido in pedidos)
    factura = Factura(id_mesa=table_id, total=total, metodo_pago=metodo_pago)
    db.session.add(factura)
    db.session.commit()

    for pedido in pedidos:
        detalle = DetalleFactura(
            id_factura=factura.id,
            id_producto=pedido.id_producto,
            cantidad=pedido.cantidad,
            precio_unitario=pedido.producto.precio,
            subtotal=pedido.producto.precio * pedido.cantidad
        )
        db.session.add(detalle)
    
    db.session.commit()
    return factura.to_dict()

# servicios Mesa-Productos
def get_all_mesaProductos():
    all_mesasProducto = MesaProducto.query.all()
    sesiones_dict = {}

    for mesaProducto in all_mesasProducto:
        if mesaProducto.id_sesion not in sesiones_dict:
            sesiones_dict[mesaProducto.id_sesion] = {
                'id_sesion': mesaProducto.id_sesion,
                'productos': []
            }
        
        sesiones_dict[mesaProducto.id_sesion]['productos'].append(mesaProducto.to_dict())

    sesiones_list = list(sesiones_dict.values())
    return sesiones_list
    
    
# Función para obtener los productos de una mesa por ID de mesa
def get_mesaProducto_byId(id_session):
    mesa_productos = MesaProducto.query.filter_by(id_sesion=id_session).all()
    if not mesa_productos:
        return None
    return [mesa_producto.to_dict() for mesa_producto in mesa_productos]



## USUARIOS 
def create_user(restaurant_name, first_name,last_name, email, password,role='user'):
    if User.query.filter_by(email=email).first():
        return None, "User already exists"
    new_user = User(restaurant_name = restaurant_name, first_name=first_name, last_name=last_name,email=email,role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict(), None

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user.to_dict(), None
    return None, "Invalid email or password"

#Esta funcion 
def role_required(role):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if role not in claims['roles']:
                return jsonify({"message": "Permission denied"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def get_all_users():
    return [user.to_dict() for user in User.query.all()]

# desencriptar data
