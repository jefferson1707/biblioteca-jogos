
"""
Script de configuração automática do banco de dados
Para novos usuários do sistema Biblioteca de Jogos
"""

import os
import sys
import pyodbc
from dotenv import load_dotenv

# Estabelece conexão com o SQL Server
def get_database_connection(server=None, database=None, username=None, password=None):
   
    load_dotenv()
    
    # Usa valores fornecidos ou do .env
    server = server or os.getenv("DB_SERVER")
    database = database or os.getenv("DB_NAME") or "master"  # Usa 'master' para criar o banco
    username = username or os.getenv("DB_USER")
    password = password or os.getenv("DB_PASSWORD")
    
    if not all([server, username, password]):
        print(" Configuração do banco de dados incompleta.")
        print("   Configure o arquivo .env ou forneça os parâmetros.")
        return None
    
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )
        
        conn = pyodbc.connect(connection_string)
        print(f" Conexão estabelecida com {server}/{database}")
        return conn
        
    except Exception as e:
        print(f" Erro na conexão: {e}")
        return None

# Cria o banco de dados se nao existir.
def create_database(conn, db_name):
  
    try:
        cursor = conn.cursor()
        
        # Verifica se o banco já existe
        cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{db_name}'")
        if cursor.fetchone():
            print(f" Banco de dados '{db_name}' já existe.")
            return True
        
        # Cria o banco de dados
        cursor.execute(f"CREATE DATABASE {db_name}")
        conn.commit()
        print(f" Banco de dados '{db_name}' criado com sucesso!")
        return True
        
    except Exception as e:
        print(f" Erro ao criar banco de dados: {e}")
        return False

# Cria as tabelas no banco.
def create_tables(conn, db_name):
   
    try:
        # Muda para o banco de dados correto
        conn.cursor().execute(f"USE {db_name}")
        
        sql_commands = [
            # Tabela Jogadores
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Jogadores' AND xtype='U')
            CREATE TABLE Jogadores (
                JogadorID INT IDENTITY(1,1) PRIMARY KEY,
                Nome NVARCHAR(100) NOT NULL,
                Idade INT NOT NULL,
                NickName NVARCHAR(50) NOT NULL,
                Palavra_chave NVARCHAR(50) NOT NULL,
                Data_cadastro DATETIME DEFAULT GETDATE()
            )
            """,
            
            # Tabela Jogos
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Jogos' AND xtype='U')
            CREATE TABLE Jogos (
                JogoID INT IDENTITY(1,1) PRIMARY KEY,
                Nome NVARCHAR(200) NOT NULL,
                Data_lancamento DATE,
                Tempo_jogado TIME,
                Concluido NVARCHAR(3) DEFAULT 'Nao',
                Tipo NVARCHAR(50),
                JogadorID INT NOT NULL,
                PlataformaID INT NOT NULL,
                Data_cadastro DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (JogadorID) REFERENCES Jogadores(JogadorID) ON DELETE CASCADE
            )
            """,
            
            # Tabela Plataformas (para referência)
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Plataformas' AND xtype='U')
            CREATE TABLE Plataformas (
                PlataformaID INT PRIMARY KEY,
                Nome NVARCHAR(50) NOT NULL,
                Descricao NVARCHAR(200)
            )
            """,
            
            # Inserir dados de plataformas
            """
            IF NOT EXISTS (SELECT * FROM Plataformas WHERE PlataformaID = 1)
            INSERT INTO Plataformas (PlataformaID, Nome, Descricao) VALUES
            (1, 'Playstation 1', 'Sony PlayStation 1'),
            (2, 'Playstation 2', 'Sony PlayStation 2'),
            (3, 'Playstation 3', 'Sony PlayStation 3'),
            (4, 'Playstation 4', 'Sony PlayStation 4'),
            (5, 'Playstation 5', 'Sony PlayStation 5'),
            (6, 'Xbox 360', 'Microsoft Xbox 360'),
            (7, 'Xbox One', 'Microsoft Xbox One'),
            (8, 'Xbox Series X/S', 'Microsoft Xbox Series X/S'),
            (9, 'PC', 'Computador Pessoal'),
            (10, 'Nintendo Switch', 'Nintendo Switch'),
            (11, 'Nintendo Wii', 'Nintendo Wii'),
            (12, 'Mobile', 'Dispositivos Móveis')
            """
        ]
        
        cursor = conn.cursor()
        print("Criando tabelas...")
        
        for i, sql in enumerate(sql_commands, 1):
            try:
                cursor.execute(sql)
                if i <= 3:  # Apenas para as criações de tabela
                    table_names = ['Jogadores', 'Jogos', 'Plataformas']
                    print(f"   Tabela '{table_names[i-1]}' verificada/criada")
            except Exception as e:
                print(f"    Erro no comando {i}: {e}")
        
        conn.commit()
        
        # Verificar tabelas criadas
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tables = cursor.fetchall()
        print(f"\n Tabelas no banco '{db_name}':")
        for table in tables:
            print(f"  • {table[0]}")
        
        return True
        
    except Exception as e:
        print(f" Erro ao criar tabelas: {e}")
        return False

# Insere dados de exemplo (opcionais).
def create_sample_data(conn):
    
    try:
        cursor = conn.cursor()
        
        # Verifica se já existem jogadores
        cursor.execute("SELECT COUNT(*) FROM Jogadores")
        if cursor.fetchone()[0] > 0:
            print(" Dados de exemplo já existem.")
            return True
        
        print("Inserindo dados de exemplo...")
        
        # Insere jogadores de exemplo
        cursor.execute("""
            INSERT INTO Jogadores (Nome, Idade, NickName, Palavra_chave) 
            VALUES 
            ('João Silva', 25, 'JoaoGamer', 'senha123'),
            ('Maria Santos', 30, 'MariPlay', 'abc456'),
            ('Carlos Oliveira', 22, 'CarlosGame', 'xyz789')
        """)
        
        # Insere jogos de exemplo
        cursor.execute("""
            INSERT INTO Jogos (Nome, Data_lancamento, Tempo_jogado, Concluido, Tipo, JogadorID, PlataformaID) 
            VALUES 
            ('The Witcher 3: Wild Hunt', '2015-05-19', '105:30:00', 'Sim', 'RPG', 1, 9),
            ('God of War', '2018-04-20', '45:15:00', 'Nao', 'Ação-Aventura', 2, 4),
            ('Red Dead Redemption 2', '2018-10-26', '80:20:00', 'Sim', 'Ação-Aventura', 1, 9),
            ('The Legend of Zelda: Breath of the Wild', '2017-03-03', '65:45:00', 'Sim', 'Ação-Aventura', 3, 10),
            ('Cyberpunk 2077', '2020-12-10', '50:10:00', 'Nao', 'RPG', 2, 9)
        """)
        
        conn.commit()
        print(" Dados de exemplo inseridos com sucesso!")
        return True
        
    except Exception as e:
        print(f"  Erro ao inserir dados de exemplo: {e}")
        return False

# Verifica se pyodbc está instalado
def check_requirements():
    
    try:
        import pyodbc
        return True
    except ImportError:
        print(" pyodbc não está instalado.")
        print("   Instale com: pip install pyodbc")
        return False

# Configuração interativa.
def interactive_setup():
    
    print("\n" + "="*60)
    print("CONFIGURAÇÃO DO BANCO DE DADOS - Biblioteca de Jogos")
    print("="*60)
    
    # Verificar pyodbc
    if not check_requirements():
        return False
    
    # Verificar .env
    if not os.path.exists(".env"):
        print("\n  Arquivo .env não encontrado.")
        create_env = input("Deseja criar o arquivo .env agora? (s/n): ").lower()
        
        if create_env == 's':
            create_env_file()
        else:
            print(" Configure o arquivo .env primeiro.")
            return False
    
    # Perguntar ao usuário
    print("\nOpções de configuração:")
    print("1. Configuração automática (usa .env)")
    print("2. Configuração manual")
    print("3. Apenas verificar estrutura atual")
    
    choice = input("\nEscolha uma opção (1-3): ").strip()
    
    if choice == "1":
        return automatic_setup()
    elif choice == "2":
        return manual_setup()
    elif choice == "3":
        return check_current_structure()
    else:
        print(" Opção inválida.")
        return False

# Cria o arquivo .env de exemplo.
def create_env_file():
    
    env_content = """# Configurações do Banco de Dados SQL Server
DB_SERVER=localhost\\SQLEXPRESS
DB_NAME=Biblioteca_jogos
DB_USER=sa
DB_PASSWORD=sua_senha_aqui

# API Google Gemini AI (opcional para funcionalidades de IA)
GEMINI_API_KEY=sua_chave_gemini_aqui

# Configurações gerais
DEBUG=False
TIMEZONE=America/Sao_Paulo
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print(" Arquivo .env criado.")
    print("  Edite o arquivo .env com suas credenciais reais!")
    return True

# Configuração automática usando .env
def automatic_setup():
    
    load_dotenv()
    
    db_name = os.getenv("DB_NAME", "Biblioteca_jogos")
    server = os.getenv("DB_SERVER")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    
    if not all([server, username, password]):
        print(" Configuração incompleta no .env")
        return False
    
    print(f"\n Configurando banco de dados '{db_name}'...")
    
    # Etapa 1: Conectar ao master e criar o banco
    conn = get_database_connection(server, "master", username, password)
    if not conn:
        return False
    
    if not create_database(conn, db_name):
        conn.close()
        return False
    
    conn.close()
    
    # Etapa 2: Conectar ao novo banco e criar tabelas
    conn = get_database_connection(server, db_name, username, password)
    if not conn:
        return False
    
    success = create_tables(conn, db_name)
    
    if success:
        # Perguntar se quer dados de exemplo
        add_samples = input("\nDeseja adicionar dados de exemplo? (s/n): ").lower()
        if add_samples == 's':
            create_sample_data(conn)
    
    conn.close()
    
    if success:
        print("\n" + "="*60)
        print(" CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print(f"Banco: {db_name}")
        print(f"Servidor: {server}")
        print(f"Tabelas criadas: Jogadores, Jogos, Plataformas")
        print("\nExecute o sistema com: python main.py")
    
    return success

# Configuração manual.
def manual_setup():
    
    print("\n Configuração Manual do Banco de Dados")
    print("-" * 40)
    
    server = input("Servidor SQL (ex: localhost\\SQLEXPRESS): ").strip()
    username = input("Usuário (ex: sa): ").strip()
    password = input("Senha: ").strip()
    db_name = input("Nome do banco (padrão: Biblioteca_jogos): ").strip() or "Biblioteca_jogos"
    
    print(f"\n Configurando banco de dados '{db_name}'...")
    
    # Etapa 1: Conectar ao master e criar o banco
    conn = get_database_connection(server, "master", username, password)
    if not conn:
        return False
    
    if not create_database(conn, db_name):
        conn.close()
        return False
    
    conn.close()
    
    # Etapa 2: Conectar ao novo banco e criar tabelas
    conn = get_database_connection(server, db_name, username, password)
    if not conn:
        return False
    
    success = create_tables(conn, db_name)
    
    if success:
        # Perguntar se quer dados de exemplo
        add_samples = input("\nDeseja adicionar dados de exemplo? (s/n): ").lower()
        if add_samples == 's':
            create_sample_data(conn)
    
    conn.close()
    
    if success:
        # Salvar no .env
        save_to_env = input("\nDeseja salvar estas configurações no .env? (s/n): ").lower()
        if save_to_env == 's':
            with open(".env", "w") as f:
                f.write(f"DB_SERVER={server}\n")
                f.write(f"DB_NAME={db_name}\n")
                f.write(f"DB_USER={username}\n")
                f.write(f"DB_PASSWORD={password}\n")
                f.write("GEMINI_API_KEY=sua_chave_gemini_aqui\n")
                f.write("DEBUG=False\n")
                f.write("TIMEZONE=America/Sao_Paulo\n")
            print(" Configurações salvas no .env")
        
        print("\n" + "="*60)
        print(" CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print(f"Banco: {db_name}")
        print(f"Servidor: {server}")
        print(f"Tabelas criadas: Jogadores, Jogos, Plataformas")
        print("\nExecute o sistema com: python main.py")
    
    return success

# Verificar estrutura atual do banco.
def check_current_structure():
    
    load_dotenv()
    
    db_name = os.getenv("DB_NAME", "Biblioteca_jogos")
    conn = get_database_connection(None, db_name, None, None)
    
    if not conn:
        print(" Não foi possível conectar ao banco de dados.")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tables = cursor.fetchall()
        
        print(f"\n ESTRUTURA ATUAL DO BANCO '{db_name}':")
        print("-" * 40)
        
        if tables:
            print("Tabelas encontradas:")
            for table in tables:
                print(f"  • {table[0]}")
                
                # Mostrar colunas de cada tabela
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = '{table[0]}'
                    ORDER BY ORDINAL_POSITION
                """)
                
                columns = cursor.fetchall()
                for col in columns:
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    print(f"    - {col[0]} ({col[1]}) {nullable}")
                print()
        else:
            print(" Nenhuma tabela encontrada.")
            print("   Execute o setup para criar as tabelas.")
        
        # Contar registros
        if tables:
            print(" ESTATÍSTICAS:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"  {table[0]}: {count} registro(s)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f" Erro ao verificar estrutura: {e}")
        return False

# Função principal.
def main():
    
    print("\n SETUP - Biblioteca de Jogos ")
    
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1:
        if sys.argv[1] == "--auto":
            return automatic_setup()
        elif sys.argv[1] == "--check":
            return check_current_structure()
        elif sys.argv[1] == "--help":
            print("\nUso: python setup_database.py [opção]")
            print("\nOpções:")
            print("  --auto     Configuração automática (usa .env)")
            print("  --check    Verifica estrutura atual")
            print("  --help     Mostra esta ajuda")
            print("\nSem argumentos: Modo interativo")
            return True
    
    # Modo interativo padrão
    return interactive_setup()

if __name__ == "__main__":
    success = main()
    if success:
        sys.exit(0)
    else:
        print("\n Configuração falhou.")
        print("   Verifique suas credenciais e tente novamente.")
        sys.exit(1)
