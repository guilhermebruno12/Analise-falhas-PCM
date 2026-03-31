import sqlite3
import pandas as pd

def conectar_banco():
    return sqlite3.connect("database/pcm.db")

def ordens_por_tipo():

    conn = conectar_banco()

    query = """
    SELECT tipo_manutencao, COUNT(*) as total
    FROM ordens
    GROUP BY tipo_manutencao
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    print("\nOrdens por tipo:\n")
    print(df)

def equipamentos_com_mais_falhas():

    conn = conectar_banco()

    query = """
    SELECT o.id_equipamento, COUNT(f.id_falha) as total_falhas
    FROM ordens o
    JOIN falhas f
    ON o.id_ordem = f.id_ordem
    GROUP BY o.id_equipamento
    ORDER BY total_falhas DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    print("\nEquipamentos com mais falhas:\n")
    print(df)

def tempo_total_parada():

    conn = conectar_banco()

    query = """
    SELECT o.id_equipamento, SUM(f.tempo_parada_h) as tempo_total
    FROM ordens o
    JOIN falhas f
    ON o.id_ordem = f.id_ordem
    GROUP BY o.id_equipamento
    ORDER BY tempo_total DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    print("\nTempo total de parada por equipamento:\n")
    print(df)

## MTTR - Mean Time To Repair (Tempo médio de reparo)
def calcular_mttr():

    conn = conectar_banco()

    query = """
    SELECT AVG(tempo_parada_h) as MTTR
    FROM falhas
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    print("\nMTTR (Tempo médio de reparo):\n")
    print(df)

def distribuicao_tipos_manutencao():

    conn = conectar_banco()

    query = """
    SELECT tipo_manutencao, COUNT(*) as total
    FROM ordens
    GROUP BY tipo_manutencao
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    print("\nDistribuição de tipos de manutenção:\n")
    print(df)

def ranking_falhas_equipamento():

    conn = conectar_banco()

    query = """
    SELECT e.nome, COUNT(f.id_falha) as total_falhas
    FROM equipamentos e
    JOIN ordens o ON e.id_equipamento = o.id_equipamento
    JOIN falhas f ON o.id_ordem = f.id_ordem
    GROUP BY e.nome
    ORDER BY total_falhas DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    print("\nRanking de falhas por equipamento:\n")
    print(df)

