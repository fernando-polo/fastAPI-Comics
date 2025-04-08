from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from DB.conexion import engine
from DB.base import Base  # Base ya viene de archivo separado
from routers.usuarios import routerUsuario
from routers.categorias import routerCategoria
from routers.productos import routerProducto
from routers.inventario import routerInventario
from routers.promociones import routerPromocion
from routers.pedidos import routerPedidos
from routers.detalles import routerDetalles
from routers.proveedores import routerProveedores

app = FastAPI(
    title='API Comics',
    description='API para la tienda de cómics',
    version='1.0.1'
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto para producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Crear tablas (solo si no existen)
Base.metadata.create_all(bind=engine)

# Ruta de prueba
@app.get('/', tags=['Hello'])
def home():
    return {'hello': 'world FastAPI'}

# Ruta de usuario
app.include_router(routerUsuario)
# Ruta de las Categorías
app.include_router(routerCategoria)
# Ruta de los Proveedores
app.include_router(routerProveedores)
# Ruta de los Productos
app.include_router(routerProducto)
# Ruta del Inventario
app.include_router(routerInventario)
# Ruta de las Promociones
app.include_router(routerPromocion)
# Ruta de los Pedidos
app.include_router(routerPedidos)
# Ruta de los Detalles
app.include_router(routerDetalles)
