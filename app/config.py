import os

from sqlalchemy import create_engine


# Parámetros de conexión a la base de datos
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Motor de base de datos
#engine = create_engine(SQLALCHEMY_DATABASE_URI)
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        print("¡Conexión exitosa a la base de datos!")
except Exception as e:
    print(f"Error de conexión: {e}")
