
# Cliente para integração com a API do Google Gemini AI.


import os
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Cliente para consumir a API do Google Gemini AI
class GeminiClient:
     
    # Inicializa o cliente Gemini
    def __init__(self, api_key: str = None):
    
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.5-flash" 
        
        if not self.api_key:
            raise ValueError(" Chave da API Gemini não encontrada. Configure GEMINI_API_KEY no .env")
    
    # Obtém informações sobre um jogo específico
    def get_game_info(self, game_name: str, platform: str = None) -> Dict[str, Any]:
        
        prompt = self._create_game_prompt(game_name, platform)
        
        try:
            response = self._make_request(prompt)
            return self._parse_response(response, game_name)
            
        except Exception as e:
            print(f" Erro ao consultar Gemini API: {e}")
            return self._get_default_response(game_name)
    
    # Cria o prompt para a API
    def _create_game_prompt(self, game_name: str, platform: str = None) -> str:
       
        platform_info = f" para a plataforma {platform}" if platform else ""
        
        prompt = f"""
        Por favor, forneça informações sobre o jogo "{game_name}"{platform_info}.
        
        Responda APENAS com um objeto JSON válido contendo as seguintes chaves:
        - "nome": nome do jogo
        - "genero": gênero principal
        - "desenvolvedor": desenvolvedor principal
        - "publicador": publicador
        - "ano_lancamento": ano de lançamento (apenas ano)
        - "descricao": descrição breve (máximo 200 caracteres)
        - "metacritic_score": pontuação no Metacritic (0-100) ou "N/A"
        - "tempo_medio_conclusao": tempo médio para conclusão em horas
        - "plataformas": lista das plataformas disponíveis
        - "curiosidade": uma curiosidade interessante sobre o jogo
        
        IMPORTANTE:
        1. Se não encontrar informações suficientes, use "N/A" para campos desconhecidos
        2. Mantenha o texto em português do Brasil
        3. Formate "tempo_medio_conclusao" como número (ex: 25.5)
        4. Para "plataformas", retorne uma lista de strings
        
        Exemplo de resposta:
        {{
            "nome": "The Witcher 3: Wild Hunt",
            "genero": "RPG de ação",
            "desenvolvedor": "CD Projekt Red",
            "publicador": "CD Projekt",
            "ano_lancamento": 2015,
            "descricao": "RPG de mundo aberto em um universo de fantasia sombria.",
            "metacritic_score": 93,
            "tempo_medio_conclusao": 51.5,
            "plataformas": ["PC", "PlayStation 4", "Xbox One", "Nintendo Switch"],
            "curiosidade": "Originalmente, o jogo teria 3 finais, mas acabou com 36 finais diferentes."
        }}
        """
        
        return prompt
    
    # Faz a requisição para a API
    def _make_request(self, prompt: str) -> Dict[str, Any]:
       
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 1,
                "topP": 0.8,
                "maxOutputTokens": 1024,
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        return response.json()
    
    # Processa a resposta da API
    def _parse_response(self, api_response: Dict[str, Any], game_name: str) -> Dict[str, Any]:
        
        try:
            # Extrai o texto da resposta
            text_response = api_response["candidates"][0]["content"]["parts"][0]["text"]
            
            # Tenta encontrar JSON na resposta
            start_idx = text_response.find('{')
            end_idx = text_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = text_response[start_idx:end_idx]
                game_info = json.loads(json_str)
                
                # Adiciona informações de fonte
                game_info["fonte"] = "Google Gemini AI"
                game_info["consulta"] = game_name
                
                return game_info
            else:
                raise ValueError("Resposta não contém JSON válido")
                
        except (KeyError, json.JSONDecodeError, ValueError) as e:
            print(f"  Erro ao processar resposta da API: {e}")
            print(f" Resposta recebida: {text_response[:200]}...")
            return self._get_default_response(game_name)
    
    # Retorna uma resposta padrão em caso de erro
    def _get_default_response(self, game_name: str) -> Dict[str, Any]:
     
        return {
            "nome": game_name,
            "genero": "N/A",
            "desenvolvedor": "N/A",
            "publicador": "N/A",
            "ano_lancamento": "N/A",
            "descricao": "Informações não disponíveis no momento.",
            "metacritic_score": "N/A",
            "tempo_medio_conclusao": "N/A",
            "plataformas": ["N/A"],
            "curiosidade": "N/A",
            "fonte": "Sistema (API indisponível)",
            "consulta": game_name
        }
    
    # Testa a conexão com a API
    def test_connection(self) -> bool:
      
        try:
            test_prompt = "Responda apenas com a palavra 'OK'"
            response = self._make_request(test_prompt)
            return "OK" in response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        except Exception:
            return False

# Classe para gerenciamento do cache
class GeminiCache:
    
    # Inicia o cache
    def __init__(self, cache_file: str = "gemini_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    # Carrega o cache
    def _load_cache(self) -> Dict[str, Dict]:
       
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}
    
    # Salva o cache
    def _save_cache(self):
        
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except IOError:
            pass
    
    # Obtem informações do cache
    def get(self, game_name: str, platform: str = None) -> Optional[Dict]:
        
        cache_key = f"{game_name.lower()}_{platform.lower() if platform else 'any'}"
        return self.cache.get(cache_key)
    
    # Define infos no cache
    def set(self, game_name: str, platform: str, game_info: Dict):
        
        cache_key = f"{game_name.lower()}_{platform.lower() if platform else 'any'}"
        self.cache[cache_key] = game_info
        self._save_cache()
   
    # Limpa o cache
    def clear(self):
       
        self.cache = {}
        self._save_cache()