# Analise_Stack_Overflow
Algoritmos para analisar dados do Stack Overflow

## Pesquisas

Os arquivos CSV usadas na criação dos gráficos estão disponíveis em [https://drive.google.com/drive/folders/1EMkkaWZIwP6XunUhbwFtrIFOTKEO3x9h](https://drive.google.com/drive/folders/1EMkkaWZIwP6XunUhbwFtrIFOTKEO3x9h)

## Preparacao das bases

Para juntar os CSVs de `dados/2011.csv` ate `dados/2025.csv` e gerar a base analitica de linguagens:

```bash
python preparar_bases_linguagens.py
```

Arquivos gerados:

- `dados/stackoverflow_2011_2025_consolidado.csv`: todas as respostas em um CSV, com a coluna `ano`.
- `dados/stackoverflow_linguagens_2011_2025_long.csv`: base longa com `ano`, `resposta_id`, `tipo`, `linguagem`, `linguagem_original` e `coluna_origem`.
- `dados/stackoverflow_linguagens_2011_2025_resumo.csv`: contagens e percentuais por ano, tipo e linguagem.
- `dados/stackoverflow_linguagens_2011_2025_mapeamento_colunas.csv`: colunas usadas para extrair linguagens em cada ano.

Na base longa, `tipo` separa `ja_trabalhou` de `quer_trabalhar`. Quando o questionario nao tinha coluna equivalente a desejo/futuro, a linguagem foi tratada como `ja_trabalhou`.
