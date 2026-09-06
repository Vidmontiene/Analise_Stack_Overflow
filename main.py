import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

conexao = sqlite3.connect("bancos/pesquisa.db")
cursor = conexao.cursor()

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

anos = [str(x) for x in range(2011, 2026)]

for ano in anos:
  resultado = top_10_ano(ano)
  print(resultado)
