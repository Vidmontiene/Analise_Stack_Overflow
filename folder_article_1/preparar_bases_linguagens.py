import argparse
import csv
import re
import sys
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ANOS = range(2011, 2026)
ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin1")
VALORES_VAZIOS = {"", "NA", "N/A", "None", "None of these", "Other(s):"}
SEPARADOR_LISTA = ";"


@dataclass(frozen=True)
class ColunaLinguagem:
    indice: int
    nome: str
    tipo: str
    formato: str
    valor_fixo: str | None = None
    fonte_mista: bool = False


MAPEAMENTO_LINGUAGENS = {
    "Bash": "Bash/Shell",
    "Bash/Shell (all shells)": "Bash/Shell",
    "C++11": "C++",
    "CSS": "HTML/CSS",
    "HTML": "HTML/CSS",
    "HTML5": "HTML/CSS",
    "Javascript": "JavaScript",
    "Java-Script": "JavaScript",
    "Matlab": "MATLAB",
    "Typescript": "TypeScript",
    "Visual Basic (.Net)": "VB.NET",
    "Visual Basic .NET": "VB.NET",
}

LINGUAGENS_EM_FONTES_MISTAS = {
    "Ada",
    "APL",
    "Assembly",
    "Bash/Shell",
    "Bash/Shell/PowerShell",
    "C",
    "C#",
    "C++",
    "Clojure",
    "COBOL",
    "CoffeeScript",
    "Crystal",
    "Dart",
    "Delphi",
    "Delphi/Object Pascal",
    "Elixir",
    "Erlang",
    "F#",
    "Fortran",
    "GDScript",
    "Gleam",
    "Go",
    "Groovy",
    "Haskell",
    "HTML/CSS",
    "Java",
    "JavaScript",
    "Julia",
    "Kotlin",
    "Lisp",
    "Lua",
    "MATLAB",
    "MicroPython",
    "Nim",
    "Objective-C",
    "OCaml",
    "Perl",
    "PHP",
    "PowerShell",
    "Prolog",
    "Python",
    "R",
    "Raku",
    "Ruby",
    "Rust",
    "Scala",
    "SAS",
    "Solidity",
    "SQL",
    "Swift",
    "TypeScript",
    "VBA",
    "VB.NET",
    "Visual Basic",
    "Visual Basic 6",
    "WebAssembly",
    "Zig",
}


def ajustar_limite_csv() -> None:
    limite = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limite)
            return
        except OverflowError:
            limite //= 10


def detectar_encoding(caminho: Path) -> str:
    for encoding in ENCODINGS:
        try:
            with caminho.open("r", encoding=encoding, newline="") as arquivo:
                arquivo.read(1024 * 1024)
            return encoding
        except UnicodeDecodeError:
            continue
    return "latin1"


def abrir_csv(caminho: Path, encoding: str | None = None):
    return caminho.open("r", encoding=encoding or detectar_encoding(caminho), newline="")


def arquivos_origem(dados_dir: Path) -> list[Path]:
    arquivos = []
    for ano in ANOS:
        caminho = dados_dir / f"{ano}.csv"
        if caminho.exists():
            arquivos.append(caminho)
    return arquivos


def preencher_cabecalho_superior(valores: list[str]) -> list[str]:
    preenchidos = []
    atual = ""
    for valor in valores:
        valor = limpar_texto(valor)
        if valor:
            atual = valor
        preenchidos.append(atual)
    return preenchidos


def limpar_texto(valor: str | None) -> str:
    if valor is None:
        return ""
    return re.sub(r"\s+", " ", str(valor)).strip()


def tornar_unicos(cabecalhos: Iterable[str]) -> list[str]:
    contagens: Counter[str] = Counter()
    unicos = []
    for cabecalho in cabecalhos:
        nome = limpar_texto(cabecalho) or "unnamed"
        contagens[nome] += 1
        if contagens[nome] == 1:
            unicos.append(nome)
        else:
            unicos.append(f"{nome}__{contagens[nome]}")
    return unicos


def ler_layout(caminho: Path) -> tuple[int, str, list[str], int]:
    ano = int(caminho.stem)
    encoding = detectar_encoding(caminho)
    with abrir_csv(caminho, encoding) as arquivo:
        leitor = csv.reader(arquivo)
        linhas = []
        for _ in range(2):
            try:
                linhas.append(next(leitor))
            except StopIteration:
                linhas.append([])

    if 2011 <= ano <= 2014:
        superior = preencher_cabecalho_superior(linhas[0])
        inferior = linhas[1]
        cabecalhos = []
        for pergunta, opcao in zip(superior, inferior):
            pergunta = limpar_texto(pergunta)
            opcao = limpar_texto(opcao)
            if opcao and opcao.lower() != "response":
                cabecalhos.append(f"{pergunta} | {opcao}" if pergunta else opcao)
            else:
                cabecalhos.append(pergunta or opcao or "unnamed")
        linhas_cabecalho = 2
    elif ano == 2015:
        cabecalhos = [limpar_texto(valor) or "unnamed" for valor in linhas[1]]
        linhas_cabecalho = 2
    else:
        cabecalhos = [limpar_texto(valor) or "unnamed" for valor in linhas[0]]
        linhas_cabecalho = 1

    return ano, encoding, tornar_unicos(cabecalhos), linhas_cabecalho


def iterar_dados(caminho: Path, encoding: str, linhas_cabecalho: int):
    with abrir_csv(caminho, encoding) as arquivo:
        leitor = csv.reader(arquivo)
        for _ in range(linhas_cabecalho):
            next(leitor, None)
        yield from leitor


def normalizar_linguagem(valor: str) -> str:
    valor = limpar_texto(valor)
    valor = MAPEAMENTO_LINGUAGENS.get(valor, valor)
    if valor.upper() == "LISP":
        return "Lisp"
    return valor


def valor_vazio(valor: str | None) -> bool:
    return limpar_texto(valor) in VALORES_VAZIOS


def dividir_lista(valor: str) -> list[str]:
    return [limpar_texto(parte) for parte in valor.split(SEPARADOR_LISTA) if limpar_texto(parte)]


def linguagem_valida(valor: str, fonte_mista: bool) -> bool:
    if valor_vazio(valor):
        return False
    if valor.lower().startswith("other"):
        return False
    if not fonte_mista:
        return True
    return normalizar_linguagem(valor) in LINGUAGENS_EM_FONTES_MISTAS


def colunas_linguagens(ano: int, cabecalhos: list[str]) -> list[ColunaLinguagem]:
    colunas = []

    for indice, nome in enumerate(cabecalhos):
        if ano in (2011, 2012) and nome.startswith("Which languages are you proficient in? | "):
            linguagem = nome.split(" | ", 1)[1]
            colunas.append(ColunaLinguagem(indice, nome, "ja_trabalhou", "checkbox", linguagem))

        elif ano in (2013, 2014) and nome.startswith(
            "Which of the following languages or technologies have you used significantly in the past year? | "
        ):
            linguagem = nome.split(" | ", 1)[1]
            colunas.append(ColunaLinguagem(indice, nome, "ja_trabalhou", "checkbox", linguagem, True))

        elif ano in (2013, 2014) and nome.startswith("Which technologies are you excited about? | "):
            linguagem = nome.split(" | ", 1)[1]
            colunas.append(ColunaLinguagem(indice, nome, "quer_trabalhar", "checkbox", linguagem, True))

        elif ano == 2015 and nome.startswith("Current Lang & Tech: "):
            linguagem = nome.split(": ", 1)[1]
            colunas.append(ColunaLinguagem(indice, nome, "ja_trabalhou", "checkbox", linguagem, True))

        elif ano == 2015 and nome.startswith("Future Lang & Tech: "):
            linguagem = nome.split(": ", 1)[1]
            colunas.append(ColunaLinguagem(indice, nome, "quer_trabalhar", "checkbox", linguagem, True))

    colunas_lista = {
        2016: (("tech_do", "ja_trabalhou", True), ("tech_want", "quer_trabalhar", True)),
        2017: (("HaveWorkedLanguage", "ja_trabalhou", False), ("WantWorkLanguage", "quer_trabalhar", False)),
        2018: (("LanguageWorkedWith", "ja_trabalhou", False), ("LanguageDesireNextYear", "quer_trabalhar", False)),
        2019: (("LanguageWorkedWith", "ja_trabalhou", False), ("LanguageDesireNextYear", "quer_trabalhar", False)),
        2020: (("LanguageWorkedWith", "ja_trabalhou", False), ("LanguageDesireNextYear", "quer_trabalhar", False)),
        2021: (("LanguageHaveWorkedWith", "ja_trabalhou", False), ("LanguageWantToWorkWith", "quer_trabalhar", False)),
        2022: (("LanguageHaveWorkedWith", "ja_trabalhou", False), ("LanguageWantToWorkWith", "quer_trabalhar", False)),
        2023: (("LanguageHaveWorkedWith", "ja_trabalhou", False), ("LanguageWantToWorkWith", "quer_trabalhar", False)),
        2024: (("LanguageHaveWorkedWith", "ja_trabalhou", False), ("LanguageWantToWorkWith", "quer_trabalhar", False)),
        2025: (("LanguageHaveWorkedWith", "ja_trabalhou", False), ("LanguageWantToWorkWith", "quer_trabalhar", False)),
    }

    for nome_procurado, tipo, fonte_mista in colunas_lista.get(ano, ()):
        if nome_procurado in cabecalhos:
            indice = cabecalhos.index(nome_procurado)
            colunas.append(ColunaLinguagem(indice, nome_procurado, tipo, "lista", None, fonte_mista))

    return colunas


def id_resposta(ano: int, numero_linha: int, cabecalhos: list[str], linha: list[str]) -> str:
    for coluna in ("ResponseId", "Respondent"):
        if coluna in cabecalhos:
            indice = cabecalhos.index(coluna)
            if indice < len(linha) and not valor_vazio(linha[indice]):
                return f"{ano}_{limpar_texto(linha[indice])}"
    return f"{ano}_linha_{numero_linha}"


def extrair_linguagens_da_linha(linha: list[str], colunas: list[ColunaLinguagem]):
    vistas_por_tipo = defaultdict(set)
    extraidas = []

    for coluna in colunas:
        valor_celula = linha[coluna.indice] if coluna.indice < len(linha) else ""
        if coluna.formato == "checkbox":
            if valor_vazio(valor_celula):
                continue
            if coluna.valor_fixo is None:
                continue
            valores = [valor_celula] if coluna.valor_fixo.lower().startswith(("other", "write-in")) else [coluna.valor_fixo]
        else:
            if valor_vazio(valor_celula):
                continue
            valores = dividir_lista(valor_celula)

        for valor_original in valores:
            if not linguagem_valida(valor_original, coluna.fonte_mista):
                continue
            linguagem = normalizar_linguagem(valor_original)
            if linguagem in vistas_por_tipo[coluna.tipo]:
                continue
            vistas_por_tipo[coluna.tipo].add(linguagem)
            extraidas.append((coluna.tipo, linguagem, limpar_texto(valor_original), coluna.nome))

    return extraidas


def preparar_layouts(dados_dir: Path):
    layouts = OrderedDict()
    uniao_cabecalhos = OrderedDict()
    for caminho in arquivos_origem(dados_dir):
        ano, encoding, cabecalhos, linhas_cabecalho = ler_layout(caminho)
        layouts[ano] = {
            "caminho": caminho,
            "encoding": encoding,
            "cabecalhos": cabecalhos,
            "linhas_cabecalho": linhas_cabecalho,
            "colunas_linguagens": colunas_linguagens(ano, cabecalhos),
        }
        for cabecalho in cabecalhos:
            uniao_cabecalhos.setdefault(cabecalho, None)
    return layouts, list(uniao_cabecalhos)


def escrever_mapeamento(layouts, caminho_saida: Path) -> None:
    with caminho_saida.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, lineterminator="\n")
        escritor.writerow(["ano", "tipo", "formato", "coluna_origem", "fonte_mista"])
        for ano, layout in layouts.items():
            for coluna in layout["colunas_linguagens"]:
                escritor.writerow([ano, coluna.tipo, coluna.formato, coluna.nome, int(coluna.fonte_mista)])


def consolidar_bases(layouts, cabecalhos_unificados: list[str], caminho_saida: Path) -> dict[int, int]:
    posicoes_saida = {nome: posicao + 1 for posicao, nome in enumerate(cabecalhos_unificados)}
    totais = {}

    with caminho_saida.open("w", encoding="utf-8-sig", newline="") as arquivo_saida:
        escritor = csv.writer(arquivo_saida, lineterminator="\n")
        escritor.writerow(["ano", *cabecalhos_unificados])

        for ano, layout in layouts.items():
            caminho = layout["caminho"]
            cabecalhos = layout["cabecalhos"]
            linhas = 0
            for linha in iterar_dados(caminho, layout["encoding"], layout["linhas_cabecalho"]):
                if not any(limpar_texto(valor) for valor in linha):
                    continue
                saida = [""] * (len(cabecalhos_unificados) + 1)
                saida[0] = ano
                for indice, valor in enumerate(linha[: len(cabecalhos)]):
                    saida[posicoes_saida[cabecalhos[indice]]] = valor
                escritor.writerow(saida)
                linhas += 1
            totais[ano] = linhas
            print(f"Consolidado {ano}: {linhas:,} linhas", flush=True)

    return totais


def escrever_linguagens(layouts, caminho_saida: Path):
    contagens = Counter()
    respondentes_por_tipo = Counter()
    totais_ano = Counter()

    with caminho_saida.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, lineterminator="\n")
        escritor.writerow(["ano", "resposta_id", "tipo", "linguagem", "linguagem_original", "coluna_origem"])

        for ano, layout in layouts.items():
            caminho = layout["caminho"]
            cabecalhos = layout["cabecalhos"]
            colunas = layout["colunas_linguagens"]
            linhas = 0
            linhas_com_linguagem = Counter()

            for numero_linha, linha in enumerate(
                iterar_dados(caminho, layout["encoding"], layout["linhas_cabecalho"]), start=1
            ):
                if not any(limpar_texto(valor) for valor in linha):
                    continue
                linhas += 1
                resposta = id_resposta(ano, numero_linha, cabecalhos, linha)
                extraidas = extrair_linguagens_da_linha(linha, colunas)
                tipos_na_linha = set()

                for tipo, linguagem, linguagem_original, coluna_origem in extraidas:
                    escritor.writerow([ano, resposta, tipo, linguagem, linguagem_original, coluna_origem])
                    contagens[(ano, tipo, linguagem)] += 1
                    tipos_na_linha.add(tipo)

                for tipo in tipos_na_linha:
                    linhas_com_linguagem[tipo] += 1

            totais_ano[ano] = linhas
            for tipo, total in linhas_com_linguagem.items():
                respondentes_por_tipo[(ano, tipo)] = total
            print(f"Linguagens {ano}: {linhas:,} linhas lidas", flush=True)

    return totais_ano, respondentes_por_tipo, contagens


def escrever_resumo(
    caminho_saida: Path,
    totais_ano: Counter,
    respondentes_por_tipo: Counter,
    contagens: Counter,
) -> None:
    with caminho_saida.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, lineterminator="\n")
        escritor.writerow(
            [
                "ano",
                "tipo",
                "linguagem",
                "respondentes",
                "total_respostas_ano",
                "respondentes_com_linguagem_no_tipo",
                "percentual_sobre_total_respostas_ano",
                "percentual_sobre_respondentes_com_linguagem_no_tipo",
            ]
        )
        for (ano, tipo, linguagem), respondentes in sorted(contagens.items()):
            total_ano = totais_ano[ano]
            total_tipo = respondentes_por_tipo[(ano, tipo)]
            escritor.writerow(
                [
                    ano,
                    tipo,
                    linguagem,
                    respondentes,
                    total_ano,
                    total_tipo,
                    round(respondentes / total_ano, 6) if total_ano else "",
                    round(respondentes / total_tipo, 6) if total_tipo else "",
                ]
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consolida as pesquisas do Stack Overflow e gera uma base longa de linguagens por ano."
    )
    parser.add_argument("--dados-dir", default="dados", type=Path)
    parser.add_argument("--sem-consolidado", action="store_true", help="gera apenas os arquivos de linguagens")
    args = parser.parse_args()

    ajustar_limite_csv()
    dados_dir = args.dados_dir
    layouts, cabecalhos_unificados = preparar_layouts(dados_dir)

    if not layouts:
        raise SystemExit(f"Nenhum CSV de origem encontrado em {dados_dir}")

    saida_consolidada = dados_dir / "stackoverflow_2011_2025_consolidado.csv"
    saida_linguagens = dados_dir / "stackoverflow_linguagens_2011_2025_long.csv"
    saida_resumo = dados_dir / "stackoverflow_linguagens_2011_2025_resumo.csv"
    saida_mapeamento = dados_dir / "stackoverflow_linguagens_2011_2025_mapeamento_colunas.csv"

    escrever_mapeamento(layouts, saida_mapeamento)
    print(f"Mapeamento salvo em {saida_mapeamento}", flush=True)

    if not args.sem_consolidado:
        consolidar_bases(layouts, cabecalhos_unificados, saida_consolidada)
        print(f"Base consolidada salva em {saida_consolidada}", flush=True)

    totais_ano, respondentes_por_tipo, contagens = escrever_linguagens(layouts, saida_linguagens)
    escrever_resumo(saida_resumo, totais_ano, respondentes_por_tipo, contagens)

    print(f"Base longa de linguagens salva em {saida_linguagens}", flush=True)
    print(f"Resumo salvo em {saida_resumo}", flush=True)


if __name__ == "__main__":
    main()
