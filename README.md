# 🔎 Análise Stack Overflow

Anualmente, a plataforma Stack Overflow realiza uma pesquisa com seus usuários e disponibiliza seus dados em seu [site](https://survey.stackoverflow.co/). A partir desses dados, foram desenvolvidos dois artigos:

- **Artigo 1 — Evolução do Uso de Linguagens de Programação: Uma Análise com
  Dados do Stack Overflow**
- **Artigo 2 — Tendências Tecnológicas na Comunidade de Desenvolvedores: Uma
  Análise das Pesquisas do Stack Overflow**

Os artigos em PDF estão disponíveis [aqui](/artigos/).

## 🖥️ Instalando bibliotecas necessárias

```
pip install -r requirements.txt
```

## 💾 Preparação das bases

Os arquivos CSV disponíveis no site do Stack Overflow podem ser consultados [aqui](https://drive.google.com/drive/folders/1EMkkaWZIwP6XunUhbwFtrIFOTKEO3x9h).

Para juntar os CSVs de `dados/2011.csv` até `dados/2025.csv` e gerar a base analítica de linguagens:

```bash
python preparar_bases_linguagens.py
```

Arquivos gerados:

- `dados/stackoverflow_2011_2025_consolidado.csv`: todas as respostas em um CSV, com a coluna `ano`.
- `dados/stackoverflow_linguagens_2011_2025_long.csv`: base longa com `ano`, `resposta_id`, `tipo`, `linguagem`, `linguagem_original` e `coluna_origem`.
- `dados/stackoverflow_linguagens_2011_2025_resumo.csv`: contagens e percentuais por ano, tipo e linguagem.
- `dados/stackoverflow_linguagens_2011_2025_mapeamento_colunas.csv`: colunas usadas para extrair linguagens em cada ano.

Na base longa, `tipo` separa `ja_trabalhou` de `quer_trabalhar`. Quando o questionário não tinha coluna equivalente a desejo/futuro, a linguagem foi tratada como `ja_trabalhou`.

## 📊 Geração das figuras

Para gerar os gráficos do artigo 1 (Evolução do Uso de Linguagens de Programação: Uma Análise com Dados do Stack Overflow):

```bash
python .\folder_article_1\main.py
```

Para gerar os gráficos do artigo 2 (Tendências Tecnológicas na Comunidade de Desenvolvedores: Uma Análise das Pesquisas do Stack Overflow):

```bash
python .\folder_article_2\main.py
```

## 👨‍💻 Autores

### Artigo 1: 

- [Camila Vidmontiene](https://github.com/Vidmontiene);
- [Bruno Presta](https://github.com/Brunodpp); 
- [Felipe Soares](https://github.com/FelipeMYS)

### Artigo 2: 

- [Yan Martins](https://github.com/1yanmrts);
- [João Nunes](https://github.com/jaovitons); 
- [Eraldo Botelho](https://github.com/SlliperySwan)

### Orientação

- [Tássio Sirqueira](https://github.com/tassioferenzini)
- [Jéssica Faciroli](http://lattes.cnpq.br/8540581494874227)