-- ============================================================
-- Schema PostgreSQL
-- Substitui: Azure SQL Database
-- Economia: ~R$ 1.740/mês
-- ============================================================

-- Tabela de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefone VARCHAR(20),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

-- Tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    preco DECIMAL(10,2) NOT NULL,
    estoque INTEGER DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de vendas
CREATE TABLE IF NOT EXISTS vendas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(id),
    produto_id INTEGER REFERENCES produtos(id),
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    valor_total DECIMAL(10,2) GENERATED ALWAYS AS (quantidade * valor_unitario) STORED,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'concluida'
);

-- Tabela de despesas
CREATE TABLE IF NOT EXISTS despesas (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL,
    categoria VARCHAR(100),
    valor DECIMAL(10,2) NOT NULL,
    data_despesa DATE NOT NULL,
    departamento VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data_venda);
CREATE INDEX IF NOT EXISTS idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_produto ON vendas(produto_id);
CREATE INDEX IF NOT EXISTS idx_despesas_data ON despesas(data_despesa);

-- Views analíticas (substituem measures do Power BI)
CREATE OR REPLACE VIEW vw_vendas_mensais AS
SELECT
    DATE_TRUNC('month', data_venda) AS mes,
    COUNT(*) AS total_vendas,
    SUM(valor_total) AS receita_total,
    AVG(valor_total) AS ticket_medio
FROM vendas
WHERE status = 'concluida'
GROUP BY DATE_TRUNC('month', data_venda)
ORDER BY mes DESC;

CREATE OR REPLACE VIEW vw_vendas_por_produto AS
SELECT
    p.nome AS produto,
    p.categoria,
    COUNT(v.id) AS total_vendas,
    SUM(v.quantidade) AS quantidade_vendida,
    SUM(v.valor_total) AS receita_total
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
WHERE v.status = 'concluida'
GROUP BY p.nome, p.categoria
ORDER BY receita_total DESC;

CREATE OR REPLACE VIEW vw_despesas_mensais AS
SELECT
    DATE_TRUNC('month', data_despesa) AS mes,
    categoria,
    departamento,
    SUM(valor) AS total_despesas,
    COUNT(*) AS num_despesas
FROM despesas
GROUP BY DATE_TRUNC('month', data_despesa), categoria, departamento
ORDER BY mes DESC;
