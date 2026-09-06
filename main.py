import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

conexao = sqlite3.connect("bancos/pesquisa.db")
cursor = conexao.cursor()

#SQL do top 10
def top_ano_SQL(ano, qt):

  cursor.execute(
    f"""
    WITH normalized AS (
    SELECT
        ano,
        CASE
        WHEN lower(linguagem) LIKE '%javascript%' THEN 'JavaScript'
        WHEN lower(linguagem) IN ('node.js','node','nodejs') THEN 'JavaScript'

        WHEN lower(linguagem) LIKE '%html%' OR lower(linguagem) LIKE '%css%' OR lower(linguagem) LIKE '%xhtml%' THEN 'HTML/CSS'

        WHEN lower(linguagem) LIKE '%sql%' OR lower(linguagem) LIKE '%mysql%' OR lower(linguagem) LIKE '%pl/sql%' OR lower(linguagem) LIKE '%plsql%' THEN 'SQL / Database'

        WHEN lower(linguagem) LIKE '%python%' THEN 'Python'
        WHEN lower(linguagem) LIKE '%java%' THEN 'Java'
        WHEN lower(linguagem) LIKE '%c++%' THEN 'C++'
        WHEN lower(linguagem) = 'c' THEN 'C'
        WHEN lower(linguagem) LIKE '%c#%' OR lower(linguagem) LIKE 'c sharp' THEN 'C#'
        WHEN lower(linguagem) LIKE '%typescript%' THEN 'TypeScript'
        WHEN lower(linguagem) LIKE '%php%' THEN 'PHP'
        WHEN lower(linguagem) LIKE '%ruby%' THEN 'Ruby'
        WHEN lower(linguagem) LIKE '%go%' OR lower(linguagem) LIKE '%golang%' THEN 'Go'
        WHEN lower(linguagem) LIKE '%rust%' THEN 'Rust'
        WHEN lower(linguagem) LIKE '%kotlin%' THEN 'Kotlin'
        WHEN lower(linguagem) LIKE '%swift%' THEN 'Swift'

        WHEN lower(linguagem) LIKE '%bash%' OR lower(linguagem) LIKE '%shell%' OR lower(linguagem) LIKE '%/sh%' THEN 'Bash / Shell'
        WHEN lower(linguagem) LIKE '%powershell%' THEN 'PowerShell'

        WHEN lower(linguagem) = 'r' OR lower(linguagem) LIKE 'r,' OR lower(linguagem) LIKE 'r %' THEN 'R'
        WHEN lower(linguagem) LIKE '%matlab%' THEN 'MATLAB'
        WHEN lower(linguagem) LIKE '%julia%' THEN 'Julia'
        WHEN lower(linguagem) LIKE '%sas%' THEN 'SAS'
        WHEN lower(linguagem) LIKE '%fortran%' THEN 'Fortran'
        WHEN lower(linguagem) LIKE '%octave%' THEN 'Octave'

        WHEN lower(linguagem) LIKE '%objective-c%' OR lower(linguagem) LIKE '%objective c%' OR lower(linguagem) LIKE '%obj-c%' THEN 'Objective-C'
        WHEN lower(linguagem) LIKE '%android%' THEN 'Android'

        WHEN lower(linguagem) LIKE '%assembly%' THEN 'Assembly'
        WHEN lower(linguagem) LIKE '%asm%' THEN 'Assembly'
        WHEN lower(linguagem) LIKE '%nasm%' THEN 'Assembly'
        WHEN lower(linguagem) LIKE '%x86%' THEN 'Assembly'
        WHEN lower(linguagem) LIKE '%arm%' AND lower(linguagem) LIKE '%assembly%' THEN 'Assembly'

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
        WHEN canonical_language IN ('JavaScript','HTML/CSS','PHP','Ruby','TypeScript','Node.js') THEN 'Web development'
        WHEN canonical_language IN ('Python','R','MATLAB','Julia','SAS','Octave') THEN 'Data analysis'
        WHEN canonical_language = 'SQL / Database' THEN 'Database'
        WHEN canonical_language IN ('Java','C#','Scala','Perl','Groovy','C','C++','Rust','Go') THEN 'General purpose / Systems'
        WHEN canonical_language IN ('Assembly','Fortran') THEN 'Systems / Low level'
        WHEN canonical_language IN ('Kotlin','Swift','Objective-C','Android') THEN 'Mobile'
        WHEN canonical_language IN ('Bash / Shell','PowerShell') THEN 'DevOps / Scripting'
        WHEN canonical_language IN ('Solidity','WebAssembly') THEN 'Other / Emerging'
        ELSE 'Other'
    END AS type,
    COUNT(*) AS occurrences
    FROM normalized
    WHERE canonical_language IS NOT NULL
    GROUP BY ano, type
    ORDER BY ano DESC, occurrences DESC;
    """
  )

  return cursor.fetchall()