import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

conexao = sqlite3.connect("bancos/pesquisa.db")
cursor = conexao.cursor()

# SQL do top 10
def top_10_ano(ano):

  cursor.execute(
    f"""
    SELECT
      ano,
      linguagem_original,
      COUNT(*) AS quantidade
    FROM stackoverflow_linguagens_2011_2025_long
    WHERE ano = {ano}
    GROUP BY ano, linguagem_original
    ORDER BY ano, quantidade DESC
    LIMIT 10
    """
  )

  return cursor.fetchall()

# Pega as top 10 linguagens de cada ano
def pegar_top_10_por_ano():
  anos = [str(x) for x in range(2011, 2026)]

  for ano in anos:
    resultado = top_10_ano(ano)

    linguagens = [linha[1] for linha in resultado]
    quantidades = [linha[2] for linha in resultado]
    plt.figure(figsize=(12, 6))

    plt.bar(linguagens, quantidades)

    plt.title(f'Top 10 linguagens mais usadas em {ano}')
    plt.xlabel('Linguagem')
    plt.ylabel('Quantidade')

    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(f'graficos/top10_por_ano/top10_{ano}.png', dpi=300)

conexao.close()
    