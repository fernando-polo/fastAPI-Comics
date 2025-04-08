from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from DB.conexion import Session
from models.modelsDB import Pedido, PedidoUsuario
from modelsPydantic import modeloPedido, modeloPedidoOut, modeloPedidoUsuario, modeloPedidoUsuarioOut

routerPedidos = APIRouter()

# ------------------- PEDIDOS GENERALES -------------------
@routerPedidos.get("/pedidos", response_model=List[modeloPedidoOut], tags=["Pedidos"])
def obtener_pedidos():
    session = Session()
    try:
        pedidos = session.query(Pedido).all()
        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerPedidos.get("/pedidos/{id}", response_model=modeloPedidoOut, tags=["Pedidos"])
def obtener_pedido(id: int):
    session = Session()
    try:
        pedido = session.query(Pedido).filter(Pedido.id == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerPedidos.post("/pedidos", tags=["Pedidos"])
def crear_pedido(pedido: modeloPedido):
    session = Session()
    try:
        nuevo = Pedido(**pedido.dict())
        session.add(nuevo)
        session.commit()
        return JSONResponse(content={"message": "Pedido creado exitosamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerPedidos.delete("/pedidos/{id}", tags=["Pedidos"])
def eliminar_pedido(id: int):
    session = Session()
    try:
        pedido = session.query(Pedido).filter(Pedido.id == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        session.delete(pedido)
        session.commit()
        return JSONResponse(content={"message": "Pedido eliminado correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ------------------- PEDIDOS USUARIO -------------------
@routerPedidos.get("/pedidos_usuarios", response_model=List[modeloPedidoUsuarioOut], tags=["Pedidos Usuarios"])
def obtener_pedidos_usuarios():
    session = Session()
    try:
        pedidos = session.query(PedidoUsuario).all()
        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerPedidos.get("/pedidos_usuarios/{id}", response_model=modeloPedidoUsuarioOut, tags=["Pedidos Usuarios"])
def obtener_pedido_usuario(id: int):
    session = Session()
    try:
        pedido = session.query(PedidoUsuario).filter(PedidoUsuario.id == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerPedidos.post("/pedidos_usuarios", tags=["Pedidos Usuarios"])
def crear_pedido_usuario(pedido: modeloPedidoUsuario):
    session = Session()
    try:
        nuevo = PedidoUsuario(**pedido.dict())
        session.add(nuevo)
        session.commit()
        return JSONResponse(content={"message": "Pedido de usuario creado exitosamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@routerPedidos.delete("/pedidos_usuarios/{id}", tags=["Pedidos Usuarios"])
def eliminar_pedido_usuario(id: int):
    session = Session()
    try:
        pedido = session.query(PedidoUsuario).filter(PedidoUsuario.id == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        session.delete(pedido)
        session.commit()
        return JSONResponse(content={"message": "Pedido de usuario eliminado correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
