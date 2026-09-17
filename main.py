import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

conexao = sqlite3.connect("bancos/pesquisa.db")
cursor = conexao.cursor()

LINGUAGEM_GRAFICO_SQL = """
  CASE
    WHEN linguagem IN ("Bash/Shell (all shells)", "Bash/Shell/PowerShell","PowerShell") THEN "Bash/Shell"
    WHEN linguagem IN ("HTML", "CSS") THEN "HTML/CSS"
    ELSE linguagem
  END
"""

CORES_LINGUAGENS = {
  "JavaScript": "#FFD600",
  "SQL": "#D65F00",
  "HTML/CSS": "#E34F26",
  "Python": "#3776AB",
  "Java": "#B07219",
  "C#": "#68217A",
  "TypeScript": "#3178C6",
  "PHP": "#6F4E37",
  "C++": "#8A2BE2",
  "C": "#A8B9CC",
  "Bash/Shell": "#4EAA25",
  "Go": "#00ADD8",
  "Ruby": "#CC342D",
  "PowerShell": "#5391FE",
  "Rust": "#DEA584",
  "Kotlin": "#A97BFF",
  "Swift": "#F05138",
  "Assembly": "#6E4C13",
  "R": "#276DC3",
  "Objective-C": "#438EFF",
  "Node.js": "#68A063",
  "VBA": "#867DB1",
  "Dart": "#0175C2",
  "MATLAB": "#E16737",
  "Scala": "#DC322F",
  "Lua": "#000080",
  "Perl": "#39457E",
  "Groovy": "#4298B8",
  "VB.NET": "#945DB7",
}

CORES_EXTRAS = sns.color_palette("tab20", 20).as_hex() + sns.color_palette("Set3", 12).as_hex()


def cor_linguagem(linguagem):
  if linguagem in CORES_LINGUAGENS:
    return CORES_LINGUAGENS[linguagem]

  indice = sum(ord(caractere) for caractere in linguagem) % len(CORES_EXTRAS)
  return CORES_EXTRAS[indice]


def paleta_linguagens(linguagens):
  return {linguagem: cor_linguagem(linguagem) for linguagem in linguagens}

# SQL do top 10
def top_ano_SQL(ano, qt):

  cursor.execute(
    f"""
    SELECT
      ano,
      {LINGUAGEM_GRAFICO_SQL} AS linguagem,
      COUNT(*) AS quantidade
    FROM stackoverflow_linguagens_2011_2025_long
    WHERE tipo = "ja_trabalhou" AND ano = {ano}
    GROUP BY ano, linguagem
    ORDER BY ano, quantidade DESC
    LIMIT {qt}
    """
  )

  return cursor.fetchall()

# SQL top linguagens web ao longo dos anos
def top_devweb(ano):
  cursor.execute(
    f"""
    SELECT
      ano,
      {LINGUAGEM_GRAFICO_SQL} AS linguagem,
      COUNT(*) AS quantidade
    FROM stackoverflow_linguagens_2011_2025_long
    WHERE tipo = "ja_trabalhou" AND ano = {ano} and ( linguagem="C#" or linguagem= "Python" or linguagem= "Java" or linguagem= "PHP" or linguagem= "Ruby" or linguagem= "JavaScript" )
    GROUP BY ano, linguagem
    ORDER BY ano, quantidade DESC
    """
    )
  return cursor.fetchall()

# Cria gráfico 10 linguagens de cada ano
def pegar_top_10_por_ano():
  anos = [str(x) for x in range(2011, 2026)]

  for ano in anos:
    resultado = top_ano_SQL(ano, 10)

    # Número de respostas no top 10
    print(f"{ano} - {len(resultado)} respostas")
    linguagens = [linha[1] for linha in resultado]
    quantidades = [linha[2] for linha in resultado]

    plt.figure(figsize=(12, 6))

    plt.bar(linguagens, quantidades, color=[cor_linguagem(linguagem) for linguagem in linguagens])

    plt.title(f'Top 10 linguagens mais usadas em {ano}')
    plt.xlabel('Linguagem')
    plt.ylabel('Quantidade')

    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(f'graficos/top10_por_ano/top10_{ano}.png', dpi=300)

# Cria gráfico Lineplot
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
    hue='linguagem',
    palette=paleta_linguagens(geral["linguagem"].unique())
  )
  plt.xticks(geral["ano"].unique())

  # Legenda à esquerda
  plt.legend(
    title='Linguagens',
    loc='upper left',
  )
  plt.title('Evolução do uso de linguagens associadas ao desenvolvimento web ao longo dos anos')
  plt.xlabel('Ano')
  plt.ylabel('Quantidade')
  plt.tight_layout()

  plt.savefig('graficos/lineplot/linguagens_por_ano.png', dpi=300)

#lineplot()
pegar_top_10_por_ano()

conexao.close()
