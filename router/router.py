from typing import List
from fastapi import APIRouter, HTTPException, status
from config.db import engine
from model.users import users
from schema.user_schema import UserSchema
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

user = APIRouter()

# Ruta para verificar que el router funciona correctamente
@user.get("/")
def root():
    return {"message": "Hi, I am FastAPI with a Router" " " "Developers"}

@user.get("/api/user", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()

    users_list = []
    for row in result:
        user_data = dict(row)
        user_id = user_data.pop("id", None)
        if user_id is not None:
            user_data["id"] = str(user_id)
        users_list.append(UserSchema(**user_data))

    return users_list

from fastapi import status

# Ruta para eliminar un usuario por su ID
@user.delete("/api/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    try:
        with engine.connect() as conn:
            # Verificar si el usuario existe antes de eliminarlo
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")

            # Eliminar el usuario de la base de datos
            conn.execute(users.delete().where(users.c.id == user_id))
    except Exception as e:
        # Agregar un mensaje de error con la excepción para rastrear el problema
        logger.error(f"Error deleting user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Ruta para crear un nuevo usuario
@user.post("/api/user", status_code=status.HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        try:
            result = conn.execute(users.insert().values(new_user))
            new_user_id = result.lastrowid  # Obtener el ID del nuevo usuario creado
            new_user["id"] = new_user_id
            return new_user

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error creating user")

# Ruta para actualizar un usuario por su ID
@user.put("/api/user/{user_id}", response_model=UserSchema)
def update_user(user_id: str, data_update: UserSchema):
    try:
        with engine.connect() as conn:
            user_data = data_update.dict()
            # Convertir el campo 'id' a una cadena
            user_data['id'] = str(user_id)

            # Actualizar el usuario en la base de datos
            conn.execute(
                users.update()
                .values(**user_data)
                .where(users.c.id == user_id)
            )

            # Obtener el usuario actualizado desde la base de datos
            result = conn.execute(users.select().where(users.c.id == user_id)).first()

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Convertir el resultado a un diccionario y luego a un objeto UserSchema
        updated_user = UserSchema(**dict(result))

        return updated_user


    except Exception as e:
        # Agregar un mensaje de error con la excepción para rastrear el problema
        logger.error(f"Error updating user with ID {user_id}: {e}")
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
