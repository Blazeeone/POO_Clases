# Conectarnos a la base de datos 
import oracledb
# Rescatar variavles de entorno
import os
# Implementar hasheo de contraseñas
import bcrypt
# Implementar peticiones HTTP
import requests
from dotenv import load_dotenv
# Importar tipo de dato Optional    
from typing import Optional
# Importar libreria de fechas
import datetime
# Carnar las variables desde el archivo .env
load_dotenv()
# Rescatar las credenciales de conexion con Oracle
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
    def __init__(self,username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    def create_all_tables(self):
        pass
    def query(self, sentence: str, parameters: Optional[dict] = None):
        print(f"Ejecutando query:\n{sentence}\nParametros:\n{parameters}")
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    resultado = cursor.execute(sentence, parameters)
                    return resultado
                connection.commit()
        except oracledb.DatabaseError as error:
            print(f"Hubo un error en la base de datos:\n {error}")

# Generar autenticacion
class Auth:
    @staticmethod
    def register(db: Database, username: str, password: str):
        salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        usuario = {
            "id": 1,
            "username": username,
            "password": hashed_password
        }

        db.query(
            "INSERT INTO USERS (id, username, password) VALUES (:id, :username, :password)",
            usuario
        )
    @staticmethod
    def login(db: Database, username: str, password: str) -> bool:
        resultado = db.query(
            "SELECT * FROM USERS WHERE username = :username",
            {"username" : username}
        ) 

        for usuario in resultado:
            password_user = usuario[2]
            return bcrypt.checkpw(password.encode('utf-8'), password_user)
        


"""
Unidad de Fomento (UF)
Indice de Valor Promedio (IVP)
Indice de Precios al Consumidor (IPC)
Unidad Tributaria Mensual (UTM)
Dólar -> CLP
EURO -> CLP
"""

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
    def get_indicator(self, indicator: str = None, fecha:str = None):
        if not indicator:
            return print("Indicador faltante")
        if not fecha:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            fecha = f"{day}-{month}-{year}"
        url = f"{self.base_url}/{indicator}/{fecha}"
        data = requests.get(url=url).json()
        print(data['serie'][0]['valor'])
    def get_uf(self, fecha: str = None):
        self.get_indicator("uf", fecha)
    def get_ivp(self, fecha: str = None):
        self.get_indicator("ivp", fecha)
    def get_ipc(self, fecha: str = None):
        self.get_indicator("ipc", fecha)
    def get_utm(self, fecha: str = None):
        self.get_indicator("utm", fecha)
    def get_usd(self, fecha: str = None):
        self.get_indicator("dolar", fecha)
    def get_eur(self, fecha: str = None):
        self.get_indicator("euro", fecha)

if __name__ == "__main__":
    indicadores = Finance()
    indicadores.get_uf()
    indicadores.get_ivp()
    indicadores.get_ipc()
    indicadores.get_utm()
    indicadores.get_usd()
    indicadores.get_eur()