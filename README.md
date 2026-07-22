# Análise de Dados de Manutenção (PCM)

Este projeto tem como finalidade simular a análise de dados de manutenção industrial, com foco em Planejamento e Controle de Manutenção (PCM).

Ele foi desenvolvido com base na minha experiência inicial em programação e no meu contato com o ambiente industrial, buscando aplicar conceitos de Análise de Dados Industriais em um contexto próximo da realidade. O projeto passou por uma **revisão metodológica** após uma auditoria de integridade dos dados — os detalhes estão na seção "Evolução do Projeto", abaixo.

## O objetivo principal é:

- Estruturar um banco de dados de manutenção
- Realizar análises utilizando Python e SQL
- Gerar indicadores relevantes para o setor de manutenção
- Criar uma base para visualização em ferramentas de BI

## Os dados utilizados neste projeto são 100% fictícios, criados com base na minha experiência de trabalho, apenas para fins de estudo e desenvolvimento de portfólio.

Apesar disso, a estrutura foi pensada para se aproximar de um cenário real de indústria, incluindo:

- equipamentos
- ordens de manutenção
- falhas operacionais

## Tecnologias Utilizadas

- Python
- SQLite
- Pandas
- SQL

## Indicadores Desenvolvidos

- Total de ordens de manutenção
- Distribuição por tipo de manutenção (preventiva, corretiva, etc.)
- Equipamentos com maior número de falhas
- Tempo total de parada por equipamento
- MTTR (Mean Time To Repair)

## Evolução do Projeto

A primeira versão deste projeto tinha um problema silencioso: o cálculo de MTTR
misturava ordens de inspeção, preventiva e preditiva na mesma tabela de falhas,
além de conter um typo de chave primária e uma chave estrangeira órfã — erros que
o SQLite não acusa, mas que quebram silenciosamente os `JOIN`s dos indicadores.

Uma auditoria de integridade posterior identificou:

- **Typo de PK** (`EQ0280` em vez de `EQ028`) e uma **FK órfã** (`EQ016`
  referenciado em ordens de manutenção, mas nunca cadastrado) — ambos quebravam
  os `JOIN`s de `ranking_falhas_equipamento()` e `equipamentos_com_mais_falhas()`.
- **Regra de povoamento da tabela `falhas` inconsistente**: qualquer tipo de
  ordem podia gerar uma linha, inclusive com `tempo_parada_h = 0` para
  inspeções e preventivas — o que inflava artificialmente a base de cálculo do
  MTTR com eventos que não eram falhas reais.
- **Lacuna de 34% nas ordens corretivas**: 34 das 99 ordens simplesmente não
  tinham registro correspondente em `falhas.csv`, concentradas no fim da
  linha do tempo — um viés silencioso, não uma amostra aleatória.
- **9 ordens com status "em andamento" e `data_fim` já preenchida** —
  inconsistência lógica que também afetava quais ordens deveriam ou não
  gerar um registro de falha "concluída".

### Correções aplicadas

- Schema da tabela `falhas` restrito a ordens **corretivas e concluídas**,
  com `CHECK (tempo_parada_h > 0)` para impedir a reintrodução do problema.
- Chave primária corrigida e equipamento órfão cadastrado.
- Tabela `falhas` repovoada cobrindo as 99 ordens corretamente.
- `data_fim` das 9 ordens inconsistentes tratada como valor ainda não
  preenchido (reparo em andamento, sem data de conclusão real).
- Script `tests/validar_integridade.py` adicionado para checagem contínua de
  PK duplicada, FK órfã, violação de `CHECK` e inconsistência de status —
  roda antes de qualquer atualização futura no dataset.

### Impacto no indicador

| Cálculo | MTTR |
| --- | --- |
| Ingênuo (mistura todos os tipos de ordem) | 1.72h |
| Filtrando só por tipo corretiva (sem tratar os demais problemas) | 1.46h |
| **Corrigido (corretiva + concluída + integridade validada)** | **2.88h** |

O salto de 1.72h para 2.88h — e não uma simples correção de décimos — mostra
que o problema original não era só "mistura de tipos de ordem": era a
integridade dos dados como um todo. É esse o motivo pelo qual uma auditoria de
qualidade de dados deveria vir *antes* de qualquer dashboard, não depois.

A branch `fix/mttr-e-integridade-referencial` documenta o histórico completo
dessa correção.

## Projeto desenvolvido como parte do meu processo de aprendizado em:

- Análise de Dados
- Python
- Banco de Dados
- Aplicações no setor industrial
