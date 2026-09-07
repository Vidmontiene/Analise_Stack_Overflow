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
    gerar_lineplot(dados)
    print(f"Gráficos gerados em: {GRAPHICS_DIR}")


if __name__ == "__main__":
    main()
