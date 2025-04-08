from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from DB.base import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(Text, nullable=False)
    contrasena = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    usuario_roles = relationship("UsuarioRol", back_populates="usuario")

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.contrasena)

    def hash_password(self):
        self.contrasena = pwd_context.hash(self.contrasena)

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)

class UsuarioRol(Base):
    __tablename__ = 'usuarios_roles'
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    id_rol = Column(Integer, ForeignKey('roles.id'), primary_key=True)

    usuario = relationship("Usuario", back_populates="usuario_roles")
    rol = relationship("Role")

class Proveedor(Base):
    __tablename__ = 'proveedores'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    direccion = Column(Text, nullable=True)  # <-- Actualizado para permitir NULL


class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    id_proveedor = Column(Integer, ForeignKey('proveedores.id'), nullable=False)

    categoria = relationship('Categoria')
    proveedor = relationship('Proveedor')

class Inventario(Base):
    __tablename__ = 'inventario'
    id = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey('productos.id'), unique=True, nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    producto = relationship('Producto')

class PedidoUsuario(Base):
    __tablename__ = 'pedidos_usuarios'
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario')

class DetallePedido(Base):
    __tablename__ = 'detalle_pedidos'
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)

    pedido = relationship('Pedido')
    producto = relationship('Producto')

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario')

class DetallePedidoUsuario(Base):
    __tablename__ = 'detalle_pedidos_usuarios'
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos_usuarios.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)

    pedido = relationship('PedidoUsuario')
    producto = relationship('Producto')

class PedidoProveedor(Base):
    __tablename__ = 'pedidos_proveedores'
    id = Column(Integer, primary_key=True, index=True)
    id_proveedor = Column(Integer, ForeignKey('proveedores.id'), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    proveedor = relationship('Proveedor')

class DetallePedidoProveedor(Base):
    __tablename__ = 'detalle_pedidos_proveedores'
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos_proveedores.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)

    pedido = relationship('PedidoProveedor')
    producto = relationship('Producto')

class Promocion(Base):
    __tablename__ = 'promociones'
    id = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    descuento = Column(DECIMAL(10, 2), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)

    producto = relationship("Producto")

class Contacto(Base):
    __tablename__ = 'contacto'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    mensaje = Column(Text, nullable=False)
