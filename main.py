import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

conexao = sqlite3.connect("bancos/pesquisa.db")
cursor = conexao.cursor()

cursor.execute(
  """
  SELECT HaveWorkedLanguage, Salary
  FROM pesquisa_2017
  WHERE Salary > 10000
  """
)

resultado = cursor.fetchall()

for linha in resultado:
  print(linha)


