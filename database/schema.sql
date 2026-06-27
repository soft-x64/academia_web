-- database/schema.sql

CREATE TABLE IF NOT EXISTS instrutor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    cref VARCHAR(20) UNIQUE NOT NULL,
    especialidade VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    peso NUMERIC(5,2),
    altura NUMERIC(3,2)
);

CREATE TABLE IF NOT EXISTS avaliacao_fisica (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL,
    data_avaliacao DATE NOT NULL,
    peso NUMERIC(5,2) NOT NULL,
    percentual_gordura NUMERIC(5,2),
    observacoes TEXT,

    CONSTRAINT fk_avaliacao_aluno
        FOREIGN KEY (aluno_id)
        REFERENCES aluno(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_peso_positivo
        CHECK (peso > 0),

    CONSTRAINT chk_percentual_gordura
        CHECK (
            percentual_gordura IS NULL 
            OR percentual_gordura BETWEEN 0 AND 100
        )
);