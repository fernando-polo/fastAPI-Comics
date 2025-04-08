from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from DB.conexion import Session
from models.modelsDB import Proveedor
from modelsPydantic import modeloProveedor, modeloProveedorOut

routerProveedores = APIRouter()

# Obtener todos los proveedores
@routerProveedores.get("/proveedores", response_model=list[modeloProveedorOut], tags=["Proveedores"])
def obtener_proveedores():
    session = Session()
    try:
        return session.query(Proveedor).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# Obtener proveedor por ID
@routerProveedores.get("/proveedores/{id}", response_model=modeloProveedorOut, tags=["Proveedores"])
def obtener_proveedor(id: int):
    session = Session()
    try:
        proveedor = session.query(Proveedor).filter(Proveedor.id == id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        return proveedor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# Crear nuevo proveedor
@routerProveedores.post("/proveedores", tags=["Proveedores"])
def crear_proveedor(data: modeloProveedor):
    session = Session()
    try:
        nuevo = Proveedor(**data.dict(exclude_unset=True))
        session.add(nuevo)
        session.commit()
        return JSONResponse(content={"message": "Proveedor creado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# Actualizar proveedor
@routerProveedores.put("/proveedores/{id}", tags=["Proveedores"])
def actualizar_proveedor(id: int, data: modeloProveedor):
    session = Session()
    try:
        proveedor = session.query(Proveedor).filter(Proveedor.id == id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        for k, v in data.dict(exclude_unset=True).items():
            setattr(proveedor, k, v)
        session.commit()
        return JSONResponse(content={"message": "Proveedor actualizado correctamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# Eliminar proveedor
@routerProveedores.delete("/proveedores/{id}", tags=["Proveedores"])
def eliminar_proveedor(id: int):
    session = Session()
    try:
        proveedor = session.query(Proveedor).filter(Proveedor.id == id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        session.delete(proveedor)
        session.commit()
        return JSONResponse(content={"message": "Proveedor eliminado correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
