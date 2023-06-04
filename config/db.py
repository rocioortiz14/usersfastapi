from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects import mysql

engine = create_engine("mysql+pymysql://root:@localhost:3306/crudusuarios")
conn = engine.connect()


meta_data = MetaData()