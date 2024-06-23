from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import ProductTable, TableSession
from services.tableServices import update_table_status, update_client_in_table



def create_session(table_id, client_id):
    new_session = TableSession(id_table=table_id, id_client=client_id, status='active')
    db.session.add(new_session)
    db.session.commit()
    update_table_status(table_id, 'occupied')
    update_client_in_table(table_id, client_id)
    return new_session.to_dict()



def get_active_session(table_id):
    sesion = TableSession.query.filter_by(id_table=table_id, status='active').first()
    return sesion.to_dict() if sesion else None



def get_active_session_list():
   return [sesion.to_dict() for sesion in TableSession.query.filter_by(status='active').all()]



def close_session(sesion_id):
    sesion = TableSession.query.get(sesion_id)
    if sesion:
        sesion.status = 'closed'
        db.session.commit()
        update_table_status(sesion.id_table, 'available')
        update_client_in_table(sesion.id_table, None)
    return sesion.to_dict() if sesion else None



def add_product_to_session(session_id, product_id, quantity):
    product_table = ProductTable(id_session=session_id, id_product=product_id, quantity=quantity)
    db.session.add(product_table)
    db.session.commit()
    return product_table.to_dict()



def get_product_list_by_session(session_id):
    return [product_table.to_dict() for product_table in ProductTable.query.filter_by(id_session=session_id).all()]



def update_product_status(session_id,new_status, product_id=None):
    if product_id:
        product_table = ProductTable.query.filter_by(id_session=session_id, id_producto=product_id).first()
        if not product_table:
            return None
        product_table.status = new_status
        db.session.commit()
        return [product_table.to_dict()]

    product_list_table = ProductTable.query.filter_by(id_session=session_id).all()
    if not product_list_table:
        return None
    for product_table in product_list_table:
        product_table.status = new_status
    db.session.commit()
    return [product_table.to_dict() for product_table in product_list_table]