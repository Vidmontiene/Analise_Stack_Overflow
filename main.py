import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from gerar_grafico_linguagens import QUERY


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "bancos" / "pesquisa.db"
GRAPHICS_DIR = BASE_DIR / "graficos"


def carregar_ocorrencias() -> pd.DataFrame:
    """Load all yearly category counts with one database scan."""
    with sqlite3.connect(DATABASE_PATH) as conexao:
        return pd.read_sql_query(QUERY, conexao)


def gerar_top10_por_ano(dados: pd.DataFrame) -> None:
    diretorio = GRAPHICS_DIR / "top10_por_ano"
    diretorio.mkdir(parents=True, exist_ok=True)

    for ano, dados_ano in dados.groupby("year", sort=True):
        top10 = dados_ano.sort_values(
            ["occurrences", "language_type"],
            ascending=[False, True],
        ).head(10)
        figura, eixo = plt.subplots(figsize=(12, 6))
        eixo.bar(top10["language_type"], top10["occurrences"])
        eixo.set_title(f"Top 10 categorias de tecnologias mais utilizadas em {ano}")
        eixo.set_xlabel("Categoria")
        eixo.set_ylabel("Ocorrências")
        eixo.tick_params(axis="x", rotation=45)
        figura.tight_layout()
        figura.savefig(diretorio / f"top10_{ano}.png", dpi=300)
        plt.close(figura)


def gerar_lineplot(dados: pd.DataFrame) -> None:
    diretorio = GRAPHICS_DIR / "lineplot"
    diretorio.mkdir(parents=True, exist_ok=True)
    figura, eixo = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=dados.sort_values(["year", "occurrences"]),
        x="year",
        y="occurrences",
        hue="language_type",
        marker="o",
        ax=eixo,
    )
    eixo.set_xticks(sorted(dados["year"].unique()))
    eixo.set_title("Uso das categorias de tecnologias ao longo dos anos")
    eixo.set_xlabel("Ano")
    eixo.set_ylabel("Ocorrências")
    eixo.legend(title="Categoria", loc="upper left")
    figura.tight_layout()
    figura.savefig(diretorio / "linguagens_por_ano.png", dpi=300)
    plt.close(figura)

def gerar_categorias_percentuais(dados: pd.DataFrame) -> None:
    """Generate yearly 100% stacked bars for the ten leading categories."""
    totais = dados.groupby("language_type")["occurrences"].sum()
    principais = totais.nlargest(10).index.tolist()
    dados = dados.copy()
    dados["category"] = dados["language_type"].where(
        dados["language_type"].isin(principais),
        "Outras",
    )
    dados = dados.groupby(["year", "category"], as_index=False)["occurrences"].sum()

    tabela = (
        dados.pivot(index="year", columns="category", values="occurrences")
        .fillna(0)
    )
    tabela = tabela.div(tabela.sum(axis=1), axis=0).mul(100)
    categorias = ["Outras"] + sorted(principais, key=totais.get)
    tabela = tabela.reindex(columns=categorias, fill_value=0)

    figura, eixo = plt.subplots(figsize=(14, 7))
    cores = plt.get_cmap("tab20").colors
    for indice, categoria in enumerate(categorias):
        eixo.bar(
            tabela.index,
            tabela[categoria],
            bottom=tabela[categorias[:indice]].sum(axis=1),
            label=categoria,
            color="#9e9e9e" if categoria == "Outras" else cores[indice - 1],
        )

    eixo.set_title("Principais categorias de tecnologia usadas ao longo dos anos")
    eixo.set_xlabel("Ano")
    eixo.set_ylabel("Participação (%)")
    eixo.set_ylim(0, 100)
    eixo.set_xticks(sorted(tabela.index))
    eixo.legend(title="Tecnologia", bbox_to_anchor=(1.02, 1), loc="upper left")
    figura.tight_layout()
    figura.savefig(GRAPHICS_DIR / "categorias_tecnologia_anos.png", dpi=300)
    plt.close(figura)


def main() -> None:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Banco não encontrado: {DATABASE_PATH}. "
            "Execute criar_db.py somente depois de colocar os CSVs em dados."
        )
    dados = carregar_ocorrencias()
    if dados.empty:
        raise ValueError("O banco não contém ocorrências para gerar gráficos.")
    gerar_top10_por_ano(dados)
    gerar_categorias_percentuais(dados)
    gerar_lineplot(dados)
    print(f"Gráficos gerados em: {GRAPHICS_DIR}")


if __name__ == "__main__":
    main()
