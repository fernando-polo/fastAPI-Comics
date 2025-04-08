from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from DB.conexion import Session as DBSession
from models.modelsDB import Categoria
from modelsPydantic import modeloCategoria, modeloCategoriaOut
from typing import List

routerCategoria = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

# ---------------- CREAR CATEGORÍA ----------------
@routerCategoria.post('/categorias', tags=['Categorias'], response_model=modeloCategoriaOut)
def crear_categoria(categoria: modeloCategoria, db: Session = Depends(get_db)):
    existente = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    nueva_categoria = Categoria(**categoria.dict())
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

# ---------------- OBTENER TODAS LAS CATEGORÍAS ----------------
@routerCategoria.get('/categorias', tags=['Categorias'], response_model=List[modeloCategoriaOut])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

# ---------------- OBTENER CATEGORÍA POR ID ----------------
@routerCategoria.get('/categorias/{id}', tags=['Categorias'], response_model=modeloCategoriaOut)
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# ---------------- ACTUALIZAR CATEGORÍA ----------------
@routerCategoria.put('/categorias/{id}', tags=['Categorias'])
def actualizar_categoria(id: int, categoria: modeloCategoria, db: Session = Depends(get_db)):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for key, value in categoria.dict().items():
        setattr(cat, key, value)
    db.commit()
    return JSONResponse(content={"message": "Categoría actualizada correctamente"})

# ---------------- ELIMINAR CATEGORÍA ----------------
@routerCategoria.delete('/categorias/{id}', tags=['Categorias'])
def eliminar_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()
    return JSONResponse(content={"message": "Categoría eliminada correctamente"})
