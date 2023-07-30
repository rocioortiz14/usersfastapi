from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data
from pydantic import BaseModel, constr

# Definimos el modelo Pydantic para validar los campos del usuario
class UserSchema(BaseModel):
    name: constr(max_length=255)
    age: int
    address: constr(max_length=255)
    skills: str
    languages: str

# Creamos la tabla de usuarios en la base de datos
users = Table(
    "users",
    meta_data,
    Column("id", String(5), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("age", String(255), nullable=False),
    Column("address", String(255), nullable=False),
    Column("skills", String(255), nullable=False),
    Column("languages", String(255), nullable=False),
)

meta_data.create_all(engine)
