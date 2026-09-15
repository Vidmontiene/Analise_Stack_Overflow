"""
Analise de tecnologias no Stack Overflow Developer Survey (2011-2025).

Gera:
  - graficos/top10_por_ano/top10_{ANO}.png  -- barras horizontais, top 10
    tipos de tecnologia por ano, com contagem e % do total anual.
  - graficos/evolucao_categorias.png -- linhas com a evolucao de cada tipo
    ao longo dos anos (magnitude absoluta, cores fixas e distintas por tipo).
"""

from pathlib import Path
import sqlite3
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "bancos" / "pesquisa.db"
GRAFICOS_DIR = BASE_DIR / "graficos"
TOP10_DIR = GRAFICOS_DIR / "top10_por_ano"
EVOLUCAO_PATH = GRAFICOS_DIR / "evolucao_categorias.png"

# ---------------------------------------------------------------------------
# Consulta SQL
# ---------------------------------------------------------------------------
QUERY = """
WITH normalizada AS (
    SELECT ano, LOWER(linguagem) AS lang
    FROM stackoverflow_linguagens_2011_2025_long
),
canonizada AS (
    SELECT ano,
        CASE
            WHEN lang LIKE '%javascript%'
              OR lang IN ('node.js','node','nodejs','jquery','coffeescript','typescript')
              OR lang LIKE '%jquery%'
              OR lang LIKE '%typescript%'
              OR lang LIKE '%coffeescript%'
              THEN 'Web / Front-end (JS/TS)'
            WHEN lang LIKE '%html%' OR lang LIKE '%css%' OR lang LIKE '%xhtml%'
              THEN 'Web / Front-end (HTML/CSS)'
            WHEN lang LIKE '%actionscript%' OR lang LIKE '%flex%'
              THEN 'Web / Front-end (ActionScript)'
            WHEN lang LIKE '%php%'        THEN 'Web / Back-end (PHP)'
            WHEN lang LIKE '%ruby%'       THEN 'Web / Back-end (Ruby)'
            WHEN lang LIKE '%coldfusion%' THEN 'Web / Back-end (ColdFusion)'
            WHEN lang LIKE '%python%'     THEN 'Dados / IA (Python)'
            WHEN lang = 'r' OR lang LIKE 'r %' OR lang LIKE '%, r'
              OR lang IN ('r,','r;')      THEN 'Dados / IA (R)'
            WHEN lang LIKE '%matlab%' OR lang LIKE '%octave%'
              THEN 'Dados / IA (MATLAB/Octave)'
            WHEN lang LIKE '%julia%'  THEN 'Dados / IA (Julia)'
            WHEN lang LIKE '%sas%'    THEN 'Dados / IA (SAS)'
            WHEN lang LIKE '%sql%' OR lang LIKE '%mysql%'
              OR lang LIKE '%pl/sql%' OR lang LIKE '%plsql%'
              THEN 'Banco de Dados (SQL)'
            WHEN lang LIKE '%java%' AND lang NOT LIKE '%javascript%'
              AND lang NOT LIKE '%jquery%'
              THEN 'Proposito Geral (Java)'
            WHEN lang LIKE '%c#%' OR lang LIKE '%csharp%' OR lang LIKE 'c sharp%'
              THEN 'Proposito Geral (C#)'
            WHEN lang LIKE '%go%' OR lang LIKE '%golang%'
              THEN 'Proposito Geral (Go)'
            WHEN lang LIKE '%scala%'  THEN 'Proposito Geral (Scala)'
            WHEN lang LIKE '%groovy%' THEN 'Proposito Geral (Groovy)'
            WHEN lang LIKE '%visual basic%' OR lang LIKE '%vb.net%'
              OR lang LIKE '%vba%' OR lang LIKE '%vb6%'
              OR lang = 'vb' OR lang LIKE 'vb %'
              THEN 'Proposito Geral (VB/VBA)'
            WHEN lang LIKE '%delphi%' OR lang LIKE '%object pascal%'
              OR lang LIKE '%pascal%'
              THEN 'Proposito Geral (Delphi/Pascal)'
            WHEN lang LIKE '%c++%' OR lang LIKE '%c++11%' THEN 'Sistemas (C++)'
            WHEN lang = 'c' OR lang LIKE 'c,' OR lang LIKE 'c %'
              THEN 'Sistemas (C)'
            WHEN lang LIKE '%rust%'        THEN 'Sistemas (Rust)'
            WHEN lang LIKE '%zig%'         THEN 'Sistemas (Zig)'
            WHEN lang LIKE '%nim%'         THEN 'Sistemas (Nim)'
            WHEN lang LIKE '%crystal%'     THEN 'Sistemas (Crystal)'
            WHEN lang LIKE '%webassembly%' THEN 'Sistemas (WebAssembly)'
            WHEN lang LIKE '%kotlin%'       THEN 'Mobile (Kotlin)'
            WHEN lang LIKE '%swift%'        THEN 'Mobile (Swift)'
            WHEN lang LIKE '%objective-c%' OR lang LIKE '%objective c%'
              OR lang LIKE '%obj-c%' OR lang LIKE '%objectivec%'
              THEN 'Mobile (Objective-C)'
            WHEN lang LIKE '%android%'     THEN 'Mobile (Android)'
            WHEN lang LIKE '%dart%'        THEN 'Mobile (Dart/Flutter)'
            WHEN lang LIKE '%bash%' OR lang LIKE '%shell%'
              OR lang LIKE '%/sh%' OR lang IN ('sh')
              THEN 'DevOps / Scripting (Bash/Shell)'
            WHEN lang LIKE '%powershell%'  THEN 'DevOps / Scripting (PowerShell)'
            WHEN lang LIKE '%haskell%'     THEN 'Funcional (Haskell)'
            WHEN lang LIKE '%elixir%'      THEN 'Funcional (Elixir)'
            WHEN lang LIKE '%clojure%'     THEN 'Funcional (Clojure)'
            WHEN lang LIKE '%erlang%'      THEN 'Funcional (Erlang)'
            WHEN lang LIKE '%f#%'          THEN 'Funcional (F#)'
            WHEN lang LIKE '%lisp%' OR lang LIKE '%scheme%' OR lang LIKE '%racket%'
              THEN 'Funcional (Lisp/Scheme)'
            WHEN lang LIKE '%ocaml%'       THEN 'Funcional (OCaml)'
            WHEN lang LIKE '%assembly%' OR lang LIKE '%assembler%'
              OR lang LIKE '%asm%' OR lang LIKE '%nasm%'
              OR lang LIKE '%x86%' OR lang LIKE '%mips%'
              THEN 'Baixo Nivel (Assembly)'
            WHEN lang LIKE '%fortran%'     THEN 'Baixo Nivel (Fortran)'
            WHEN lang LIKE '%vhdl%' OR lang LIKE '%verilog%'
              THEN 'Baixo Nivel (VHDL/Verilog)'
            WHEN lang LIKE '%ada%'         THEN 'Baixo Nivel (Ada)'
            WHEN lang LIKE '%perl%'        THEN 'Scripting (Perl)'
            WHEN lang LIKE '%lua%'         THEN 'Scripting (Lua)'
            WHEN lang LIKE '%solidity%'    THEN 'Blockchain (Solidity)'
            WHEN lang LIKE '%cobol%'       THEN 'Legado (COBOL)'
            WHEN lang LIKE '%prolog%'      THEN 'Academico (Prolog)'
            ELSE NULL
        END AS categoria
    FROM normalizada
)
SELECT ano, categoria, COUNT(*) AS ocorrencias
FROM canonizada
WHERE categoria IS NOT NULL
GROUP BY ano, categoria
ORDER BY ano, ocorrencias DESC;
"""

# ---------------------------------------------------------------------------
# Paleta curada -- 14 matizes distintos no circulo cromatico.
#
# Cada tipo ocupa uma regiao de matiz unica. Criterios:
#   1. Sem dois tipos no mesmo "setor" cromatico (ex: sem ciano E azul-medio).
#   2. Sem dois amarelos/dourados adjacentes.
#   3. Associacao semantica onde possivel (azul = web, verde = dados...).
#
# Matizes usados (graus):
#   H0   vermelho    H22  laranja-queimado   H54  oliva-escuro
#   H88  verde-lima  H124 verde-floresta     H174 teal
#   H216 azul-cobalt H232 indigo-escuro      H257 violeta-medio
#   H283 roxo-uva    H338 rosa-magenta       H17  marrom (baixa sat.)
#   + 2 neutros (cinza escuro / cinza medio)
# ---------------------------------------------------------------------------
CORES_POR_TIPO: dict = {
    "Web / Front-end":    "#1565c0",   # azul cobalto        H216
    "Web / Back-end":     "#e65100",   # laranja queimado    H22
    "Dados / IA":         "#2e7d32",   # verde floresta      H124
    "Banco de Dados":     "#b71c1c",   # vermelho escuro     H0
    "Proposito Geral":    "#4a148c",   # roxo uva escuro     H283
    "Sistemas":           "#5d4037",   # marrom-terra        H17 (baixa sat.)
    "Mobile":             "#c51162",   # rosa-magenta        H338
    "DevOps / Scripting": "#37474f",   # cinza-ardosia       neutro escuro
    "Funcional":          "#00897b",   # teal medio          H174
    "Baixo Nivel":        "#827717",   # oliva escuro        H54
    "Scripting":          "#1a237e",   # indigo escuro       H232
    "Blockchain":         "#8bc34a",   # verde-lima          H88
    "Legado":             "#9e9e9e",   # cinza medio         neutro
    "Academico":          "#5c35b1",   # violeta medio       H257
    "Outro":              "#c7c7c7",   # cinza claro (fallback)
}

# Ordem da legenda: cores opostas no circulo cromatico ficam ADJACENTES,
# garantindo maximo contraste entre entradas consecutivas.
ORDEM_LEGENDA = [
    "Banco de Dados",      # H0    vermelho
    "Funcional",           # H174  teal          (~oposto)
    "Web / Back-end",      # H22   laranja
    "Web / Front-end",     # H216  azul           (~oposto)
    "Baixo Nivel",         # H54   oliva
    "Scripting",           # H232  indigo         (~oposto)
    "Blockchain",          # H88   verde-lima
    "Academico",           # H257  violeta        (~oposto)
    "Dados / IA",          # H124  verde
    "Proposito Geral",     # H283  roxo           (~oposto)
    "Sistemas",            # H17   marrom (quente-neutro)
    "Mobile",              # H338  rosa-magenta   (~oposto)
    "DevOps / Scripting",  # neutro escuro
    "Legado",              # neutro medio         (~oposto em luminosidade)
]


def _extrair_tipo(categoria: str) -> str:
    """
    Remove o sufixo parentetico de uma categoria detalhada e retorna o tipo pai.
    Ex: 'Proposito Geral (Java)'  -> 'Proposito Geral'
        'Web / Front-end (JS/TS)' -> 'Web / Front-end'
    """
    return re.sub(r"\s*\(.*\)$", "", categoria).strip() or categoria


def _cor(tipo: str) -> str:
    return CORES_POR_TIPO.get(tipo, CORES_POR_TIPO["Outro"])


# ---------------------------------------------------------------------------
# Carregamento e agregacao
# ---------------------------------------------------------------------------

def carregar_dados() -> pd.DataFrame:
    """Carrega as contagens anuais por subcategoria do banco SQLite."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql_query(QUERY, conn)


def agregar_por_tipo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Colapsa subcategorias no tipo pai somando ocorrencias.
    Ex: 'Proposito Geral (Java)' + 'Proposito Geral (C#)' -> 'Proposito Geral'.
    """
    df = df.copy()
    df["tipo"] = df["categoria"].apply(_extrair_tipo)
    return (
        df.groupby(["ano", "tipo"], as_index=False)["ocorrencias"]
        .sum()
        .sort_values(["ano", "ocorrencias"], ascending=[True, False])
    )


# ---------------------------------------------------------------------------
# Graficos
# ---------------------------------------------------------------------------

def gerar_top10_por_ano(df_tipos: pd.DataFrame) -> None:
    """
    Um grafico de barras horizontal por ano com o top 10 de tipos.
    Cada barra exibe: contagem absoluta e percentual sobre o total do ano.
    """
    TOP10_DIR.mkdir(parents=True, exist_ok=True)

    for ano, grupo in df_tipos.groupby("ano", sort=True):
        total_ano = grupo["ocorrencias"].sum()

        top10 = (
            grupo.sort_values("ocorrencias", ascending=False)
            .head(10)
            .sort_values("ocorrencias", ascending=True)
            .reset_index(drop=True)
        )

        fig, ax = plt.subplots(figsize=(14, 7))
        bars = ax.barh(
            top10["tipo"],
            top10["ocorrencias"],
            color=[_cor(t) for t in top10["tipo"]],
            edgecolor="white",
            linewidth=0.6,
            height=0.65,
        )

        x_max = top10["ocorrencias"].max()
        for bar in bars:
            w = bar.get_width()
            pct = w / total_ano * 100
            label = f"{int(w):,}  ({pct:.1f}%)".replace(",", ".")
            ax.text(
                w + x_max * 0.012,
                bar.get_y() + bar.get_height() / 2,
                label,
                va="center",
                ha="left",
                fontsize=9,
                color="#333333",
            )

        ax.set_xlim(right=x_max * 1.30)
        ax.set_title(
            f"Top 10 Tipos de Tecnologia Mais Utilizados em {ano}",
            fontsize=14,
            fontweight="bold",
            pad=12,
        )
        ax.set_xlabel("Numero de Ocorrencias", fontsize=11)
        ax.set_ylabel("")
        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "."))
        )
        ax.grid(axis="x", alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.text(
            0.99, 0.01,
            f"Total de ocorrencias em {ano}: {int(total_ano):,}".replace(",", "."),
            ha="right", va="bottom", fontsize=8, color="#777777",
        )

        fig.tight_layout()
        fig.savefig(TOP10_DIR / f"top10_{ano}.png", dpi=200, bbox_inches="tight")
        plt.close(fig)
        print(f"  top10_{ano}.png gerado.")


def gerar_evolucao(df_tipos: pd.DataFrame) -> None:
    """
    Grafico de linhas: evolucao absoluta dos top 15 tipos ao longo dos anos.
    Cores fixas por tipo; legenda ordenada de forma intercalada (quente/frio)
    para que cores similares nao fiquem adjacentes.
    """
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    top_tipos = (
        df_tipos.groupby("tipo")["ocorrencias"]
        .sum()
        .nlargest(15)
        .index.tolist()
    )

    pivot = (
        df_tipos[df_tipos["tipo"].isin(top_tipos)]
        .pivot_table(index="ano", columns="tipo", values="ocorrencias", aggfunc="sum")
        .fillna(0)
        .sort_index()
    )

    # Ordena colunas pela ORDEM_LEGENDA para maximizar contraste na legenda.
    presentes = [t for t in ORDEM_LEGENDA if t in pivot.columns]
    restantes = [t for t in pivot.columns if t not in presentes]
    pivot = pivot[presentes + restantes]

    fig, ax = plt.subplots(figsize=(18, 9))

    for tipo in pivot.columns:
        ax.plot(
            pivot.index,
            pivot[tipo],
            marker="o",
            linewidth=2.5,
            markersize=6,
            label=tipo,
            color=_cor(tipo),
        )

    ax.set_title(
        "Evolucao dos Tipos de Tecnologia no Stack Overflow (2011-2025)",
        fontsize=15,
        fontweight="bold",
        pad=14,
    )
    ax.set_xlabel("Ano", fontsize=12)
    ax.set_ylabel("Numero de Ocorrencias", fontsize=12)
    ax.set_xticks(sorted(pivot.index))
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "."))
    )
    ax.grid(axis="y", alpha=0.25, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(
        title="Tipo de Tecnologia",
        title_fontsize=10,
        fontsize=9,
        bbox_to_anchor=(1.01, 1),
        loc="upper left",
        frameon=True,
    )

    fig.tight_layout()
    fig.savefig(EVOLUCAO_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Grafico de evolucao salvo em: {EVOLUCAO_PATH}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Banco nao encontrado: {DATABASE_PATH}. "
            "Execute criar_db.py apos colocar os CSVs em dados/."
        )

    print("Carregando dados do banco de dados...")
    df = carregar_dados()

    if df.empty:
        raise ValueError("O banco nao contem ocorrencias para gerar graficos.")

    print(
        f"  {len(df)} subcategorias carregadas, "
        f"{df['categoria'].nunique()} subcategorias distintas, "
        f"{df['ano'].nunique()} anos."
    )

    print("Agrupando subcategorias por tipo pai...")
    df_tipos = agregar_por_tipo(df)
    print(f"  {df_tipos['tipo'].nunique()} tipos apos agrupamento.")

    print("Gerando graficos top-10 por ano...")
    gerar_top10_por_ano(df_tipos)

    print("Gerando grafico de evolucao...")
    gerar_evolucao(df_tipos)

    print(f"\nTodos os graficos foram salvos em: {GRAFICOS_DIR}")


if __name__ == "__main__":
    main()
