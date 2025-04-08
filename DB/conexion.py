# Ambiente local
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.base import Base  # Usamos Base desde archivo separado

# Datos de conexión
USER = "root"
PASSWORD = "GtYxEWnnVoGIKcBCInnyadvKGlnMBOTO"  # Si tienes contraseña, colócala aquí
HOST = "interchange.proxy.rlwy.net"
PORT = "53650"
DB_NAME = "railway"

# URL de conexión a MySQL con PyMySQL
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Crear la sesión local
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # Railway
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from DB.base import Base
# from dotenv import load_dotenv

# # Cargar variables desde .env si existe (solo en entorno local)
# load_dotenv()

# # Variables de entorno
# USER = os.getenv("DB_USER", "root")
# PASSWORD = os.getenv("DB_PASSWORD", "")
# HOST = os.getenv("DB_HOST", "localhost")
# PORT = os.getenv("DB_PORT", "3306")
# DB_NAME = os.getenv("DB_NAME", "tienda_comics")

# # URL de conexión a MySQL
# DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# # Crear el motor
# engine = create_engine(DATABASE_URL, echo=True)

# # Crear sesión
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
