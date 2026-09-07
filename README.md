# Analise_Stack_Overflow
Algoritmos para analisar dados do Stack Overflow

## Geracao dos graficos

Execute os comandos abaixo na raiz do projeto:

```bash
python criar_db.py
python main.py
```

Se o banco `bancos/pesquisa.db` ja existir, basta executar `python main.py`.
Os graficos sao salvos em `graficos/top10_por_ano/` e
`graficos/lineplot/`. As barras sao ordenadas por ocorrencias, com desempate
alfabetico. As categorias representam tecnologias relacionadas ao tema da
analise: desenvolvimento web, dados, banco de dados, sistemas, mobile,
DevOps/scripts e tecnologias emergentes.
