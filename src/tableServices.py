
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Mesa, Producto, MesaProducto, Cliente, Factura, DetalleFactura, SesionMesa, User



def create_table(numero_mesa):
    existing_table = Mesa.query.filter_by(numero_mesa=numero_mesa).first()
    if existing_table:
        return None, "Mesa ya existe"
    
    nueva_mesa = Mesa(numero_mesa=numero_mesa)
    db.session.add(nueva_mesa)
    db.session.commit()
    return nueva_mesa.to_dict()

def get_all_tables():
    return [mesa.to_dict() for mesa in Mesa.query.all()]

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