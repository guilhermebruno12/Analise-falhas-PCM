"""
Checklist de qualidade de dados pro projeto PCM. Roda antes de qualquer
atualização no dashboard/portfólio, pra pegar os mesmos tipos de problema
que motivaram a revisão de 2026: PK duplicada/typo, FK órfã, CHECK
violado, status inconsistente com as datas.

Uso: python tests/validar_integridade.py
Sai com código 0 se tudo passar, 1 se achar algum problema (pra plugar
em CI depois, se quiser).
"""

import sys
import pandas as pd

ERROS = []


def checar(condicao, mensagem):
    if not condicao:
        ERROS.append(mensagem)


def main():
    eq = pd.read_csv("data/equipamentos.csv")
    ordens = pd.read_csv("data/ordens.csv")
    falhas = pd.read_csv("data/falhas.csv")

    # 1. PK duplicada ou com espaço/typo óbvio (dois dígitos a mais)
    checar(eq["id_equipamento"].is_unique, "PK duplicada em equipamentos.csv")
    checar(ordens["id_ordem"].is_unique, "PK duplicada em ordens.csv")
    checar(falhas["id_falha"].is_unique, "PK duplicada em falhas.csv")

    # 2. FK órfã: toda ordem precisa apontar pra um equipamento existente
    orfas_ordens = ordens[~ordens["id_equipamento"].isin(eq["id_equipamento"])]
    checar(len(orfas_ordens) == 0,
           f"ordens.csv com id_equipamento inexistente: {orfas_ordens['id_ordem'].tolist()}")

    # 3. FK órfã: toda falha precisa apontar pra uma ordem existente
    orfas_falhas = falhas[~falhas["id_ordem"].isin(ordens["id_ordem"])]
    checar(len(orfas_falhas) == 0,
           f"falhas.csv com id_ordem inexistente: {orfas_falhas['id_ordem'].tolist()}")

    # 4. falhas.csv só pode conter ordens do tipo corretiva
    f_check = falhas.merge(ordens[["id_ordem", "tipo_manutencao", "status"]], on="id_ordem", how="left")
    nao_corretiva = f_check[f_check["tipo_manutencao"] != "corretiva"]
    checar(len(nao_corretiva) == 0,
           f"falhas.csv com ordem não-corretiva: {nao_corretiva['id_ordem'].tolist()}")

    # 5. falhas.csv só pode conter ordens já concluídas (reparo finalizado)
    nao_concluida = f_check[f_check["status"] != "concluída"]
    checar(len(nao_concluida) == 0,
           f"falhas.csv com ordem ainda não concluída: {nao_concluida['id_ordem'].tolist()}")

    # 6. tempo_parada_h precisa ser sempre > 0 (CHECK do schema)
    zerados = falhas[falhas["tempo_parada_h"] <= 0]
    checar(len(zerados) == 0,
           f"falhas.csv com tempo_parada_h <= 0: {zerados['id_falha'].tolist()}")

    # 7. status "em andamento" não pode ter data_fim preenchida
    inconsistentes = ordens[(ordens["status"] == "em andamento") & (ordens["data_fim"].notna())]
    checar(len(inconsistentes) == 0,
           f"ordens 'em andamento' com data_fim preenchida: {inconsistentes['id_ordem'].tolist()}")

    # 8. data_fim não pode ser anterior a data_inicio (quando ambas existem)
    ordens_com_datas = ordens.dropna(subset=["data_fim"]).copy()
    ordens_com_datas["data_inicio"] = pd.to_datetime(ordens_com_datas["data_inicio"])
    ordens_com_datas["data_fim"] = pd.to_datetime(ordens_com_datas["data_fim"])
    fora_de_ordem = ordens_com_datas[ordens_com_datas["data_fim"] < ordens_com_datas["data_inicio"]]
    checar(len(fora_de_ordem) == 0,
           f"ordens com data_fim antes de data_inicio: {fora_de_ordem['id_ordem'].tolist()}")

    if ERROS:
        print(f"[FALHOU] {len(ERROS)} problema(s) encontrado(s):")
        for e in ERROS:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("[OK] Todas as checagens de integridade passaram.")
        sys.exit(0)


if __name__ == "__main__":
    main()
