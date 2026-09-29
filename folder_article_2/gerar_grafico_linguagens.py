"""Generate a line chart of language-type occurrences by year."""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "bancos" / "pesquisa.db"
OUTPUT_PATH = BASE_DIR / "output" / "linguagens_por_tipo_ano.png"


QUERY = """
WITH normalized AS (
    SELECT
        ano,
        CASE
            WHEN lower(linguagem) LIKE '%javascript%'
                OR lower(linguagem) IN ('node.js', 'node', 'nodejs')
                THEN 'JavaScript'
            WHEN lower(linguagem) LIKE '%html%'
                OR lower(linguagem) LIKE '%css%'
                OR lower(linguagem) LIKE '%xhtml%'
                THEN 'HTML/CSS'
            WHEN lower(linguagem) LIKE '%sql%'
                OR lower(linguagem) LIKE '%mysql%'
                OR lower(linguagem) LIKE '%pl/sql%'
                OR lower(linguagem) LIKE '%plsql%'
                THEN 'SQL / Database'
            WHEN lower(linguagem) LIKE '%python%' THEN 'Python'
            WHEN lower(linguagem) LIKE '%java%' THEN 'Java'
            WHEN lower(linguagem) LIKE '%c++%' THEN 'C++'
            WHEN lower(linguagem) = 'c' THEN 'C'
            WHEN lower(linguagem) LIKE '%c#%'
                OR lower(linguagem) LIKE 'c sharp'
                THEN 'C#'
            WHEN lower(linguagem) LIKE '%typescript%' THEN 'TypeScript'
            WHEN lower(linguagem) LIKE '%php%' THEN 'PHP'
            WHEN lower(linguagem) LIKE '%ruby%' THEN 'Ruby'
            WHEN lower(linguagem) LIKE '%go%'
                OR lower(linguagem) LIKE '%golang%'
                THEN 'Go'
            WHEN lower(linguagem) LIKE '%rust%' THEN 'Rust'
            WHEN lower(linguagem) LIKE '%kotlin%' THEN 'Kotlin'
            WHEN lower(linguagem) LIKE '%swift%' THEN 'Swift'
            WHEN lower(linguagem) LIKE '%bash%'
                OR lower(linguagem) LIKE '%shell%'
                OR lower(linguagem) LIKE '%/sh%'
                THEN 'Bash / Shell'
            WHEN lower(linguagem) LIKE '%powershell%' THEN 'PowerShell'
            WHEN lower(linguagem) = 'r'
                OR lower(linguagem) LIKE 'r,'
                OR lower(linguagem) LIKE 'r %'
                THEN 'R'
            WHEN lower(linguagem) LIKE '%matlab%' THEN 'MATLAB'
            WHEN lower(linguagem) LIKE '%julia%' THEN 'Julia'
            WHEN lower(linguagem) LIKE '%sas%' THEN 'SAS'
            WHEN lower(linguagem) LIKE '%fortran%' THEN 'Fortran'
            WHEN lower(linguagem) LIKE '%octave%' THEN 'Octave'
            WHEN lower(linguagem) LIKE '%objective-c%'
                OR lower(linguagem) LIKE '%objective c%'
                OR lower(linguagem) LIKE '%obj-c%'
                THEN 'Objective-C'
            WHEN lower(linguagem) LIKE '%android%' THEN 'Android'
            WHEN lower(linguagem) LIKE '%assembly%'
                OR lower(linguagem) LIKE '%asm%'
                OR lower(linguagem) LIKE '%nasm%'
                OR lower(linguagem) LIKE '%x86%'
                THEN 'Assembly'
            WHEN lower(linguagem) LIKE '%scala%' THEN 'Scala'
            WHEN lower(linguagem) LIKE '%perl%' THEN 'Perl'
            WHEN lower(linguagem) LIKE '%lua%' THEN 'Lua'
            WHEN lower(linguagem) LIKE '%haskell%' THEN 'Haskell'
            WHEN lower(linguagem) LIKE '%elixir%' THEN 'Elixir'
            WHEN lower(linguagem) LIKE '%clojure%' THEN 'Clojure'
            WHEN lower(linguagem) LIKE '%groovy%' THEN 'Groovy'
            WHEN lower(linguagem) LIKE '%dart%' THEN 'Dart'
            WHEN lower(linguagem) LIKE '%solidity%' THEN 'Solidity'
            WHEN lower(linguagem) LIKE '%webassembly%' THEN 'WebAssembly'
            ELSE NULL
        END AS canonical_language
    FROM stackoverflow_linguagens_2011_2025_long
)
SELECT
    ano AS year,
    CASE
        WHEN canonical_language IN (
            'JavaScript', 'HTML/CSS', 'PHP', 'Ruby', 'TypeScript'
        ) THEN 'Web development'
        WHEN canonical_language IN (
            'Python', 'R', 'MATLAB', 'Julia', 'SAS', 'Octave'
        ) THEN 'Data analysis'
        WHEN canonical_language = 'SQL / Database' THEN 'Database'
        WHEN canonical_language IN (
            'Java', 'C#', 'Scala', 'Perl', 'Groovy', 'C', 'C++', 'Rust', 'Go'
        ) THEN 'General purpose / Systems'
        WHEN canonical_language IN ('Assembly', 'Fortran')
            THEN 'Systems / Low level'
        WHEN canonical_language IN (
            'Kotlin', 'Swift', 'Objective-C', 'Android'
        ) THEN 'Mobile'
        WHEN canonical_language IN ('Bash / Shell', 'PowerShell')
            THEN 'DevOps / Scripting'
        WHEN canonical_language IN ('Solidity', 'WebAssembly')
            THEN 'Other / Emerging'
        ELSE 'Other'
    END AS language_type,
    COUNT(*) AS occurrences
FROM normalized
WHERE canonical_language IS NOT NULL
GROUP BY ano, language_type
ORDER BY ano, language_type;
"""


def load_occurrences() -> pd.DataFrame:
    """Read yearly language-type counts from the SQLite database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(QUERY, connection)


def create_chart(data: pd.DataFrame) -> None:
    """Create and save the yearly language-type line chart."""
    chart_data = (
        data.pivot(index="year", columns="language_type", values="occurrences")
        .fillna(0)
        .sort_index()
    )

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    ax = chart_data.plot(figsize=(16, 8), linewidth=2)
    ax.set_title("Uso dos tipos de linguagem de desenvolvimento ao longo dos anos")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Quantidade de ocorrências")
    ax.set_xticks(chart_data.index)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(title="Tipos de linguagem", loc="upper left")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()


if __name__ == "__main__":
    create_chart(load_occurrences())
    print(f"Gráfico salvo em: {OUTPUT_PATH}")
