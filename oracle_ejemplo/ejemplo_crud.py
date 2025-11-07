import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(iuser=username, password=password, dsn=dsn)

def create_table_personas():
    query = (
        "CREATE TABLE personas ("
        "rut  VARCHAR2(50) PRIMARY KEY,"
        "nombres"
        "apellidos varchar2(200) personas ("
        "fehca_nacimiento DATE,"
        "cod_area VARCHAR2(20),"
        "numero_telefono VARCHAR2(50)"
    )

    try: 
        with get_connection() as conn: 
            with conn.cursor() as cur: 
                cur.execute(query) 
                print("Tabla 'personas' creada.") 
    except oracledb.DatabaseError as error: 
        print(f"No se pudo crear la tabla: {error}") 