PRAGMA foreign_keys = ON;

-- ==========================
-- CLIENTES
-- ==========================
CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    cpf TEXT,
    endereco TEXT,
    observacoes TEXT
);


-- ==========================
-- VEÍCULOS
-- ==========================
CREATE TABLE veiculos (
    id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    placa TEXT NOT NULL UNIQUE,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    ano INTEGER,
    cor TEXT,
    km INTEGER DEFAULT 0,
    motor TEXT,
    combustivel TEXT,

    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
);

-- ==========================
-- SERVIÇOS
-- ==========================
CREATE TABLE servicos (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor_padrao REAL NOT NULL DEFAULT 0,
    observacoes TEXT
);

-- ==========================
-- PEÇAS
-- ==========================
CREATE TABLE pecas (
    id_peca INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    marca TEXT,
    valor REAL NOT NULL DEFAULT 0
);

-- ==========================
-- ORDENS DE SERVIÇO
-- ==========================
CREATE TABLE ordens_servico (
    id_os INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_os INTEGER NOT NULL UNIQUE,
    cliente_id INTEGER NOT NULL,
    veiculo_id INTEGER NOT NULL,
    data_abertura TEXT NOT NULL,
    data_fechamento TEXT,
    problema_relatado TEXT NOT NULL,
    diagnostico TEXT,
    valor_mao_obra REAL NOT NULL DEFAULT 0,
    valor_pecas REAL NOT NULL DEFAULT 0,
    valor_total REAL NOT NULL DEFAULT 0,
    forma_pagamento TEXT,
    status TEXT NOT NULL DEFAULT 'Aberta'
        CHECK(status IN (
            'Aberta',
            'Em andamento',
            'Finalizada',
            'Entregue',
            'Cancelada'
        )),
    observacoes TEXT,
    FOREIGN KEY(cliente_id)
        REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT,
    FOREIGN KEY(veiculo_id)
        REFERENCES veiculos(id_veiculo)
        ON DELETE RESTRICT
);


-- ==========================
-- ITENS DE SERVIÇO
-- ==========================
CREATE TABLE itens_servico (
    id_item_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    os_id INTEGER NOT NULL,
    servico_id INTEGER NOT NULL,
    quantidade REAL NOT NULL DEFAULT 1,
    valor_unitario REAL NOT NULL,
    valor_total REAL NOT NULL,

    FOREIGN KEY(os_id)
        REFERENCES ordens_servico(id_os)
        ON DELETE CASCADE,

    FOREIGN KEY(servico_id)
        REFERENCES servicos(id_servico)
);

-- ==========================
-- ITENS DE PEÇAS
-- ==========================
CREATE TABLE itens_peca (
    id_item_peca INTEGER PRIMARY KEY AUTOINCREMENT,
    os_id INTEGER NOT NULL,
    peca_id INTEGER NOT NULL,

    quantidade REAL NOT NULL DEFAULT 1,
    valor_unitario REAL NOT NULL,
    valor_total REAL NOT NULL,

    FOREIGN KEY(os_id)
        REFERENCES ordens_servico(id_os)
        ON DELETE CASCADE,

    FOREIGN KEY(peca_id)
        REFERENCES pecas(id_peca)
);

-- ==========================
-- CONFIGURAÇÕES
-- ==========================
CREATE TABLE configuracoes (
    id_configuracao INTEGER PRIMARY KEY CHECK(id_configuracao = 1),

    nome_oficina TEXT NOT NULL,
    cnpj TEXT,
    telefone TEXT,
    endereco TEXT,
    cidade TEXT,
    estado TEXT,
    email TEXT,
    logo TEXT
);

INSERT INTO configuracoes (
    id_configuracao,
    nome_oficina
)
VALUES (
    1,
    'EWE Multimarcas'
);

-- ==========================
-- ÍNDICES
-- ==========================
CREATE INDEX idx_clientes_nome
ON clientes(nome);

CREATE INDEX idx_ordens_servico_status
ON ordens_servico(status);

CREATE INDEX idx_ordens_servico_data
ON ordens_servico(data_abertura);