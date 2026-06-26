-- database/schema.sql

CREATE TABLE IF NOT EXISTS instrutor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    cref VARCHAR(20) NOT NULL,
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