from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal

# ------------------ USUARIOS ------------------

class modeloUsuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    telefono: str = Field(..., min_length=10, max_length=20, description="Número telefónico con lada")
    direccion: str = Field(..., min_length=5, description="Dirección del usuario")
    contrasena: str = Field(..., min_length=6, max_length=255, description="Contraseña segura")

class modeloUsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: str
    direccion: str
    contrasena: str
    fecha_registro: datetime

    class Config:
        from_attributes = True

class modeloAuth(BaseModel):
    email: EmailStr
    password: str

# ------------------ ROLES ------------------

class modeloRole(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)

class modeloRoleOut(modeloRole):
    id: int

    class Config:
        from_attributes = True

# ------------------ PROVEEDORES ------------------

class modeloProveedor(BaseModel):
    nombre: str = Field(..., min_length=3)
    contacto: str = Field(..., min_length=3)
    telefono: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    direccion: Optional[str] = Field(None, min_length=3)  # <-- Ahora es opcional

class modeloProveedorOut(modeloProveedor):
    id: int

    class Config:
        from_attributes = True

# ------------------ CATEGORIAS ------------------

class modeloCategoria(BaseModel):
    nombre: str = Field(..., min_length=3)

class modeloCategoriaOut(modeloCategoria):
    id: int

    class Config:
        from_attributes = True

# ------------------ PRODUCTOS ------------------

class modeloProducto(BaseModel):
    nombre: str = Field(..., min_length=3)
    descripcion: str = Field(..., min_length=5)
    precio: Decimal = Field(..., ge=0, description="Precio positivo")
    id_categoria: int
    id_proveedor: int

class modeloProductoOut(modeloProducto):
    id: int

    class Config:
        from_attributes = True

# ------------------ INVENTARIO ------------------

class modeloInventario(BaseModel):
    id_producto: int
    stock: int = Field(..., ge=0, description="Stock debe ser igual o mayor a 0")

class modeloInventarioOut(modeloInventario):
    id: int

    class Config:
        from_attributes = True

# ------------------ PEDIDOS USUARIOS ------------------

class modeloPedidoUsuario(BaseModel):
    id_usuario: int
    total: Decimal = Field(..., ge=0)

class modeloPedidoUsuarioOut(modeloPedidoUsuario):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True

# ------------------ DETALLE PEDIDO ------------------

class modeloDetallePedido(BaseModel):
    id_pedido: int
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio: Decimal = Field(..., ge=0)

class modeloDetallePedidoOut(modeloDetallePedido):
    id: int

    class Config:
        from_attributes = True

# ------------------ DETALLE PEDIDO USUARIO ------------------

class modeloDetallePedidoUsuario(BaseModel):
    id_pedido: int
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., ge=0)

class modeloDetallePedidoUsuarioOut(modeloDetallePedidoUsuario):
    id: int

    class Config:
        from_attributes = True

# ------------------ PEDIDOS PROVEEDORES ------------------

class modeloPedidoProveedor(BaseModel):
    id_proveedor: int
    total: Decimal = Field(..., ge=0)

class modeloPedidoProveedorOut(modeloPedidoProveedor):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True

# ------------------ DETALLE PEDIDO PROVEEDOR ------------------

class modeloDetallePedidoProveedor(BaseModel):
    id_pedido: int
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., ge=0)

class modeloDetallePedidoProveedorOut(modeloDetallePedidoProveedor):
    id: int

    class Config:
        from_attributes = True

# ------------------ PEDIDOS ------------------

class modeloPedido(BaseModel):
    id_usuario: int
    total: Decimal = Field(..., ge=0)

class modeloPedidoOut(modeloPedido):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True

# ------------------ PROMOCIONES ------------------

class modeloPromocion(BaseModel):
    id_producto: int
    descuento: Decimal = Field(..., ge=0)
    fecha_inicio: datetime
    fecha_fin: datetime

class modeloPromocionOut(modeloPromocion):
    id: int

    class Config:
        from_attributes = True

# ------------------ CONTACTO ------------------

class modeloContacto(BaseModel):
    nombre: str = Field(..., min_length=3)
    email: EmailStr
    mensaje: str = Field(..., min_length=5)

class modeloContactoOut(modeloContacto):
    id: int

    class Config:
        from_attributes = True
