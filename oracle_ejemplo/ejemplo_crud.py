import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(iuser=username, password=password, dsn=dsn)


def create_schrema():
    
    tables = [
        (
            "CREAATE TABLE"
            "MASCOTAS ("
            "id INTEGER PRIMARTY KEY,"
            "nombre VARCHAR(50),"
            "edad INTEGER,"
            "especie VARCHAR(30)"

            "CREATE TABLE"
            "DUEÑOS ("
            "id INTEGER PRIMARY KEY,"
            "nombre VARCHAR(50),"
            "telefono VARCHAR(15),"
            "direccion VARCHAR(100)"

        )
    ]