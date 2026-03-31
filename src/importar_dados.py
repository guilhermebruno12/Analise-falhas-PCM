import pandas as pd
import sqlite3

# conexão com banco
conn = sqlite3.connect("database/pcm.db")

# carregar arquivos CSV
equipamentos = pd.read_csv("data/equipamentos.csv", sep=',', skipinitialspace=True)
ordens = pd.read_csv("data/ordens.csv", sep=',', skipinitialspace=True)
ordens.columns = ordens.columns.str.strip()
falhas = pd.read_csv("data/falhas.csv", sep=',', skipinitialspace=True)

# inserir dados nas tabelas
equipamentos.to_sql("equipamentos", conn, if_exists="replace", index=False)
ordens.to_sql("ordens", conn, if_exists="replace", index=False)
falhas.to_sql("falhas", conn, if_exists="replace", index=False)

conn.close()

print("Dados importados com sucesso.")