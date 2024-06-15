""" 
    Definicion de modelos de base de datos, las tablas que se van a crear en la base de datos
"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, unique=True, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    sesiones = db.relationship('SesionMesa', backref='mesa', lazy=True)
    estado = db.Column(db.String(50), nullable=False, default='disponible')
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_mesa': self.numero_mesa,
            'id_cliente': self.id_cliente,
            'estado': self.estado,
            'sesiones': [sesion.to_dict() for sesion in self.sesiones if sesion.estado == 'activa']
        }
    
class SesionMesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    productos = db.relationship('MesaProducto', backref='sesion', lazy=True)
    estado = db.Column(db.String(50), nullable=False, default='activa')
    
    def to_dict(self):
        return {
            'id_sesion': self.id,
            'id_mesa': self.id_mesa,
            'id_cliente': self.id_cliente,
            'estado': self.estado,
            'productos': [producto.to_dict() for producto in self.productos]
        }
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
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
class MesaProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion_mesa.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    estado = db.Column(db.String(50), nullable=False, default='pendiente')
    def to_dict(self):
        producto = Producto.query.get(self.id_producto)
        return {
            'id': self.id,
            'id_sesion': self.id_sesion,
            'id_producto': self.id_producto,
            'nombre_producto': producto.nombre if producto else None,
            'cantidad': self.cantidad,
            'estado': self.estado
        }
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, default='Cliente')
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }
class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'id_mesa': self.id_mesa,
            'total': self.total,
            'metodo_pago': self.metodo_pago,
            'fecha': self.fecha,
            'detalles': [detalle.to_dict() for detalle in self.detalles]
        }
class DetalleFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    def to_dict(self):
        producto = Producto.query.get(self.id_producto)
        return {
            'id': self.id,
            'id_factura': self.id_factura,
            'id_producto': self.id_producto,
            'nombre_producto': producto.nombre if producto else None,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }
        
        
        ## AUTENTIFICAR USUARIOS
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    restaurant_name = db.Column(db.String(255))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')

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