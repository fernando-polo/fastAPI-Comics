from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from modelsPydantic import modeloUsuario, modeloUsuarioOut, modeloAuth
from DB.conexion import Session
from models.modelsDB import Usuario, Role, UsuarioRol

routerUsuario = APIRouter()

# ---------------- LOGIN ----------------
@routerUsuario.post('/login', tags=['Login'])
def login(usuario: modeloAuth):
    session = Session()
    try:
        user = session.query(Usuario).filter(Usuario.email == usuario.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # COMPARAR EN TEXTO PLANO DIRECTO (NO HASH)
        if user.contrasena != usuario.password:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
        user_role = (
            session.query(Role.nombre)
            .join(UsuarioRol, UsuarioRol.id_rol == Role.id)
            .filter(UsuarioRol.id_usuario == user.id)
            .first()
        )
        
        if not user_role:
            raise HTTPException(status_code=403, detail="Rol no encontrado")

        return JSONResponse(content={
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "role": user_role.nombre
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# ---------------- UPDATE PROFILE ----------------
@routerUsuario.put('/update_profile/{id}', tags=['Usuarios'])
def update_profile(id: int, usuario: modeloUsuario):
    session = Session()
    try:
        user = session.query(Usuario).filter(Usuario.id == id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        user.update(usuario.dict())
        session.commit()

        return JSONResponse(content={"message": "Perfil actualizado exitosamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- GET TODOS LOS USUARIOS ----------------
@routerUsuario.get('/usuarios', tags=['Usuarios'], response_model=List[modeloUsuarioOut])
def obtener_usuarios():
    session = Session()
    try:
        usuarios = session.query(Usuario).all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- GET USUARIO POR ID ----------------
@routerUsuario.get('/usuarios/{id}', tags=['Usuarios'], response_model=modeloUsuarioOut)
def obtener_usuario(id: int):
    session = Session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# ---------------- CREAR NUEVO USUARIO ----------------
@routerUsuario.post('/usuarios', tags=['Usuarios'])
def crear_usuario(usuario: modeloUsuario):
    session = Session()
    try:
        existente = session.query(Usuario).filter(Usuario.email == usuario.email).first()
        if existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        nuevo_usuario = Usuario(**usuario.dict())
        # No aplicamos hash, ya que en la base de datos la contraseña va en texto plano
        session.add(nuevo_usuario)
        session.commit()

        return JSONResponse(content={"message": "Usuario creado exitosamente"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# ---------------- ELIMINAR USUARIO ----------------
@routerUsuario.delete('/usuarios/{id}', tags=['Usuarios'])
def eliminar_usuario(id: int):
    session = Session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        session.delete(usuario)
        session.commit()
        return JSONResponse(content={"message": "Usuario eliminado correctamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
