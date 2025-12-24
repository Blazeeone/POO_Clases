import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
import datetime

load_dotenv()

class Database:
    def __init__(self, username, dsn, password):
        self.username = username
        self.dsn = dsn
        self.password = password

    def get_connection(self):
        # Conexión 'Thin' mode (no requiere cliente pesado si usas python-oracledb moderno)
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)

    def create_all_tables(self):
        # Oracle requiere bloques PL/SQL para manejar errores si la tabla ya existe
        # Usamos GENERATED ALWAYS AS IDENTITY para que el ID sea automático (Oracle 12c+)
        tables_sql = [
            """
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE USERS (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    username VARCHAR2(50) UNIQUE,
                    password VARCHAR2(128)
                )';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -955 THEN NULL; ELSE RAISE; END IF;
            END;
            """,
            """
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE CONSULTAS (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    user_id INTEGER,
                    indicador VARCHAR2(20),
                    valor FLOAT,
                    fecha_consulta VARCHAR2(20),
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES USERS(id)
                )';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -955 THEN NULL; ELSE RAISE; END IF;
            END;
            """
        ]

        for sql in tables_sql:
            self.query_script(sql)

    def query_script(self, sql):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                conn.commit()
        except oracledb.DatabaseError as error:
            print(f"Nota DB: {error}")

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Ejecutar consulta
                    ejecucion = cur.execute(sql, parameters or {})
                    
                    # Si es un SELECT, devolver los datos
                    if sql.strip().upper().startswith("SELECT"):
                        columnas = [col[0] for col in cur.description]
                        resultado = []
                        for fila in ejecucion:
                            # Convertimos la fila en algo más manejable si es necesario
                            resultado.append(list(fila))
                        return resultado
                    
                conn.commit()
        except oracledb.DatabaseError as error:
            print(f"Error Oracle: {error}")
            # Retornamos lista vacía o lanzamos error según prefieras, 
            # pero mejor no romper la app en el video
            return []

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str):
        # Oracle devuelve tuplas. 
        # Columna 0: id, 1: username, 2: password
        resultado = db.query(
            sql="SELECT id, username, password FROM USERS WHERE username = :username",
            parameters={"username": username}
        )

        if not resultado or len(resultado) == 0:
            return {"message": "Usuario no encontrado", "success": False}

        user_data = resultado[0]
        user_id = user_data[0]
        stored_hash = user_data[2] # El hash guardado en BD

        # Asegurar codificación
        if isinstance(stored_hash, str):
            stored_hash_bytes = stored_hash.encode('utf-8')
        else:
            stored_hash_bytes = stored_hash

        password_bytes = password.encode("UTF-8")

        try:
            if bcrypt.checkpw(password_bytes, stored_hash_bytes):
                return {"message": "Login exitoso", "success": True, "user_id": user_id}
            else:
                return {"message": "Contraseña incorrecta", "success": False}
        except ValueError:
             return {"message": "Error hash corrupto", "success": False}

    @staticmethod
    def register(db: Database, username: str, password: str):
        try:
            if not username or not password:
                return {"message": "Datos incompletos", "success": False}
            
            password_bytes = password.encode("UTF-8")
            salt = bcrypt.gensalt(12)
            hash_password = bcrypt.hashpw(password_bytes, salt)
            # Guardar como string para Oracle VARCHAR2
            hash_str = hash_password.decode('utf-8')

            # NO pasamos ID, dejamos que Oracle lo genere (IDENTITY)
            db.query(
                sql="INSERT INTO USERS(username, password) VALUES (:username, :password)",
                parameters={"username": username, "password": hash_str}
            )
            return {"message": "Usuario creado. Ahora inicia sesión.", "success": True}
        except Exception as error:
            return {"message": f"Error (Usuario ya existe?): {str(error)}", "success": False}

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url

    def get_indicator(self, indicator: str, fecha: str = None):
        try:
            # Lógica API
            if not fecha:
                url = f"{self.base_url}/{indicator}"
            else:
                url = f"{self.base_url}/{indicator}/{fecha}"
            
            respuesta = requests.get(url, timeout=5).json()
            
            if "serie" in respuesta and len(respuesta["serie"]) > 0:
                valor = respuesta["serie"][0]["valor"]
                return {"valor": valor, "success": True}
            
            return {"message": "Sin datos para esa fecha", "success": False}

        except Exception as error:
            return {"message": "Error de conexión API", "success": False}

class History:
    @staticmethod
    def save_query(db: Database, user_id: int, indicator: str, value: float, date_query: str):
        try:
            # En Oracle, CURRENT_TIMESTAMP se maneja en el DEFAULT de la tabla, 
            # solo insertamos los datos manuales.
            db.query(
                sql="INSERT INTO CONSULTAS (user_id, indicador, valor, fecha_consulta) VALUES (:u, :i, :v, :f)",
                parameters={"u": user_id, "i": indicator, "v": value, "f": date_query}
            )
            return True
        except Exception:
            return False

    @staticmethod
    def get_history(db: Database, user_id: int):
        # Oracle 12c+ soporta OFFSET/FETCH, pero para seguridad usamos ROWNUM o simple ORDER BY
        sql = """
            SELECT indicador, valor, fecha_consulta 
            FROM CONSULTAS 
            WHERE user_id = :u 
            ORDER BY fecha_registro DESC
        """
        return db.query(sql, {"u": user_id})