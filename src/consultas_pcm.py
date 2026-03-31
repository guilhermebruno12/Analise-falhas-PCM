import sqlite3
import pandas as pd

def mostrar_equipamentos():

    conn = sqlite3.connect("database/pcm.db")

    query = "SELECT * FROM equipamentos"

    df = pd.read_sql_query(query, conn)

    print("\nEquipamentos cadastrados:\n")
    print(df)

    conn.close()