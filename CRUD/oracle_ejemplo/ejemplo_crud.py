import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(iuser=username, password=password, dsn=dsn)

def create_schema(query):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                print(f"Tabla creada \n {query}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo crear la tabla: {error}")

def create_table_mascota():
    tables = [
            (
                "CREATE TABLE MASCOTAS ("
                "id INTEGER PRIMARTY KEY,"
                "nombre VARCHAR(50),"
                "edad INTEGER,"
                "especie VARCHAR(20),"
                "historial_medico TEXT,"
                "dueño_id INTEGER,"
                "FOREIGN KEY (dueño_id) REFERENCES DUEÑOS(id)"
                ")"
            ),
            (
                "CREATE TABLE DUEÑOS ("
                "id INTEGER PRIMARY KEY,"
                "nombre VARCHAR(50),"
                "apellido VARCHAR(50),"
                "edad INTEGER,"
                "rut VARCHAR(10),"
                "direccion VARCHAR(100)"
                "comuna VARCHAR(30)"
                ")"
            ),
            (
                "CREATE TABLE PERROS ("
                "id INTEGER PRIMARY KEY,"
                "mascota_id INTEGER,"
                "raza VARCHAR(20),"
                ")"
            ),
            (
                "CREATE TABLE GATOS ("
                "id INTEGER PRIMARY KEY,"
                "mascota_id INTEGER,"
                "raza VARCHAR(20)"
                ")"
            ),
            (
                "CREATE TABLE AVES ("
                "id INTEGER PRIMARY KEY,"
                "mascota_id INTEGER,"
                "especie VARCHAR(20)"
                ")"
            ),
    ]
    for query in tables:
            create_schema(query)

from datetime import datetime
def create_mascota(
    id,
    nombre,
    edad, 
    especie,
    historial_medico,
    dueño_id
):
    sql = (
        "INSERT INTO MASCOTAS (id, nombre, edad, especie, historial_medico, dueño_id) "
        "VALUES (:id, :nombre, :edad, :especie, :historial_medico, :dueño_id)"
    )

    parametros = {
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
        "historial_medico": historial_medico,
        "dueño_id": dueño_id
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Mascota creada exitosamente.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar la mascota \n {error} \n {sql} \n {parametros}")

def create_table_dueño(
    id,
    nombre,
    apellido,
    edad,
    rut,
    direccion,
    comuna
):
    sql = (
        "INSERT INTO DUEÑOS (id, nombre, apellido, edad, rut, direccion, comuna) "
        "VALUES (:id, :nombre, :apellido, :edad, :rut, :direccion, :comuna)"
    )

    parametros = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "rut": rut,
        "direccion": direccion,
        "comuna": comuna
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Dueño creado exitosamente.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dueño \n {error} \n {sql} \n {parametros}")

def create_perro(
    id,
    mascota_id,
    raza
):
    sql = (
        "INSERT INTO PERROS (id, mascota_id, raza) "
        "VALUES (:id, :mascota_id, :raza)"
    )

    parametros = {
        "id": id,
        "mascota_id": mascota_id,
        "raza": raza
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")

def create_gato(
    id,
    mascota_id,
    raza
):
    sql = (
        "INSERT INTO GATOS (id, mascota_id, raza) "
        "VALUES (:id, :mascota_id, :raza)"
    )

    parametros = {
        "id": id,
        "mascota_id": mascota_id,
        "raza": raza
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")   

def create_ave(
    id,
    mascota_id,
    especie
):
    sql = (
        "INSERT INTO AVES (id, mascota_id, especie) "
        "VALUES (:id, :mascota_id, :especie)"
    )

    parametros = {
        "id": id,
        "mascota_id": mascota_id,
        "especie": especie
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")    
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")

            