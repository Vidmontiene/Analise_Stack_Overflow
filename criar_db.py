import sqlite3
import pandas as pd
import os

os.makedirs('bancos', exist_ok=True)
conexao = sqlite3.connect('bancos/pesquisa.db')
encodings = ['utf-8', 'cp1252', 'latin1']

for arquivo in os.listdir('dados'):
  
  print('Começando exportação... ')
  if not arquivo.endswith('.csv'):
    continue

  # Nome do arquivo sem a extensão
  nome_tabela = os.path.splitext(arquivo)[0]

  caminho = os.path.join('dados', arquivo)

  # Tenta as codificações
  for encoding in encodings:
    try:
      df = pd.read_csv(
        caminho,
        encoding=encoding,
        low_memory=False
      )
      break
    except UnicodeDecodeError:
      continue

  df.to_sql(
    nome_tabela,
    conexao,
    if_exists='replace',
    index=False
  )

  print(f'Tabela {nome_tabela} criada com sucesso')

conexao.close()
