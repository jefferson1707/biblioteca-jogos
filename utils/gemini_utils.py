
# Utilitários para formatação e exibição de informações do Gemini.


from typing import Dict, Any

# Utilitários para formatação e exibição de informações do Gemini
class GeminiDisplay:
   
    # Exibe informações do jogo
    @staticmethod
    def display_game_info(game_info: Dict[str, Any]):
        
        if not game_info:
            print(" Nenhuma informação disponível.")
            return
        
        print("\n" + "=" * 50)
        print(f" INFORMAÇÕES SOBRE: {game_info.get('nome', 'Desconhecido').upper()}")
        print("=" * 50)
        
        # Informações básicas
        print(f"\n DADOS DO JOGO:")
        print(f"    Desenvolvedor: {game_info.get('desenvolvedor', 'N/A')}")
        print(f"    Publicador: {game_info.get('publicador', 'N/A')}")
        print(f"    Ano de lançamento: {game_info.get('ano_lancamento', 'N/A')}")
        print(f"    Gênero: {game_info.get('genero', 'N/A')}")
        
        # Pontuação Metacritic (se disponível)
        metacritic = game_info.get('metacritic_score')
        if metacritic != "N/A" and metacritic is not None:
            score = int(metacritic) if str(metacritic).isdigit() else metacritic
            print(f"    Metacritic: {score}/100")
        
        # Tempo de conclusão
        tempo = game_info.get('tempo_medio_conclusao')
        if tempo != "N/A" and tempo is not None:
            print(f"   Tempo médio: {tempo} horas")
        
        # Plataformas
        plataformas = game_info.get('plataformas', [])
        if plataformas and plataformas[0] != "N/A":
            print(f"    Plataformas: {', '.join(plataformas)}")
        
        # Descrição
        descricao = game_info.get('descricao', '')
        if descricao and descricao != "N/A":
            print(f"\n DESCRIÇÃO:")
            print(f"   {descricao}")
        
        # Curiosidade
        curiosidade = game_info.get('curiosidade', '')
        if curiosidade and curiosidade != "N/A":
            print(f"\n CURIOSIDADE:")
            print(f"   {curiosidade}")
        
        # Fonte
        fonte = game_info.get('fonte', '')
        if fonte:
            print(f"\n Fonte: {fonte}")
        
        print("─" * 50)
    
    # Cria uma tabela comparativa entre jogos
    @staticmethod
    def create_comparison_table(games_info: list):
        
        if not games_info:
            print(" Nenhum jogo para comparar.")
            return
        
        print("\n COMPARAÇÃO ENTRE JOGOS")
        print("=" * 100)
        
        headers = ["Jogo", "Gênero", "Ano", "Metacritic", "Tempo (h)"]
        print(f"{headers[0]:<25} {headers[1]:<20} {headers[2]:<8} {headers[3]:<12} {headers[4]:<10}")
        print("-" * 100)
        
        for game in games_info:
            nome = game.get('nome', 'Desconhecido')[:24]
            genero = game.get('genero', 'N/A')[:19]
            ano = str(game.get('ano_lancamento', 'N/A'))[:7]
            
            metacritic = game.get('metacritic_score', 'N/A')
            if metacritic != "N/A" and metacritic is not None:
                try:
                    metacritic = f"{int(metacritic)}/100"
                except:
                    pass
            
            tempo = game.get('tempo_medio_conclusao', 'N/A')
            if tempo != "N/A" and tempo is not None:
                tempo = f"{tempo:.1f}"
            
            print(f"{nome:<25} {genero:<20} {ano:<8} {metacritic:<12} {tempo:<10}")
        
        print("=" * 100)
    
    # Gera uma recomendação baseada nas informações do jogo
    @staticmethod
    def get_recommendation_based_on_game(game_info: Dict[str, Any]) -> str:
        
        genero = game_info.get('genero', '').lower()
        score = game_info.get('metacritic_score')
        
        recomendacoes = {
            'rpg': ["The Witcher 3", "Elden Ring", "Baldur's Gate 3", "Cyberpunk 2077"],
            'ação': ["God of War", "Doom Eternal", "Devil May Cry 5", "Hades"],
            'aventura': ["The Legend of Zelda", "Uncharted 4", "Red Dead Redemption 2", "Horizon Zero Dawn"],
            'estratégia': ["Civilization VI", "XCOM 2", "StarCraft II", "Age of Empires IV"],
            'esporte': ["FIFA 23", "NBA 2K24", "Rocket League", "Tony Hawk's Pro Skater 1+2"],
            'corrida': ["Forza Horizon 5", "Gran Turismo 7", "Mario Kart 8", "F1 2023"],
        }
        
        for key, games in recomendacoes.items():
            if key in genero:
                return f" Baseado no gênero '{genero}', talvez você goste de: {', '.join(games[:3])}"
        
        if score and score != "N/A":
            try:
                score_num = int(score)
                if score_num >= 90:
                    return " Este é um jogo excelente! Você tem bom gosto!"
                elif score_num >= 80:
                    return " Este jogo tem ótimas críticas!"
                elif score_num >= 70:
                    return " Um jogo sólido e divertido!"
            except:
                pass
        
        return " Continue explorando novos jogos!"