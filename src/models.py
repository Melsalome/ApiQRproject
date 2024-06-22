""" 
    Definicion de modelos de base de datos, las tablas que se van a crear en la base de datos
"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    restaurant_name = db.Column(db.String(255))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'status': "ok"
        }

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    menus = db.relationship('Menu', backref='restaurant', lazy=True)

    def __repr__(self):
        return f'<Restaurant {self.name}>'
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image
        }

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    sessions = db.relationship('TableSession', backref='table', lazy=True)
    status = db.Column(db.String(50), nullable=False, default='available')
    restaurant = db.relationship('Restaurant', backref=db.backref('tables', lazy=True))
    def to_dict(self):
        return {
            'id': self.id,
            'table_number': self.table_number,
            "restaurant_id": self.restaurant_id,
            'id_client': self.id_client,
            'status': self.status,
            'sessions': [sesion.to_dict() for sesion in self.sessions if sesion.status == 'active']
        }

class TableSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_table = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    products = db.relationship('ProductTable', backref='session', lazy=True)
    status = db.Column(db.String(50), nullable=False, default='active')
    
    def to_dict(self):
        return {
            'id_session': self.id,
            'id_table': self.id_table,
            'id_client': self.id_client,
            'status': self.status,
            'products': [product.to_dict() for product in self.products]
        }
        
        
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(255))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image': self.image,
            'category' : self.category
        }
        
        
class ProductTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_session = db.Column(db.Integer, db.ForeignKey('table_session.id'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(50), nullable=False, default='pending')
    def to_dict(self):
        product = Product.query.get(self.id_product)
        return {
            'id': self.id,
            'id_session': self.id_session,
            'id_product': self.id_product,
            'product_name': product.name if product else None,
            'quantity': self.quantity,
            'status': self.status
        }
        
        
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, default='Client')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
        
        
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_table = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    summary = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    details = db.relationship('InvoiceDetail', backref='invoice', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'id_table': self.id_table,
            'summary': self.summary,
            'payment_method': self.payment_method,
            'date': self.date,
            'details': [detail.to_dict() for detail in self.details]
        }
        
        
class InvoiceDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_invoice = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    def to_dict(self):
        product = Product.query.get(self.id_product)
        return {
            'id': self.id,
            'id_invoice': self.id_invoice,
            'id_product': self.id_product,
            'nombre_product': product.nombre if product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal
        }
    

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def __repr__(self):
        return f'<Menu {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "image": self.image,
            "restaurant_id": self.restaurant_id
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, nullable=False)
    table_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    payment_method = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "table_id": self.table_id,
            "comment": self.comment,
            "payment_method": self.payment_method,
            "total_price": self.total_price,
            "order_items": [item.serialize() for item in self.order_items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return f'<OrderItem {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "menu_id": self.menu_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
          
        }       
       