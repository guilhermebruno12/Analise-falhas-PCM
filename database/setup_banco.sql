-- tabela de equipamentos
CREATE TABLE IF NOT EXISTS equipamentos (
    id_equipamento TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    setor TEXT,
    criticidade TEXT
);

-- tabela de ordens de manutenção
CREATE TABLE IF NOT EXISTS ordens (
    id_ordem TEXT PRIMARY KEY,
    id_equipamento TEXT,
    tipo_manutencao TEXT,
    data_inicio DATE,
    data_fim DATE,
    status TEXT,
    FOREIGN KEY (id_equipamento) REFERENCES equipamentos(id_equipamento)
);

-- tabela de falhas (registra SOMENTE eventos de manutenção corretiva --
-- ou seja, falhas reais que pararam o equipamento de forma não planejada
-- e já foram resolvidas. Ordens de inspeção/preventiva/preditiva não geram
-- linha aqui, e uma corretiva só entra depois de concluída, com o tempo
-- de parada definitivo)
CREATE TABLE IF NOT EXISTS falhas (
    id_falha TEXT PRIMARY KEY,
    id_ordem TEXT,
    causa_raiz TEXT,
    tempo_parada_h REAL NOT NULL CHECK (tempo_parada_h > 0),
    FOREIGN KEY (id_ordem) REFERENCES ordens(id_ordem)
);
