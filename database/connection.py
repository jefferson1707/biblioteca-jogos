
# Módulo de conexão com o banco de dados.


import os
import pyodbc
from dotenv import load_dotenv

 # Gerencia a conexão com o banco de dados
class DatabaseConnection:
    
    # Inicializa a conexão com o banco de dados
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._connect()
    
    # Estabelece conexão com o banco de dados
    def _connect(self):
        load_dotenv()
        
        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_NAME")
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        
        try:
            connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
            
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()
            print(" Conexão com banco de dados estabelecida.")
            
        except Exception as e:
            print(f" Erro na conexão: {e}")
            raise
    
    # Fecha a conexão com o banco de dados
    def close(self):
       
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print(" Conexão com banco de dados fechada.")
    
    # Gera um contexto para a conexão com o banco de dados
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()