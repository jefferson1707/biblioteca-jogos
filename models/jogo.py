
# Modelo para dados do jogo.


# Representa um jogo no sistema.
class Jogo:
    
    
    PLATAFORMAS = {
        1: "Playstation 1",
        2: "Playstation 2",
        3: "Playstation 3",
        4: "Playstation 4",
        5: "Playstation 5",
        6: "Xbox 360",
        7: "Xbox One",
        8: "Xbox Series X/S",
        9: "PC"
    }
    
    def __init__(self):
        self.dados = {}
    
    # Exibe a lista de plataformas disponíveis.
    def mostrar_plataformas(self):
        
        print("\n🎮 PLATAFORMAS DISPONÍVEIS:")
        for key, value in self.PLATAFORMAS.items():
            print(f"   {key}. {value}")
    
    # Coleta dados do jogo via input do usuário.
    def coletar_dados_insercao(self, jogador_id):
        
        print("\n" + "="*50)
        print(" CADASTRO DE JOGO")
        print("="*50)
        
        self.dados["Nome"] = input("Nome do jogo: ").strip()
        self.dados["Data_lancamento"] = input("Data de lançamento (AAAA-MM-DD): ").strip()
        self.dados["Tempo_jogado"] = input("Tempo jogado (formato 00:00): ").strip()
        self.dados["Concluido"] = input("Concluído (Sim/Não): ").strip()
        self.dados["Tipo"] = input("Tipo (Ação, RPG, etc.): ").strip()
        self.dados["JogadorID"] = jogador_id
        
        self.mostrar_plataformas()
        
        try:
            plataforma_id = int(input("\nNúmero da plataforma: "))
            if plataforma_id not in self.PLATAFORMAS:
                print(" Plataforma inválida.")
                return None
            self.dados["PlataformaID"] = plataforma_id
        except ValueError:
            print(" Plataforma deve ser um número.")
            return None
        
        return tuple(self.dados.values())
    
    # Coleta ID do jogo para remoção.
    def coletar_id_remocao(self):
       
        try:
            return int(input("Informe o número ID do jogo: "))
        except ValueError:
            print(" ID deve ser um número inteiro.")
            return None
    
    # Retorna as colunas da tabela Jogos.
    @staticmethod
    def get_columns():
        
        return [
            "Nome", "Data_lancamento", "Tempo_jogado", 
            "Concluido", "Tipo", "JogadorID", "PlataformaID"
        ]