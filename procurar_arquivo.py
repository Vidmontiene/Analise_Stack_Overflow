import csv
from pathlib import Path

nome_coluna = "DatabaseAdmired"

def colher_arquivos(nome_coluna):
  csv_files = sorted(Path("Dados").glob("*.csv"))
  csv_files_with_column = []

  for csv_file in csv_files:
    with csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
      reader = csv.reader(handle)
      try:
        headers = next(reader)
      except StopIteration:
        continue

      if nome_coluna in headers:
        csv_files_with_column.append(csv_file)

    return csv_files_with_column
  