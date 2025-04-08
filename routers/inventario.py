from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from DB.conexion import Session as DBSession
from models.modelsDB import Inventario
from modelsPydantic import modeloInventario, modeloInventarioOut
from typing import List

routerInventario = APIRouter()

# ---------------- OBTENER TODO EL INVENTARIO ----------------
@routerInventario.get("/inventario", tags=["Inventario"], response_model=List[modeloInventarioOut])
def obtener_inventario():
    session: Session = DBSession()
    try:
        inventario = session.query(Inventario).all()
        return inventario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- OBTENER INVENTARIO POR ID ----------------
@routerInventario.get("/inventario/{id}", tags=["Inventario"], response_model=modeloInventarioOut)
def obtener_inventario_id(id: int):
    session: Session = DBSession()
    try:
        item = session.query(Inventario).filter(Inventario.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- CREAR ENTRADA DE INVENTARIO ----------------
@routerInventario.post("/inventario", tags=["Inventario"])
def crear_inventario(item: modeloInventario):
    session: Session = DBSession()
    try:
        nuevo = Inventario(**item.dict())
        session.add(nuevo)
        session.commit()
        return JSONResponse(content={"message": "Inventario creado exitosamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- ACTUALIZAR INVENTARIO ----------------
@routerInventario.put("/inventario/{id}", tags=["Inventario"])
def actualizar_inventario(id: int, item: modeloInventario):
    session: Session = DBSession()
    try:
        inventario = session.query(Inventario).filter(Inventario.id == id).first()
        if not inventario:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        for key, value in item.dict().items():
            setattr(inventario, key, value)

        session.commit()
        return JSONResponse(content={"message": "Inventario actualizado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- ELIMINAR INVENTARIO ----------------
@routerInventario.delete("/inventario/{id}", tags=["Inventario"])
def eliminar_inventario(id: int):
    session: Session = DBSession()
    try:
        item = session.query(Inventario).filter(Inventario.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        session.delete(item)
        session.commit()
        return JSONResponse(content={"message": "Inventario eliminado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
