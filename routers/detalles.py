from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from DB.conexion import Session
from models.modelsDB import DetallePedido, DetallePedidoUsuario, DetallePedidoProveedor
from modelsPydantic import (
    modeloDetallePedido, modeloDetallePedidoOut,
    modeloDetallePedidoUsuario, modeloDetallePedidoUsuarioOut,
    modeloDetallePedidoProveedor, modeloDetallePedidoProveedorOut
)

routerDetalles = APIRouter()

# ----------- DETALLE PEDIDOS -----------
@routerDetalles.get("/detalle_pedidos", response_model=list[modeloDetallePedidoOut], tags=["DetallePedidos"])
def obtener_detalle_pedidos():
    session = Session()
    try:
        return session.query(DetallePedido).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.get("/detalle_pedidos/{id}", response_model=modeloDetallePedidoOut, tags=["DetallePedidos"])
def obtener_detalle_pedido(id: int):
    session = Session()
    try:
        detalle = session.query(DetallePedido).filter(DetallePedido.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return detalle
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.post("/detalle_pedidos", tags=["DetallePedidos"])
def crear_detalle_pedido(data: modeloDetallePedido):
    session = Session()
    try:
        nuevo = DetallePedido(**data.dict())
        session.add(nuevo)
        session.commit()
        return JSONResponse(content={"message": "Detalle de pedido creado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.put("/detalle_pedidos/{id}", tags=["DetallePedidos"])
def actualizar_detalle_pedido(id: int, data: modeloDetallePedido):
    session = Session()
    try:
        detalle = session.query(DetallePedido).filter(DetallePedido.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        for k, v in data.dict().items():
            setattr(detalle, k, v)
        session.commit()
        return JSONResponse(content={"message": "Detalle actualizado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.delete("/detalle_pedidos/{id}", tags=["DetallePedidos"])
def eliminar_detalle_pedido(id: int):
    session = Session()
    try:
        detalle = session.query(DetallePedido).filter(DetallePedido.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        session.delete(detalle)
        session.commit()
        return JSONResponse(content={"message": "Detalle eliminado correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ----------- DETALLE PEDIDOS USUARIOS -----------
@routerDetalles.get("/detalle_pedidos_usuarios", response_model=list[modeloDetallePedidoUsuarioOut], tags=["DetallePedidosUsuarios"])
def obtener_detalle_pedidos_usuarios():
    session = Session()
    try:
        return session.query(DetallePedidoUsuario).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.get("/detalle_pedidos_usuarios/{id}", response_model=modeloDetallePedidoUsuarioOut, tags=["DetallePedidosUsuarios"])
def obtener_detalle_pedido_usuario(id: int):
    session = Session()
    try:
        detalle = session.query(DetallePedidoUsuario).filter(DetallePedidoUsuario.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return detalle
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.post("/detalle_pedidos_usuarios", tags=["DetallePedidosUsuarios"])
def crear_detalle_pedido_usuario(data: modeloDetallePedidoUsuario):
    session = Session()
    try:
        nuevo = DetallePedidoUsuario(**data.dict())
        session.add(nuevo)
        session.commit()
        return JSONResponse(content={"message": "Detalle de pedido de usuario creado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.put("/detalle_pedidos_usuarios/{id}", tags=["DetallePedidosUsuarios"])
def actualizar_detalle_pedido_usuario(id: int, data: modeloDetallePedidoUsuario):
    session = Session()
    try:
        detalle = session.query(DetallePedidoUsuario).filter(DetallePedidoUsuario.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        for k, v in data.dict().items():
            setattr(detalle, k, v)
        session.commit()
        return JSONResponse(content={"message": "Detalle actualizado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.delete("/detalle_pedidos_usuarios/{id}", tags=["DetallePedidosUsuarios"])
def eliminar_detalle_pedido_usuario(id: int):
    session = Session()
    try:
        detalle = session.query(DetallePedidoUsuario).filter(DetallePedidoUsuario.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        session.delete(detalle)
        session.commit()
        return JSONResponse(content={"message": "Detalle eliminado correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ----------- DETALLE PEDIDOS PROVEEDORES -----------
@routerDetalles.get("/detalle_pedidos_proveedores", response_model=list[modeloDetallePedidoProveedorOut], tags=["DetallePedidosProveedores"])
def obtener_detalle_pedidos_proveedores():
    session = Session()
    try:
        return session.query(DetallePedidoProveedor).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.get("/detalle_pedidos_proveedores/{id}", response_model=modeloDetallePedidoProveedorOut, tags=["DetallePedidosProveedores"])
def obtener_detalle_pedido_proveedor(id: int):
    session = Session()
    try:
        detalle = session.query(DetallePedidoProveedor).filter(DetallePedidoProveedor.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return detalle
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.post("/detalle_pedidos_proveedores", tags=["DetallePedidosProveedores"])
def crear_detalle_pedido_proveedor(data: modeloDetallePedidoProveedor):
    session = Session()
    try:
        nuevo = DetallePedidoProveedor(**data.dict())
        session.add(nuevo)
        session.commit()
        return JSONResponse(content={"message": "Detalle de pedido de proveedor creado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.put("/detalle_pedidos_proveedores/{id}", tags=["DetallePedidosProveedores"])
def actualizar_detalle_pedido_proveedor(id: int, data: modeloDetallePedidoProveedor):
    session = Session()
    try:
        detalle = session.query(DetallePedidoProveedor).filter(DetallePedidoProveedor.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        for k, v in data.dict().items():
            setattr(detalle, k, v)
        session.commit()
        return JSONResponse(content={"message": "Detalle actualizado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerDetalles.delete("/detalle_pedidos_proveedores/{id}", tags=["DetallePedidosProveedores"])
def eliminar_detalle_pedido_proveedor(id: int):
    session = Session()
    try:
        detalle = session.query(DetallePedidoProveedor).filter(DetallePedidoProveedor.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        session.delete(detalle)
        session.commit()
        return JSONResponse(content={"message": "Detalle eliminado correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
