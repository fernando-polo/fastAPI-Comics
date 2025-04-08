from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from DB.conexion import Session as DBSession
from models.modelsDB import Promocion
from modelsPydantic import modeloPromocion, modeloPromocionOut
from typing import List

routerPromocion = APIRouter()

# ---------------- OBTENER TODAS LAS PROMOCIONES ----------------
@routerPromocion.get("/promociones", tags=["Promociones"], response_model=List[modeloPromocionOut])
def obtener_promociones():
    session: Session = DBSession()
    try:
        promociones = session.query(Promocion).all()
        return promociones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- OBTENER PROMOCION POR ID ----------------
@routerPromocion.get("/promociones/{id}", tags=["Promociones"], response_model=modeloPromocionOut)
def obtener_promocion(id: int):
    session: Session = DBSession()
    try:
        promocion = session.query(Promocion).filter(Promocion.id == id).first()
        if not promocion:
            raise HTTPException(status_code=404, detail="Promoción no encontrada")
        return promocion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- CREAR PROMOCION ----------------
@routerPromocion.post("/promociones", tags=["Promociones"])
def crear_promocion(promocion: modeloPromocion):
    session: Session = DBSession()
    try:
        nueva = Promocion(**promocion.dict())
        session.add(nueva)
        session.commit()
        return JSONResponse(content={"message": "Promoción creada exitosamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- ACTUALIZAR PROMOCION ----------------
@routerPromocion.put("/promociones/{id}", tags=["Promociones"])
def actualizar_promocion(id: int, promocion: modeloPromocion):
    session: Session = DBSession()
    try:
        promocion_db = session.query(Promocion).filter(Promocion.id == id).first()
        if not promocion_db:
            raise HTTPException(status_code=404, detail="Promoción no encontrada")

        for key, value in promocion.dict().items():
            setattr(promocion_db, key, value)

        session.commit()
        return JSONResponse(content={"message": "Promoción actualizada correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- ELIMINAR PROMOCION ----------------
@routerPromocion.delete("/promociones/{id}", tags=["Promociones"])
def eliminar_promocion(id: int):
    session: Session = DBSession()
    try:
        promocion = session.query(Promocion).filter(Promocion.id == id).first()
        if not promocion:
            raise HTTPException(status_code=404, detail="Promoción no encontrada")

        session.delete(promocion)
        session.commit()
        return JSONResponse(content={"message": "Promoción eliminada correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
