import sqlite3

conn = sqlite3.connect("database/pcm.db")
cursor = conn.cursor()

with open("database/setup_banco.sql", "r") as f:
    sql_script = f.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Banco criado com sucesso.")