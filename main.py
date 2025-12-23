# Sistema de Biblioteca de Jogos - Programa Principal


from database.functions import DatabaseFunctions
from database.scripts import SQLScripts
from models.jogador import Jogador
from models.jogo import Jogo
from utils.display import DisplayUtils
from utils.gemini_utils import GeminiDisplay
from api.gemini_client import GeminiClient, GeminiCache


# Classe principal do sistema.
class BibliotecaJogos:
    
    def __init__(self):
        self.db = DatabaseFunctions()
        self.jogador = Jogador()
        self.jogo = Jogo()
        self.usuario_id = None
        self.senha = None
        self.gemini_client = None
        self.gemini_cache = GeminiCache()
        self._initialize_gemini()
    
    # Inicializa o cliente Gemini AI.
    def _initialize_gemini(self):
        try:
            self.gemini_client = GeminiClient()
            if self.gemini_client.test_connection():
                print("Conexao com Gemini AI estabelecida.")
            else:
                print("Gemini AI disponivel em modo limitado.")
        except Exception as e:
            print(f"Gemini AI nao disponivel: {e}")
            self.gemini_client = None
    
    # Valida o acesso do usuario ao sistema.
    def _validar_usuario(self):
        
        print("\n" + "="*60)
        print(" ACESSO AO SISTEMA")
        print("="*60)
        
        possui_usuario = input("Ja possui um usuario? (sim/nao): ").lower()
        
        if possui_usuario == "nao":
            return self._criar_primeiro_usuario()
        elif possui_usuario == "sim":
            return self._realizar_login()
        else:
            print(" Resposta invalida. Use 'sim' ou 'nao'.")
            return False
    
    # Cria o primeiro usuario do sistema.
    def _criar_primeiro_usuario(self):
        
        print("\n Vamos criar seu primeiro usuario para acesso ao sistema.")
        
        dados = self.jogador.coletar_dados_insercao()
        if not dados:
            return False
        
        sql = SQLScripts.insert("Jogadores", Jogador.get_columns())
        
        if self.db.insert(sql, dados):
            print(" Usuario criado com sucesso! Faca login para continuar.")
            return self._realizar_login()
        return False
    
    # Realiza o login do usuario.
    def _realizar_login(self):
        
        self.senha = input("\n Informe sua palavra-chave: ").strip()
        
        try:
            self.usuario_id = int(input(" Informe seu ID de jogador: "))
        except ValueError:
            print(" ID deve ser um numero.")
            return False
        
        # Verificar credenciais
        sql = SQLScripts.select_player_by_password()
        resultado = self.db.query(sql, (self.senha,))
        
        if resultado and any(self.usuario_id == row[0] for row in resultado):
            print(" Login realizado com sucesso!")
            return True
        else:
            print(" ID ou senha incorretos.")
            return False
    
    # Menu de consulta de dados.
    def _consultar_dados(self):
        
        print("\n" + "="*50)
        print(" MENU DE CONSULTA")
        print("="*50)
        
        print("1. Jogadores")
        print("2. Jogos")
        print("3. Informacoes detalhadas sobre um jogo (Gemini AI)")
        print("4. Comparar jogos")
        
        try:
            opcao_tabela = int(input("\nEscolha o que deseja consultar (1-4): "))
            
            if opcao_tabela == 1:
                self._consultar_jogadores()
            elif opcao_tabela == 2:
                self._consultar_jogos()
            elif opcao_tabela == 3:
                self._consultar_info_gemini()
            elif opcao_tabela == 4:
                self._comparar_jogos()
            else:
                print(" Opcao invalida.")
                
        except ValueError:
            print(" Digite um numero valido.")
    
    # Consulta dados de jogadores.
    def _consultar_jogadores(self):
        
        print("\n Opcoes de consulta para Jogadores:")
        print("1. Todos os dados")
        print("2. Apenas nomes")
        
        try:
            opcao = int(input("Escolha (1-2): "))
            
            if opcao == 1:
                sql = SQLScripts.select("Jogadores", "*", "Palavra_chave = ?")
                dados = self.db.query(sql, (self.senha,))
            elif opcao == 2:
                sql = SQLScripts.select("Jogadores", ["Nome"], "Palavra_chave = ?")
                dados = self.db.query(sql, (self.senha,))
            else:
                print(" Opcao invalida.")
                return
            
            DisplayUtils.mostrar_resultado_consulta(dados, "Jogadores")
            
        except ValueError:
            print(" Digite um numero valido.")
    
    # Consulta dados de jogos.
    def _consultar_jogos(self):
        
        print("\n Opcoes de consulta para Jogos:")
        print("1. Todos os dados")
        print("2. Apenas nomes")
        
        try:
            opcao = int(input("Escolha (1-2): "))
            
            if opcao == 1:
                sql = SQLScripts.select("Jogos", "*", "JogadorID = ?")
            elif opcao == 2:
                sql = SQLScripts.select("Jogos", ["Nome"], "JogadorID = ?")
            else:
                print(" Opcao invalida.")
                return
            
            dados = self.db.query(sql, (self.usuario_id,))
            DisplayUtils.mostrar_resultado_consulta(dados, "Jogos")
            
        except ValueError:
            print(" Digite um numero valido.")
    
    # Consulta informacoes detalhadas sobre um jogo usando Gemini AI.
    def _consultar_info_gemini(self):
        
        if not self.gemini_client:
            print(" Servico Gemini AI nao esta disponivel no momento.")
            return
        
        print("\n" + "*" * 50)
        print(" CONSULTA GEMINI AI - INFORMACOES DETALHADAS")
        print("*" * 50)
        
        # Opcao 1: Consultar jogo especifico
        print("\n1. Consultar informacoes de um jogo especifico")
        print("2. Consultar informacoes de todos os seus jogos")
        
        try:
            opcao = int(input("\nEscolha (1-2): "))
            
            if opcao == 1:
                nome_jogo = input(" Digite o nome do jogo: ").strip()
                if nome_jogo:
                    self._get_game_info_gemini(nome_jogo)
                else:
                    print(" Nome do jogo nao pode ser vazio.")
            
            elif opcao == 2:
                self._get_all_games_info_gemini()
            
            else:
                print(" Opcao invalida.")
                
        except ValueError:
            print(" Digite um numero valido.")
    
    # Obtem informacoes de um jogo especifico usando Gemini AI.
    def _get_game_info_gemini(self, game_name, platform=None):
        
        print(f"\n Buscando informacoes sobre '{game_name}'...")
        
        # Verificar cache primeiro
        cached_info = self.gemini_cache.get(game_name, platform)
        if cached_info:
            print(" Usando informacoes em cache...")
            GeminiDisplay.display_game_info(cached_info)
            return cached_info
        
        # Consultar API
        if self.gemini_client:
            print(" Consultando Gemini AI...")
            game_info = self.gemini_client.get_game_info(game_name, platform)
            
            # Salvar no cache
            self.gemini_cache.set(game_name, platform, game_info)
            
            GeminiDisplay.display_game_info(game_info)
            
            # Mostrar recomendacao
            recomendacao = GeminiDisplay.get_recommendation_based_on_game(game_info)
            print(f"\n {recomendacao}")
            
            return game_info
        
        return None
    
    # Obtem informacoes de todos os jogos do usuario.
    def _get_all_games_info_gemini(self):
        
        # Primeiro, obter lista de jogos do banco
        sql = SQLScripts.select("Jogos", ["Nome", "PlataformaID"], "JogadorID = ?")
        jogos = self.db.query(sql, (self.usuario_id,))
        
        if not jogos:
            print(" Voce nao tem jogos cadastrados.")
            return
        
        print(f"\n Voce tem {len(jogos)} jogo(s) cadastrado(s):")
        
        all_games_info = []
        for i, (nome_jogo, plataforma_id) in enumerate(jogos, 1):
            print(f"\n[{i}/{len(jogos)}] Consultando '{nome_jogo}'...")
            
            # Mapear ID da plataforma para nome (se disponivel)
            plataforma = self._get_platform_name(plataforma_id)
            
            # Obter informacoes
            game_info = self._get_game_info_gemini(nome_jogo, plataforma)
            if game_info:
                all_games_info.append(game_info)
        
        # Oferecer comparacao se houver multiplos jogos
        if len(all_games_info) > 1:
            comparar = input("\n Deseja ver uma comparacao entre seus jogos? (sim/nao): ").lower()
            if comparar == "sim":
                GeminiDisplay.create_comparison_table(all_games_info)
    
    # Converte ID da plataforma para nome.
    def _get_platform_name(self, platform_id):
        
        plataformas = {
            1: "Playstation 1", 2: "Playstation 2", 3: "Playstation 3",
            4: "Playstation 4", 5: "Playstation 5", 6: "Xbox 360",
            7: "Xbox One", 8: "Xbox Series X/S", 9: "PC"
        }
        return plataformas.get(platform_id, "Desconhecida")
    
    # Compara informacoes de multiplos jogos.
    def _comparar_jogos(self):
        
        print("\n" + "*" * 50)
        print(" COMPARACAO DE JOGOS")
        print("*" * 50)
        
        # Obter jogos do usuario
        sql = SQLScripts.select("Jogos", ["Nome"], "JogadorID = ?")
        jogos = self.db.query(sql, (self.usuario_id,))
        
        if not jogos:
            print(" Voce nao tem jogos cadastrados para comparar.")
            return
        
        print("\n Seus jogos cadastrados:")
        for i, (nome_jogo,) in enumerate(jogos, 1):
            print(f"{i}. {nome_jogo}")
        
        print(f"\n a. Comparar todos os jogos")
        
        try:
            escolhas = input("\n Digite os numeros dos jogos para comparar (separados por virgula): ").strip()
            
            if escolhas.lower() == 'a':
                # Comparar todos
                self._get_all_games_info_gemini()
                return
            
            indices = [int(x.strip()) for x in escolhas.split(',') if x.strip().isdigit()]
            indices = [i for i in indices if 1 <= i <= len(jogos)]
            
            if len(indices) < 2:
                print(" Selecione pelo menos 2 jogos para comparar.")
                return
            
            jogos_selecionados = [jogos[i-1][0] for i in indices]
            
            print(f"\n Comparando {len(jogos_selecionados)} jogos...")
            
            games_info = []
            for nome_jogo in jogos_selecionados:
                game_info = self._get_game_info_gemini(nome_jogo)
                if game_info:
                    games_info.append(game_info)
            
            if len(games_info) >= 2:
                GeminiDisplay.create_comparison_table(games_info)
            else:
                print(" Nao ha informacoes suficientes para comparar.")
                
        except ValueError:
            print(" Entrada invalida.")
    
    # Cadastra um novo jogo.
    def _cadastrar_jogo(self):
        
        dados = self.jogo.coletar_dados_insercao(self.usuario_id)
        if not dados:
            return
        
        sql = SQLScripts.insert("Jogos", Jogo.get_columns())
        self.db.insert(sql, dados)
    
    # Menu de remocao de dados.
    def _remover_dados(self):
        
        print("\n" + "="*50)
        print(" MENU DE REMOCAO")
        print("="*50)
        
        print("1. Remover jogador")
        print("2. Remover jogo")
        print("3. Limpar cache do Gemini AI")
        
        try:
            opcao = int(input("\n Escolha o que deseja (1-3): "))
            
            if opcao == 1:
                return self._remover_jogador()
            elif opcao == 2:
                self._remover_jogo()
            elif opcao == 3:
                self._limpar_cache_gemini()
            else:
                print(" Opcao invalida.")
                
        except ValueError:
            print(" Digite um numero valido.")
        
        return False
    
    # Remove um jogador do sistema.
    def _remover_jogador(self):
        
        jogador_id = self.jogador.coletar_id_remocao()
        
        if jogador_id and jogador_id == self.usuario_id:
            confirmacao = input(f" Tem certeza que deseja remover o jogador ID {jogador_id}? (sim/nao): ").lower()
            
            if confirmacao == "sim":
                sql = SQLScripts.delete("Jogadores", f"JogadorID = {jogador_id}")
                if self.db.delete(sql):
                    print(" Jogador removido. Encerrando sessao...")
                    return True  # Indica que o programa deve encerrar
        else:
            print(" Voce so pode remover seu proprio usuario.")
        
        return False
    
    # Remove um jogo do sistema.
    def _remover_jogo(self):
        
        jogo_id = self.jogo.coletar_id_remocao()
        
        if jogo_id:
            confirmacao = input(f" Tem certeza que deseja remover o jogo ID {jogo_id}? (sim/nao): ").lower()
            
            if confirmacao == "sim":
                sql = SQLScripts.delete("Jogos", f"JogoID = {jogo_id} AND JogadorID = {self.usuario_id}")
                self.db.delete(sql)
    
    # Limpa o cache do Gemini AI.
    def _limpar_cache_gemini(self):
        
        confirmacao = input(" Tem certeza que deseja limpar o cache do Gemini AI? (sim/nao): ").lower()
        if confirmacao == "sim":
            self.gemini_cache.clear()
            print(" Cache do Gemini AI limpo.")
    
    # Exibe informacoes sobre a IA.
    def _mostrar_info_ia(self):
        
        print("\n" + "*" * 60)
        print(" SOBRE A INTELIGENCIA ARTIFICIAL")
        print("*" * 60)
        print("\n Este sistema utiliza o Google Gemini AI para:")
        print("   * Fornecer informacoes detalhadas sobre jogos")
        print("   * Comparar jogos com base em varios criterios")
        print("   * Sugerir recomendacoes personalizadas")
        print("   * Buscar dados atualizados sobre lancamentos")
        
        if self.gemini_client:
            print("\n Status: Gemini AI esta ativo e funcionando.")
        else:
            print("\n Status: Gemini AI esta temporariamente indisponivel.")
            print("   Voce ainda pode usar todas as outras funcionalidades.")
        
        print("\n A IA consulta diversas fontes para fornecer:")
        print("   * Genero e classificacao")
        print("   * Desenvolvedores e publicadores")
        print("   * Pontuacoes em sites especializados")
        print("   * Tempos medios de conclusao")
        print("   * Curiosidades e fatos interessantes")
        
        input("\n Pressione Enter para voltar ao menu...")
    
    # Exibe o menu principal.
    def _mostrar_menu_principal(self):
        
        print("\n" + "="*60)
        print(" BIBLIOTECA DE JOGOS - MENU PRINCIPAL")
        print("="*60)
        print("1. Consultar dados")
        print("2. Cadastrar novo jogo")
        print("3. Remover dados / Gerenciar")
        print("4. Sobre a IA")
        print("5. Sair do sistema")
        print("="*60)
    
    # Metodo principal que executa o sistema.
    def executar(self):
        
        print("\n" + "=" * 30)
        print("BEM-VINDO AO SISTEMA DE BIBLIOTECA DE JOGOS")
        print("=" * 30)
        
        # Validar usuario
        if not self._validar_usuario():
            print(" Nao foi possivel autenticar. Encerrando...")
            return
        
        # Loop principal do programa
        while True:
            self._mostrar_menu_principal()
            
            try:
                opcao = int(input("\n Escolha uma opcao (1-5): "))
                
                if opcao == 1:
                    self._consultar_dados()
                elif opcao == 2:
                    self._cadastrar_jogo()
                elif opcao == 3:
                    if self._remover_dados():  # Se retornar True, significa que usuario foi removido
                        break
                elif opcao == 4:
                    self._mostrar_info_ia()
                elif opcao == 5:
                    print("\n Obrigado por usar a Biblioteca de Jogos!")
                    break
                else:
                    print(" Opcao invalida. Escolha entre 1 e 5.")
                    
            except ValueError:
                print(" Digite um numero valido.")
            except KeyboardInterrupt:
                print("\n\n Programa interrompido pelo usuario.")
                break
        
        # Fechar conexao com o banco
        self.db.close()


if __name__ == "__main__":
    sistema = BibliotecaJogos()
    sistema.executar()