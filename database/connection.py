"""
Modulo de conexao com o banco de dados SQL Server.
Gerencia a conexao, execucao de queries e criacao automatica de tabelas.
"""

import os
import pyodbc
from dotenv import load_dotenv


class DatabaseConnection:
    """
    Classe para gerenciar a conexao com o banco de dados SQL Server.
    
    Atributos:
        conn: Objeto de conexao pyodbc
        cursor: Cursor para execucao de queries
    """
    
    def __init__(self):
        """
        Inicializa a conexao com o banco de dados.
        
        Carrega as variaveis de ambiente e estabelece conexao com o SQL Server.
        Cria as tabelas automaticamente se nao existirem.
        """
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables_if_not_exist()
    
    def _connect(self):
        """
        Estabelece conexao com o banco de dados.
        
        Carrega as configuracoes do arquivo .env e cria a string de conexao.
        """
        load_dotenv()
        
        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_NAME")
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        
        if not all([server, database, username, password]):
            raise ValueError("Configuracoes de banco de dados incompletas no arquivo .env")
        
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
            print("Conexao com banco de dados estabelecida.")
            
        except pyodbc.Error as e:
            print(f"Erro de conexao ODBC: {e}")
            raise
        except Exception as e:
            print(f"Erro na conexao: {e}")
            raise
    
    def _create_tables_if_not_exist(self):
        """
        Cria as tabelas necessarias se nao existirem.
        Adapta-se a estrutura existente sem causar erros.
        """
        try:
            print("Verificando estrutura do banco de dados...")
            
            # Criar tabela Jogadores se nao existir
            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Jogadores' AND xtype='U')
                CREATE TABLE Jogadores (
                    JogadorID INT IDENTITY(1,1) PRIMARY KEY,
                    Nome NVARCHAR(100) NOT NULL,
                    Idade INT NOT NULL,
                    NickName NVARCHAR(50),
                    Palavra_chave NVARCHAR(50) NOT NULL
                )
            """)
            
            # Criar tabela Jogos se nao existir
            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Jogos' AND xtype='U')
                CREATE TABLE Jogos (
                    JogoID INT IDENTITY(1,1) PRIMARY KEY,
                    Nome NVARCHAR(200) NOT NULL,
                    Data_lancamento DATE NOT NULL,
                    Tempo_jogado NVARCHAR(20),
                    Concluido CHAR(3) NOT NULL,
                    Tipo NVARCHAR(50) NOT NULL,
                    JogadorID INT,
                    PlataformaID INT
                )
            """)
            
            # Verificar se tabela Plataformas existe e sua estrutura
            self.cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Plataformas'
            """)
            
            existing_columns = [row[0] for row in self.cursor.fetchall()]
            
            if not existing_columns:
                # Tabela nao existe, criar com estrutura padrao
                self.cursor.execute("""
                    CREATE TABLE Plataformas (
                        PlataformaID INT PRIMARY KEY,
                        Nome NVARCHAR(50) NOT NULL,
                        Descricao NVARCHAR(200)
                    )
                """)
                print("  Tabela Plataformas criada com coluna 'Descricao'")
            else:
                # Tabela existe, verificar se tem coluna Descricao ou Console
                if 'Descricao' in existing_columns:
                    print("  Tabela Plataformas ja existe com coluna 'Descricao'")
                elif 'Console' in existing_columns:
                    print("  Tabela Plataformas existe com coluna 'Console' (estrutura atual)")
                else:
                    print(f"  Tabela Plataformas existe com colunas: {existing_columns}")
            
            # Verificar e inserir plataformas padrao se necessario
            self._check_and_insert_platforms(existing_columns)
            
            self.conn.commit()
            print("Verificacao de estrutura concluida.")
            
            # Verificar e exibir as tabelas
            self.cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """)
            
            tables = self.cursor.fetchall()
            print(f"Tabelas disponiveis: {[table[0] for table in tables]}")
            
        except pyodbc.Error as e:
            print(f"Erro ao verificar estrutura: {e}")
            # Nao faz rollback, apenas informa o erro
            print("Continuando com estrutura existente...")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            print("Continuando com estrutura existente...")

    def _check_and_insert_platforms(self, existing_columns):
        """
        Verifica e insere plataformas padrao adaptando-se a estrutura existente.
        """
        try:
            # Verificar se ja existem plataformas
            self.cursor.execute("SELECT COUNT(*) FROM Plataformas")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                print("Inserindo plataformas padrao...")
                
                # Verificar qual coluna existe
                if 'Console' in existing_columns:
                    # Usar estrutura atual (Console)
                    platforms = [
                        (1, 'Playstation 1', 'Sony'),
                        (2, 'Playstation 2', 'Sony'),
                        (3, 'Playstation 3', 'Sony'),
                        (4, 'Playstation 4', 'Sony'),
                        (5, 'Playstation 5', 'Sony'),
                        (6, 'Xbox 360', 'Microsoft'),
                        (7, 'Xbox One', 'Microsoft'),
                        (8, 'Xbox Series X/S', 'Microsoft'),
                        (9, 'PC', 'Computador')
                    ]
                    
                    for plataforma_id, nome, console in platforms:
                        self.cursor.execute("""
                            INSERT INTO Plataformas (PlataformaID, Nome, Console)
                            VALUES (?, ?, ?)
                        """, (plataforma_id, nome, console))
                    
                    print(f"  {len(platforms)} plataformas inseridas (estrutura Console)")
                    
                elif 'Descricao' in existing_columns:
                    # Usar estrutura padrao (Descricao)
                    platforms = [
                        (1, 'Playstation 1', 'Sony PlayStation 1'),
                        (2, 'Playstation 2', 'Sony PlayStation 2'),
                        (3, 'Playstation 3', 'Sony PlayStation 3'),
                        (4, 'Playstation 4', 'Sony PlayStation 4'),
                        (5, 'Playstation 5', 'Sony PlayStation 5'),
                        (6, 'Xbox 360', 'Microsoft Xbox 360'),
                        (7, 'Xbox One', 'Microsoft Xbox One'),
                        (8, 'Xbox Series X/S', 'Microsoft Xbox Series X/S'),
                        (9, 'PC', 'Computador Pessoal')
                    ]
                    
                    for plataforma_id, nome, descricao in platforms:
                        self.cursor.execute("""
                            INSERT INTO Plataformas (PlataformaID, Nome, Descricao)
                            VALUES (?, ?, ?)
                        """, (plataforma_id, nome, descricao))
                    
                    print(f"  {len(platforms)} plataformas inseridas (estrutura Descricao)")
                else:
                    print("  Estrutura da tabela Plataformas desconhecida, pulando insercao")
                    
            else:
                print(f"  Plataformas ja existem ({count} registros)")
                
        except Exception as e:
            print(f"  Erro ao verificar/inserir plataformas: {e}")
            # Continua mesmo com erro
    
    def execute_query(self, sql, params=None):
        """
        Executa uma query SQL e retorna os resultados.
        
        Args:
            sql: String com o comando SQL
            params: Tupla ou lista com parametros para a query (opcional)
        
        Returns:
            Lista com os resultados da query
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            
            # Verifica se e uma query que retorna resultados
            if sql.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor.rowcount
            
        except pyodbc.Error as e:
            print(f"Erro na execucao da query: {e}")
            self.conn.rollback()
            raise
        except Exception as e:
            print(f"Erro inesperado na query: {e}")
            self.conn.rollback()
            raise
    
    def insert_data(self, table, data_dict):
        """
        Insere dados em uma tabela.
        
        Args:
            table: Nome da tabela
            data_dict: Dicionario com as colunas e valores
        
        Returns:
            ID do registro inserido (se aplicavel)
        """
        if not data_dict:
            raise ValueError("Dicionario de dados vazio")
        
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?' for _ in data_dict])
        values = tuple(data_dict.values())
        
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            
            # Retorna o ID gerado se a tabela tem coluna de identidade
            if 'ID' in [col.upper() for col in data_dict.keys()]:
                self.cursor.execute("SELECT @@IDENTITY")
                return self.cursor.fetchone()[0]
            
            return self.cursor.rowcount
            
        except pyodbc.Error as e:
            print(f"Erro ao inserir dados: {e}")
            self.conn.rollback()
            raise
    
    def delete_data(self, table, condition, params=None):
        """
        Remove dados de uma tabela.
        
        Args:
            table: Nome da tabela
            condition: Condicao WHERE para a remocao
            params: Parametros para a condicao (opcional)
        
        Returns:
            Numero de registros removidos
        """
        sql = f"DELETE FROM {table} WHERE {condition}"
        
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            
            self.conn.commit()
            return self.cursor.rowcount
            
        except pyodbc.Error as e:
            print(f"Erro ao remover dados: {e}")
            self.conn.rollback()
            raise
    
    def get_table_info(self, table_name):
        """
        Obtem informacoes sobre as colunas de uma tabela.
        
        Args:
            table_name: Nome da tabela
        
        Returns:
            Lista de tuplas com informacoes das colunas
        """
        sql = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
        """
        
        try:
            self.cursor.execute(sql, (table_name,))
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Erro ao obter informacoes da tabela: {e}")
            return []
    
    def test_connection(self):
        """
        Testa a conexao com o banco de dados.
        
        Returns:
            True se a conexao estiver funcionando, False caso contrario
        """
        try:
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()
            return result[0] == 1
        except:
            return False
    
    def close(self):
        """
        Fecha a conexao com o banco de dados.
        
        Fecha o cursor e a conexao se estiverem abertos.
        """
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        
        if self.conn:
            self.conn.close()
            self.conn = None
        
        print("Conexao com banco de dados fechada.")
    
    def __enter__(self):
        """
        Metodo para uso em context manager (with statement).
        
        Returns:
            A propria instancia da classe
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Metodo para uso em context manager (with statement).
        
        Garante que a conexao seja fechada ao sair do contexto.
        """
        self.close()
    
    def __del__(self):
        """
        Destrutor da classe.
        
        Garante que a conexao seja fechada quando o objeto for destruido.
        """
        self.close()


# Funcoes auxiliares para uso geral
def create_connection():
    """
    Cria uma nova conexao com o banco de dados.
    
    Returns:
        Instancia de DatabaseConnection
    """
    return DatabaseConnection()


def test_database_connection():
    """
    Testa a conexao com o banco de dados.
    
    Returns:
        True se a conexao for bem-sucedida, False caso contrario
    """
    try:
        db = DatabaseConnection()
        connected = db.test_connection()
        db.close()
        return connected
    except Exception as e:
        print(f"Falha ao testar conexao: {e}")
        return False


def get_database_info():
    """
    Obtem informacoes sobre o banco de dados conectado.
    
    Returns:
        Dicionario com informacoes do banco de dados
    """
    try:
        db = DatabaseConnection()
        
        # Obtem nome do banco
        db.cursor.execute("SELECT DB_NAME()")
        db_name = db.cursor.fetchone()[0]
        
        # Obtem versao do SQL Server
        db.cursor.execute("SELECT @@VERSION")
        version = db.cursor.fetchone()[0]
        
        # Obtem lista de tabelas
        db.cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tables = [row[0] for row in db.cursor.fetchall()]
        
        db.close()
        
        return {
            'database_name': db_name,
            'version': version[:100] + '...' if len(version) > 100 else version,
            'tables': tables,
            'tables_count': len(tables)
        }
        
    except Exception as e:
        print(f"Erro ao obter informacoes do banco: {e}")
        return None


if __name__ == "__main__":
    # Teste basico da conexao
    print("Testando conexao com o banco de dados...")
    
    try:
        if test_database_connection():
            print("Conexao com banco de dados testada com sucesso.")
            
            info = get_database_info()
            if info:
                print(f"\nInformacoes do banco de dados:")
                print(f"  Nome: {info['database_name']}")
                print(f"  Tabelas: {info['tables_count']}")
                print(f"  Lista: {', '.join(info['tables'])}")
        else:
            print("Falha na conexao com o banco de dados.")
            
    except Exception as e:
        print(f"Erro durante teste: {e}")