import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vizualizar import analisar_dados, porcentagem

def criar_grafico(lista_dados, lista_anos, titulo):

  fig, ax = plt.subplots(figsize=(8, 6))
  bottom = np.zeros(len(lista_anos))

  # Usa o primeiro como referência
  ref = list(lista_dados[0].keys())

  for dado in ref:
    valores = [
      dados_2024_porcent.get(dado, 0),
      dados_2025_porcent.get(dado, 0)
    ]

    p = ax.bar(lista_anos, valores, bottom=bottom, label=dado)
    ax.bar_label(p, label_type="center")

    bottom += valores

  ax.set_title(titulo)
  ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

  plt.tight_layout()
  plt.show()

# Coleta de dados
dados_2025 = analisar_dados('DatabaseAdmired', '2025')
dados_2024 = analisar_dados('DatabaseAdmired', '2024')

# Porcentagem
dados_2025_porcent = porcentagem(dados_2025)
dados_2024_porcent = porcentagem(dados_2024)

anos = ['2025', '2024']

criar_grafico([dados_2024_porcent, dados_2025_porcent], anos, "Porcentagem Bancos")
