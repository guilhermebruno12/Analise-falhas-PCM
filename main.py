from src.indicadores_pcm import (
    ordens_por_tipo,
    equipamentos_com_mais_falhas,
    tempo_total_parada,
    calcular_mttr,
    distribuicao_tipos_manutencao,
    ranking_falhas_equipamento
)

import sqlite3
import pandas as pd


def mostrar_equipamentos():

    conn = sqlite3.connect("database/pcm.db")

    query = "SELECT * FROM equipamentos"

    df = pd.read_sql_query(query, conn)

    print("\nEquipamentos cadastrados:\n")
    print(df)

    conn.close()


def main():

    print("\nSistema de Análise de Manutenção (PCM)\n")

    # mostrar equipamentos cadastrados
    mostrar_equipamentos()

    # indicadores de manutenção
    print("\nIndicadores de Manutenção\n")

    ordens_por_tipo()
    distribuicao_tipos_manutencao()
    equipamentos_com_mais_falhas()
    ranking_falhas_equipamento()
    tempo_total_parada()
    calcular_mttr()


if __name__ == "__main__":
    main()