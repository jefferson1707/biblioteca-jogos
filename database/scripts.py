#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Scripts SQL para operações no banco de dados.


# Contém scripts SQL parametrizados
class SQLScripts:
    
    # Gera script SELECT
    @staticmethod
    def select(table, columns="*", where=None):
        """Gera script SELECT."""
        columns_str = columns if columns == "*" else ", ".join(columns)
        sql = f"SELECT {columns_str} FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        return sql
    
    # Gera script para consultar jogador por palavra-chave
    @staticmethod
    def select_player_by_password():
    
        return "SELECT JogadorID, Palavra_chave FROM Jogadores WHERE Palavra_chave = ?"
    
    # Gera script para consultar jogos por jogador
    @staticmethod
    def select_games_by_player():
        
        return "SELECT * FROM Jogos WHERE JogadorID = ?"
    
    # Gera script INSERT
    @staticmethod
    def insert(table, columns):
      
        if not columns:
            raise ValueError("É necessário informar as colunas para o INSERT")
        
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        
        return f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    
    # Gera script DELETE
    @staticmethod
    def delete(table, conditions):
        
        if not conditions:
            raise ValueError("É necessário informar as condições para o DELETE")
        
        return f"DELETE FROM {table} WHERE {conditions}"