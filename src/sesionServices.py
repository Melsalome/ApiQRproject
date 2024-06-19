from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Mesa, Producto, MesaProducto, Cliente, Factura, DetalleFactura, SesionMesa, User
from services import update_client_in_table
from tableServices import update_table_status



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