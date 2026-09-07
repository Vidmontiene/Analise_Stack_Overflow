import sqlite3
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
dados_dir = BASE_DIR / 'dados'
bancos_dir = BASE_DIR / 'bancos'
bancos_dir.mkdir(exist_ok=True)

if not dados_dir.exists():
  raise FileNotFoundError(
    f'Pasta de dados não encontrada: {dados_dir}. '
    'Coloque os CSVs na pasta dados antes de executar este script.'
  )

conexao = sqlite3.connect(bancos_dir / 'pesquisa.db')
encodings = ['utf-8', 'cp1252', 'latin1']

for arquivo in os.listdir(dados_dir):
  
  print('Começando exportação... ')
  if not arquivo.endswith('.csv'):
    continue

  # Nome do arquivo sem a extensão
  nome_tabela = os.path.splitext(arquivo)[0]

  caminho = dados_dir / arquivo

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