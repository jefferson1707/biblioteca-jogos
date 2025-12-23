
# Funções para operações no banco de dados.


from .connection import DatabaseConnection

# Classe de funções
class DatabaseFunctions:
    
    # Construtor
    def __init__(self, db_connection=None):
        self.db = db_connection or DatabaseConnection()
    
    #  Executa uma consulta SELECT.
    def query(self, sql, params=None):
        
        try:
            if params:
                self.db.cursor.execute(sql, params)
            else:
                self.db.cursor.execute(sql)
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f" Erro na consulta: {e}")
            return None
    
    # Insere dados no banco de dados
    def insert(self, sql, values):
        
        try:
            self.db.cursor.execute(sql, values)
            self.db.cursor.commit()
            print(" Dados inseridos com sucesso.")
            return True
        except Exception as e:
            print(f" Erro ao inserir dados: {e}")
            return False
    
    # Remove dados do banco de dados
    def delete(self, sql, params=None):
        
        try:
            if params:
                self.db.cursor.execute(sql, params)
            else:
                self.db.cursor.execute(sql)
            self.db.cursor.commit()
            print(" Dados removidos com sucesso.")
            return True
        except Exception as e:
            print(f" Erro na remoção: {e}")
            return False
    
    # Fecha a conexão com o banco de dados
    def close(self):
        self.db.close()