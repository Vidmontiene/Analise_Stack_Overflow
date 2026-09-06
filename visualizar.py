import pandas as pd
pd.set_option('display.max_rows', None)

# Recolhe os dados de uma coluna específica
def analisar_dados(nome_coluna, nome_arquivo):

  dados = pd.read_csv(f"dados/{nome_arquivo}.csv", usecols=[nome_coluna])
  result = {}

  # Percorre os dados
  for linha in dados.itertuples():
    dbs = linha[1]

    # Remove nan
    if pd.isna(dbs):
      continue

    bancos_separados = dbs.split(';')
    for banco in bancos_separados:
      if banco in result:
        result[banco] += 1
      else:
        result[banco] = 1

  result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
  result = dict(list(result.items())[:10])
  return result

# Pega em porcentagem
def porcentagem(dados):
  total = sum(dados.values())
  porcent = {}

  for db, qt in dados.items():
    pc = (qt*100) / total
    porcent[db] = pc

  return porcent
