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



CREATE TABLE IF NOT EXISTS aparelho (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'Disponível'
);

CREATE TABLE IF NOT EXISTS exercicio (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    grupo_muscular VARCHAR(100) NOT NULL,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS exercicio_aparelho (
    exercicio_id INT REFERENCES exercicio(id) ON DELETE CASCADE,
    aparelho_id INT REFERENCES aparelho(id) ON DELETE CASCADE,
    PRIMARY KEY (exercicio_id, aparelho_id)
);

CREATE TABLE IF NOT EXISTS ficha_treino (
    id SERIAL PRIMARY KEY,
    aluno_id INT NOT NULL REFERENCES aluno(id) ON DELETE CASCADE,
    instrutor_id INT NOT NULL REFERENCES instrutor(id) ON DELETE RESTRICT,
    data_inicio DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    objetivo VARCHAR(150) NOT NULL,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS item_ficha (
    id SERIAL PRIMARY KEY,
    ficha_id INT NOT NULL REFERENCES ficha_treino(id) ON DELETE CASCADE,
    exercicio_id INT NOT NULL REFERENCES exercicio(id) ON DELETE RESTRICT,
    series INT NOT NULL,
    repeticoes VARCHAR(50) NOT NULL,
    carga VARCHAR(50),
    ordem INT NOT NULL,
    observacoes TEXT
);
