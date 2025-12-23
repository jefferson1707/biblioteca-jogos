
# Utilitários para exibição de dados.


import pandas as pd

# Utilitários para formatação e exibição de dados.
class DisplayUtils:
    
    # Exibe dados de consulta em formato tabular.
    @staticmethod
    def mostrar_resultado_consulta(dados, tipo):
        
        if not dados:
            print(" Nenhum dado encontrado.")
            return
        
        try:
            df = pd.DataFrame.from_records(dados)
            
            if tipo == "Jogadores":
                DisplayUtils._mostrar_jogadores(df)
            elif tipo == "Jogos":
                DisplayUtils._mostrar_jogos(df)
            else:
                DisplayUtils._mostrar_generico(df, tipo)
                
        except Exception as e:
            print(f" Erro ao processar dados: {e}")
    
    # Exibe dados de jogadores.
    @staticmethod
    def _mostrar_jogadores(df):
       
        if len(df.columns) == 5:
            df.columns = ["ID", "Nome", "Idade", "NickName", "Palavra_chave"]
            DisplayUtils._imprimir_tabela(df, " RELATÓRIO DE JOGADORES")
        else:
            DisplayUtils._imprimir_lista_simples(df, "Jogadores")
    
    # Exibe dados de jogos.
    @staticmethod
    def _mostrar_jogos(df):
        
        if len(df.columns) == 8:
            df.columns = [
                "ID", "Nome", "Lançamento", "Tempo jogado", 
                "Concluído", "Tipo", "JogadorID", "Plataforma"
            ]
            DisplayUtils._imprimir_tabela(df, " RELATÓRIO DE JOGOS")
        else:
            DisplayUtils._imprimir_lista_simples(df, "Jogos")
    
    # Imprime DataFrame como tabela formatada.
    @staticmethod
    def _imprimir_tabela(df, titulo):
       
        print("\n" + "═" * 100)
        print(titulo.center(100))
        print("═" * 100)
        print(df.to_string(index=False))
        print("═" * 100)
        print(f"Total de registros: {len(df)}")
        print("═" * 100)
    
    # Imprime lista simples de resultados.
    @staticmethod
    def _imprimir_lista_simples(df, tipo):
     
        print(f"\n RESULTADO DA CONSULTA - {tipo.upper()}")
        print("─" * 50)
        for i, row in df.iterrows():
            print(f"{i+1:3}. {row[0]}")
        print("─" * 50)
        print(f"Total: {len(df)} itens")