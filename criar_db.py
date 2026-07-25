import sqlite3
import pandas as pd

# Antes de rodar, criar o diretório "bancos" no caminho principal

anos = ['2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011']
conexao = sqlite3.connect('bancos/pesquisa.db')
encoding = ['utf-8', 'cp1252', 'latin1']

for ano in anos:

  if ano == '2015':
    df = pd.read_csv(
      f"dados/{ano}.csv",
      header=1,
      low_memory=False
    )
  else:
    for enc in encoding:
      try:
        df = pd.read_csv(f"dados/{ano}.csv", encoding=enc, low_memory=False)
        break
      except UnicodeDecodeError:
        continue

  df.to_sql(
    f"pesquisa_{ano}",
    conexao,
    if_exists="replace",
    index=False
  )

  print(f'Tabela {ano} criada com sucesso')

conexao.close()
