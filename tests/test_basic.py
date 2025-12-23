
"""
Testes básicos para o sistema de Biblioteca de Jogos
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_project_structure():
    """Testa se a estrutura do projeto está correta"""
    print(" Testando estrutura do projeto...")
    
    # Arquivos obrigatórios
    required_files = [
        ('main.py', 'Arquivo principal'),
        ('requirements.txt', 'Dependências'),
        ('README.md', 'Documentação'),
        ('.env.example', 'Exemplo de configuração'),
    ]
    
    for filename, description in required_files:
        if os.path.exists(filename):
            print(f"   {filename} - {description}")
        else:
            print(f"   {filename} - {description} (NÃO ENCONTRADO)")
            return False
    
    # Pastas obrigatórias
    required_dirs = [
        ('database', 'Conexão com banco'),
        ('models', 'Modelos de dados'),
        ('utils', 'Utilitários'),
        ('api', 'Integração com APIs'),
    ]
    
    for dirname, description in required_dirs:
        if os.path.isdir(dirname):
            # Verifica se tem arquivos Python
            py_files = [f for f in os.listdir(dirname) if f.endswith('.py')]
            print(f"  {dirname}/ - {description} ({len(py_files)} arquivos Python)")
        else:
            print(f"  {dirname}/ - {description} (NÃO ENCONTRADO)")
            return False
    
    return True

def test_basic_imports():
    """Testa se os imports básicos funcionam"""
    print("\n🔍 Testando imports básicos...")
    
    try:
        # Testa import do módulo database
        import database
        print("   Módulo database importado")
    except ImportError as e:
        print(f"   Erro importando database: {e}")
        return False
    
    try:
        # Testa import do módulo models
        import models
        print("   Módulo models importado")
    except ImportError as e:
        print(f"   Erro importando models: {e}")
        return False
    
    try:
        # Testa import do módulo utils
        import utils
        print("   Módulo utils importado")
    except ImportError as e:
        print(f"   Erro importando utils: {e}")
        return False
    
    try:
        # Testa import do módulo api
        import api
        print("   Módulo api importado")
    except ImportError as e:
        print(f"   Erro importando api: {e}")
        return False
    
    return True

def test_class_imports():
    """Testa import das classes principais"""
    print("\n  Testando import de classes...")
    
    classes_to_test = [
        ('database.connection', 'DatabaseConnection'),
        ('models.jogador', 'Jogador'),
        ('models.jogo', 'Jogo'),
        ('utils.display', 'DisplayUtils'),
    ]
    
    all_imported = True
    
    for module_name, class_name in classes_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            if hasattr(module, class_name):
                print(f"   {class_name} importada de {module_name}")
            else:
                print(f"   {class_name} não encontrada em {module_name}")
                all_imported = False
        except ImportError as e:
            print(f"   Erro importando {class_name} de {module_name}: {e}")
            all_imported = False
        except Exception as e:
            print(f"    Erro inesperado com {class_name}: {e}")
            all_imported = False
    
    return all_imported

def test_requirements_file():
    """Verifica se o requirements.txt está correto"""
    print("\n Verificando requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        # Verifica se não está vazio
        if not content.strip():
            print("   requirements.txt está vazio")
            return False
        
        # Conta linhas
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        print(f"   {len(lines)} dependências listadas")
        
        # Verifica dependências essenciais
        essential_packages = ['pyodbc', 'pandas', 'requests']
        missing = []
        
        for package in essential_packages:
            if package in content.lower():
                print(f"   {package} encontrado")
            else:
                print(f"   {package} NÃO encontrado")
                missing.append(package)
        
        if missing:
            print(f"    Faltando: {', '.join(missing)}")
            return False
        
        return True
        
    except FileNotFoundError:
        print("   requirements.txt não encontrado")
        return False
    except Exception as e:
        print(f"   Erro lendo requirements.txt: {e}")
        return False

def test_main_file():
    """Verifica se o arquivo principal existe e tem conteúdo"""
    print("\n Verificando main.py...")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Verifica tamanho mínimo
        if len(content) < 100:
            print("    main.py muito pequeno (menos de 100 caracteres)")
            return False
        
        # Verifica se tem a classe principal
        if 'class BibliotecaJogos' in content:
            print("   Classe BibliotecaJogos encontrada")
        else:
            print("    Classe BibliotecaJogos não encontrada")
        
        # Verifica se tem a execução principal
        if '__name__' in content and '__main__' in content:
            print("   Bloco principal encontrado")
        else:
            print("    Bloco principal não encontrado")
        
        print(f"   Tamanho: {len(content)} caracteres")
        return True
        
    except FileNotFoundError:
        print("   main.py não encontrado")
        return False
    except Exception as e:
        print(f"   Erro lendo main.py: {e}")
        return False

def test_env_example():
    """Verifica se o .env.example tem as variáveis necessárias"""
    print("\n  Verificando .env.example...")
    
    try:
        with open('.env.example', 'r') as f:
            content = f.read()
        
        required_vars = ['DB_SERVER', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'GEMINI_API_KEY']
        missing = []
        
        for var in required_vars:
            if var in content:
                print(f"  {var} definido")
            else:
                print(f"   {var} NÃO definido")
                missing.append(var)
        
        if missing:
            print(f"    Variáveis faltando: {', '.join(missing)}")
            return False
        
        # Verifica se tem comentários/explicações
        if '#' in content:
            print("   Comentários/explicações presentes")
        else:
            print("    Sem comentários/explicações")
        
        return True
        
    except FileNotFoundError:
        print("   .env.example não encontrado")
        return False
    except Exception as e:
        print(f"   Erro lendo .env.example: {e}")
        return False

def test_python_syntax():
    """Testa a sintaxe de todos os arquivos Python"""
    print("\ Testando sintaxe Python...")
    
    import py_compile
    import glob
    
    # Encontra todos os arquivos .py
    python_files = glob.glob('**/*.py', recursive=True)
    
    if not python_files:
        print("    Nenhum arquivo Python encontrado")
        return False
    
    print(f"   Verificando {len(python_files)} arquivo(s) Python...")
    
    errors = []
    
    for py_file in python_files:
        try:
            # Ignora arquivos em __pycache__
            if '__pycache__' in py_file:
                continue
                
            py_compile.compile(py_file, doraise=True)
            print(f"   {py_file} - Sintaxe OK")
        except py_compile.PyCompileError as e:
            print(f"   {py_file} - Erro de sintaxe: {e}")
            errors.append(py_file)
        except Exception as e:
            print(f"    {py_file} - Erro inesperado: {e}")
    
    if errors:
        print(f"   {len(errors)} arquivo(s) com erro de sintaxe")
        return False
    
    print(f"   Todos os {len(python_files)} arquivos Python têm sintaxe válida")
    return True

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print(" EXECUTANDO TESTES - BIBLIOTECA DE JOGOS")
    print("="*60)
    
    # Lista de testes a executar
    tests = [
        ("Estrutura do Projeto", test_project_structure),
        ("Imports Básicos", test_basic_imports),
        ("Imports de Classes", test_class_imports),
        ("Arquivo requirements.txt", test_requirements_file),
        ("Arquivo main.py", test_main_file),
        ("Arquivo .env.example", test_env_example),
        ("Sintaxe Python", test_python_syntax),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n TESTE: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f" {test_name}: PASSOU")
            else:
                print(f" {test_name}: FALHOU")
                
        except Exception as e:
            print(f" {test_name}: ERRO - {e}")
            results.append((test_name, False))
    
    # Resumo final
    print("\n" + "="*60)
    print(" RESULTADO FINAL")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = " PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:30} {status}")
    
    print("\n" + "-"*60)
    print(f" TOTAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n TODOS OS TESTES PASSARAM! Sistema pronto para CI/CD.")
        return 0
    else:
        print(f"\n {total - passed} teste(s) falharam. Corrija antes de continuar.")
        return 1

if __name__ == "__main__":
    sys.exit(main())