import oracledb
import os
import bcrypt
import requests
from dotenv import load_dotenv
from typing import Optional
import datetime

load_dotenv()

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
        print(f"Ejecutando query: \n{sentence}\nParametros: \n{parameters}")
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sentence, parameters)
        except oracledb.DarabaseError as error:
            print(f"Hubo un error en la base de datos:\n {error}")

# Generar autenticacion
class Auth:
    @staticmethod
    def register():
        pass
    @staticmethod
    def login():
        pass

class Finance:
    def __init__(self, base_url):
        self.base_url = base_url
    def get_uf(self, fecha: str = None):
        if not fecha:
            year = datetiime.datetime.now().year()
            month = datetime.datetime.now().month()
            day = datetime.datetime.now().day()
            fecha = f"{day}-{month}-{year}"
        url = f"{self.base_url}/uf/{fecha}"
        data = requests.get(url=url).json()
        print(data)
    def get_ivp():
        pass
    
    def get_ipc():
        pass
    
    def get_utm():
        pass
    
    def get_usd():
        pass
    
    def get_eur():
        pass

if __name__ == "__main__":
    indicadores = Finance()
    indicadores.get_uf()
    #db = Database(username=username, password=password, dsn=dsn)
    #db.query("SELECT ")