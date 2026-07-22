PRAGMA foreign_keys = ON;

-- ==========================
-- CLIENTES
-- ==========================
CREATE TABLE Clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    cpf TEXT,
    endereco TEXT,
    observacoes TEXT
);

-- ==========================
-- VEICULOS
-- ==========================
CREATE TABLE Veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        REFERENCES Clientes(id)
        ON DELETE CASCADE
);

-- ==========================
-- SERVICOS
-- ==========================
CREATE TABLE Servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor_padrao REAL NOT NULL DEFAULT 0
);

-- ==========================
-- PECAS
-- ==========================
CREATE TABLE Pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    marca TEXT,
    valor REAL NOT NULL DEFAULT 0
);

-- ==========================
-- ORDENS DE SERVIÇO
-- ==========================
CREATE TABLE OrdensServico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,

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
        REFERENCES Clientes(id),

    FOREIGN KEY(veiculo_id)
        REFERENCES Veiculos(id)
);

-- ==========================
-- ITENS DE SERVIÇO
-- ==========================
CREATE TABLE ItensServico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    os_id INTEGER NOT NULL,
    servico_id INTEGER NOT NULL,

    quantidade REAL NOT NULL DEFAULT 1,
    valor_unitario REAL NOT NULL,
    valor_total REAL NOT NULL,

    FOREIGN KEY(os_id)
        REFERENCES OrdensServico(id)
        ON DELETE CASCADE,

    FOREIGN KEY(servico_id)
        REFERENCES Servicos(id)
);

-- ==========================
-- ITENS DE PEÇAS
-- ==========================
CREATE TABLE ItensPeca (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    os_id INTEGER NOT NULL,
    peca_id INTEGER NOT NULL,

    quantidade REAL NOT NULL DEFAULT 1,
    valor_unitario REAL NOT NULL,
    valor_total REAL NOT NULL,

    FOREIGN KEY(os_id)
        REFERENCES OrdensServico(id)
        ON DELETE CASCADE,

    FOREIGN KEY(peca_id)
        REFERENCES Pecas(id)
);

-- ==========================
-- CONFIGURAÇÕES
-- ==========================
CREATE TABLE Configuracoes (
    id INTEGER PRIMARY KEY CHECK (id = 1),

    nome_oficina TEXT NOT NULL,
    cnpj TEXT,
    telefone TEXT,
    endereco TEXT,
    cidade TEXT,
    estado TEXT,
    email TEXT,
    logo TEXT
);

INSERT INTO Configuracoes (
    id,
    nome_oficina
)
VALUES (
    1,
    'EWE Multimarcas'
);

-- ==========================
-- ÍNDICES
-- ==========================
CREATE INDEX idx_cliente_nome
ON Clientes(nome);

CREATE INDEX idx_os_status
ON OrdensServico(status);

CREATE INDEX idx_os_data
ON OrdensServico(data_abertura);