
# Modelo para dados do jogador.


# Representa um jogador no sistema.
class Jogador:
    
    
    def __init__(self):
        self.dados = {}
    
    # Coleta dados do jogador.
    def coletar_dados_insercao(self):
       
        print("\n" + "="*50)
        print(" CADASTRO DE JOGADOR")
        print("="*50)
        
        self.dados["Nome"] = input("Nome do jogador: ").strip()
        
        try:
            self.dados["Idade"] = int(input("Idade do jogador: "))
        except ValueError:
            print(" Idade deve ser um número inteiro.")
            return None
        
        self.dados["NickName"] = input("NickName do jogador: ").strip()
        self.dados["Palavra_chave"] = input("Palavra chave: ").strip()
        
        return tuple(self.dados.values())
    
    # Coleta ID do jogador para remoção.
    def coletar_id_remocao(self):
    
        try:
            return int(input("Informe o número ID do jogador: "))
        except ValueError:
            print(" ID deve ser um número inteiro.")
            return None
    
    # Retorna as colunas da tabela Jogadores.
    @staticmethod
    def get_columns():
        
        return ["Nome", "Idade", "NickName", "Palavra_chave"]