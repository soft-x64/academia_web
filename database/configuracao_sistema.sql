CREATE TABLE IF NOT EXISTS configuracao_sistema (
    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    nome_academia VARCHAR(120) NOT NULL DEFAULT 'TrainerX64',
    cnpj VARCHAR(20),
    telefone VARCHAR(30),
    endereco TEXT,
    alertas_fichas_vencidas BOOLEAN NOT NULL DEFAULT TRUE,
    mostrar_manutencao_dashboard BOOLEAN NOT NULL DEFAULT TRUE,
    relatorio_semanal_email BOOLEAN NOT NULL DEFAULT FALSE,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO configuracao_sistema (
    id,
    nome_academia,
    cnpj,
    telefone,
    endereco,
    alertas_fichas_vencidas,
    mostrar_manutencao_dashboard,
    relatorio_semanal_email
)
VALUES (
    1,
    'TrainerX64',
    '00.000.000/0001-00',
    '(92) 99999-9999',
    'Itacoatiara/AM',
    TRUE,
    TRUE,
    FALSE
)
ON CONFLICT (id) DO NOTHING;