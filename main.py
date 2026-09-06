import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

conexao = sqlite3.connect("bancos/pesquisa.db")
cursor = conexao.cursor()

# SQL do top 10
def top_ano_SQL(ano, qt):

  cursor.execute(
    f"""
    SELECT
      ano,
      linguagem_original,
      COUNT(*) AS quantidade
    FROM stackoverflow_linguagens_2011_2025_long
    WHERE tipo = "ja_trabalhou" AND ano = {ano}
    GROUP BY ano, linguagem_original
    ORDER BY ano, quantidade DESC
    LIMIT {qt}
    """
  )

  return cursor.fetchall()
def top_devweb(ano):
  cursor.execute(f"""    SELECT
      ano,
      linguagem_original,
      COUNT(*) AS quantidade
    FROM stackoverflow_linguagens_2011_2025_long
    WHERE tipo = "ja_trabalhou" AND ano = {ano} and ( linguagem_original="C#" or linguagem_original= "Python" or linguagem_original= "Java" or linguagem_original= "PHP" or linguagem_original= "Ruby" or linguagem_original= "JavaScript" )
    GROUP BY ano, linguagem_original
    ORDER BY ano, quantidade DESC
    """
    )
  return cursor.fetchall()

# Pega as top 10 linguagens de cada ano
def pegar_top_10_por_ano():
  anos = [str(x) for x in range(2011, 2026)]

  for ano in anos:
    resultado = top_ano_SQL(ano, 10)

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

# Lineplot
def lineplot():
  anos = [str(x) for x in range(2011, 2026)]
  geral = []
  for ano in anos:
    resultado = top_devweb(ano)
    for linha in resultado:
      if linha[1] == "Bash/Shell (all shells)" or linha[1] == "Bash/Shell/PowerShell":
        linha = (linha[0], "Bash/Shell", linha[2])
      elif linha[1]=="HTML" or linha[1]=="CSS":
        linha=(linha[0], "HTML/CSS",linha[2])
      geral.append(linha)

  geral = pd.DataFrame(
    geral,
    columns=['ano', 'linguagem', 'quantidade']
  )

  plt.figure(figsize=(12, 6))
  sns.lineplot(
    data=geral,
    x='ano',
    y='quantidade',
    hue='linguagem'
  )
  plt.xticks(geral["ano"].unique())

  # Legenda à esquerda
  plt.legend(
    title='Linguagens',
    loc='upper left',
  )
  plt.title('Uso das linguagens de desenvolvimento web ao longo dos anos')
  plt.xlabel('Ano')
  plt.ylabel('Quantidade')
  plt.tight_layout()

  plt.savefig('graficos/lineplot/linguagens_por_ano.png', dpi=300)

lineplot()

conexao.close()
    