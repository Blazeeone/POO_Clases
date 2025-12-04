import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN") 
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

def create_schema(query):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                print(f"Tabla creada \n {query}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo crear la tabla: {error}")

def create_all_tables():
    tables = [
            (
                "CREATE TABLE MASCOTAS ("
                "id INTEGER PRIMARY KEY," 
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

# CREATE - Insercion de datos
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

# UPDATE - Actualizacion de datos6
def update_mascota( 
        id: int,
        nombre: Optional[str] = None, 
        edad: Optional[int] = None,
        especie: Optional[str] = None,
        historial_medico: Optional[str] = None,
        dueño_id: Optional[int]= None
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if edad is not None:
        modificaciones.append("edad = :edad")
        parametros["edad"] = edad   
    if especie is not None:
        modificaciones.append("especie = :especie")
        parametros["especie"] = especie
    if historial_medico is not None:
        modificaciones.append("historial_medico = :historial_medico")
        parametros["historial_medico"] = historial_medico
    if dueño_id is not None:
        modificaciones.append("dueño_id = :dueño_id")
        parametros["dueño_id"] = dueño_id
    if not modificaciones:
        return print("No has enviado datos por modificar")
    
    sql = f"UPDATE MASCOTAS SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros)
            connection.commit()
            print("Mascota actualizada exitosamente.")

def update_dueño( 
    id: int,
    nombre: Optional[str] = None, 
    apellido: Optional[str] = None,
    edad: Optional[int] = None,
    rut: Optional[str] = None,
    direccion: Optional[str] = None,
    comuna: Optional[str] = None
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if apellido is not None:
        modificaciones.append("apellido = :apellido")
        parametros["apellido"] = apellido   
    if edad is not None:
        modificaciones.append("edad = :edad")
        parametros["edad"] = edad
    if rut is not None:
        modificaciones.append("rut = :rut")
        parametros["rut"] = rut
    if direccion is not None:
        modificaciones.append("direccion = :direccion")
        parametros["direccion"] = direccion
    if comuna is not None:
        modificaciones.append("comuna = :comuna")
        parametros["comuna"] = comuna
    if not modificaciones:
        return print("No has enviado datos por modificar")
    
    sql = f"UPDATE DUEÑOS SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros)
            connection.commit()
            print("Dueño actualizado exitosamente.")

def update_perro( 
    id: int,
    mascota_id: Optional[int] = None, 
    raza: Optional[str] = None
):
    modificaciones = []
    parametros = {"id": id}

    if mascota_id is not None:
        modificaciones.append("mascota_id = :mascota_id")
        parametros["mascota_id"] = mascota_id
    if raza is not None:
        modificaciones.append("raza = :raza")
        parametros["raza"] = raza   
    if not modificaciones:
        return print("No has enviado datos por modificar")
    
    sql = f"UPDATE PERROS SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros)
            connection.commit()
            print("Perro actualizado exitosamente.")

def update_gato( 
    id: int,
    mascota_id: Optional[int] = None, 
    raza: Optional[str] = None
):
    modificaciones = []
    parametros = {"id": id}

    if mascota_id is not None:
        modificaciones.append("mascota_id = :mascota_id")
        parametros["mascota_id"] = mascota_id
    if raza is not None:
        modificaciones.append("raza = :raza")
        parametros["raza"] = raza   
    if not modificaciones:
        return print("No has enviado datos por modificar")
    
    sql = f"UPDATE GATOS SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros)
            connection.commit()
            print("Gato actualizado exitosamente.")

def update_ave( 
    id: int,
    mascota_id: Optional[int] = None, 
    especie: Optional[str] = None
):
    modificaciones = []
    parametros = {"id": id}

    if mascota_id is not None:
        modificaciones.append("mascota_id = :mascota_id")
        parametros["mascota_id"] = mascota_id
    if especie is not None:
        modificaciones.append("especie = :especie")
        parametros["especie"] = especie   
    if not modificaciones:
        return print("No has enviado datos por modificar")
    
    sql = f"UPDATE AVES SET {', '.join(modificaciones)} WHERE id = :id"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, parametros)
            connection.commit()
            print("Ave actualizada exitosamente.")  

# DELETE - Elminacion de datos
def delete_mascota(id: int):
    sql = (
        "DELETE FROM MASCOTAS WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Mascota eliminada exitosamente. \n {parametros}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar la mascota \n {error} \n {sql} \n {parametros}")

def delete_dueño(id: int):
    sql = (
        "DELETE FROM DUEÑOS WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dueño eliminado exitosamente. \n {parametros}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el dueño \n {error} \n {sql} \n {parametros}")

def delete_perro(id: int):
    sql = (
        "DELETE FROM PERROS WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Perro eliminado exitosamente. \n {parametros}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el perro \n {error} \n {sql} \n {parametros}")

def delete_gato(id: int):
    sql = (
        "DELETE FROM GATOS WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Gato eliminado exitosamente. \n {parametros}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el gato \n {error} \n {sql} \n {parametros}")

def delete_ave(id: int):
    sql = (
        "DELETE FROM AVES WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Ave eliminada exitosamente. \n {parametros}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el ave \n {error} \n {sql} \n {parametros}")

def menu_mascotas():
     while True:
        print(
            """
                MENU: Mascotas
            -----------------------
            1. Insertar una mascota
            2. Consultar todos las mascotas
            3. Consultar Mascota por ID
            4. Modificar una mascota
            5. Eliminar una mascota
            0. Volver al menu principal
            """
            )
        opcion = input("Seleccione una opción: 1-4 (0 para salir): ")

def main():
    while True:
        print(
            """
            CRUD : Oracle + Python
            -----------------------
            1. Crear tablas
            2. Insertar datos 
            3. Actualizar datos 
            4. Eliminar datos 
            0. Salir
            """
            )
        opcion = input("Seleccione una opción: 1-4 (0 para salir): ")

        if opcion == "1":
            create_all_tables()
        elif opcion == "2":
            pass
        elif opcion == "3":
            pass
        elif opcion == "4":
            pass
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")   
            print("PRESIONE ENTER PARA CONTINUAR...")


if __name__ == "__main__":
    main()