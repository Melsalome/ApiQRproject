from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Mesa, Producto, MesaProducto, Cliente, Factura, DetalleFactura, SesionMesa, User



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