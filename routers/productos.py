from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from DB.conexion import Session as DBSession
from models.modelsDB import Producto
from modelsPydantic import modeloProducto, modeloProductoOut
from typing import List

routerProducto = APIRouter()

# ---------------- OBTENER TODOS LOS PRODUCTOS ----------------
@routerProducto.get("/productos", tags=["Productos"], response_model=List[modeloProductoOut])
def obtener_productos():
    session: Session = DBSession()
    try:
        productos = session.query(Producto).all()
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- OBTENER PRODUCTO POR ID ----------------
@routerProducto.get("/productos/{id}", tags=["Productos"], response_model=modeloProductoOut)
def obtener_producto(id: int):
    session: Session = DBSession()
    try:
        producto = session.query(Producto).filter(Producto.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- CREAR PRODUCTO ----------------
@routerProducto.post("/productos", tags=["Productos"])
def crear_producto(producto: modeloProducto):
    session: Session = DBSession()
    try:
        nuevo_producto = Producto(**producto.dict())
        session.add(nuevo_producto)
        session.commit()
        return JSONResponse(content={"message": "Producto creado exitosamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- ACTUALIZAR PRODUCTO ----------------
@routerProducto.put("/productos/{id}", tags=["Productos"])
def actualizar_producto(id: int, producto: modeloProducto):
    session: Session = DBSession()
    try:
        producto_db = session.query(Producto).filter(Producto.id == id).first()
        if not producto_db:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        for key, value in producto.dict().items():
            setattr(producto_db, key, value)

        session.commit()
        return JSONResponse(content={"message": "Producto actualizado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- ELIMINAR PRODUCTO ----------------
@routerProducto.delete("/productos/{id}", tags=["Productos"])
def eliminar_producto(id: int):
    session: Session = DBSession()
    try:
        producto = session.query(Producto).filter(Producto.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        session.delete(producto)
        session.commit()
        return JSONResponse(content={"message": "Producto eliminado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
