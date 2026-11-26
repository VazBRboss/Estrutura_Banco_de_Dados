USE BolsaEleicoes;
GO

/* ==========================
   DIM_EMPRESA
   ========================== */

CREATE TABLE dim_empresa
(
    id_empresa INT IDENTITY(1,1) PRIMARY KEY,

    ticker VARCHAR(10) NOT NULL,

    grupo VARCHAR(50) NOT NULL
);
GO


/* ==========================
   DIM_EVENTO
   ========================== */

CREATE TABLE dim_evento
(
    id_evento INT IDENTITY(1,1) PRIMARY KEY,

    evento_eleitoral VARCHAR(20) NOT NULL,

    data_eleicao DATE NOT NULL
);
GO


/* ==========================
   DIM_TEMPO
   ========================== */

CREATE TABLE dim_tempo
(
    id_tempo INT IDENTITY(1,1) PRIMARY KEY,

    data DATE NOT NULL,

    dia INT NOT NULL,

    mes INT NOT NULL,

    ano INT NOT NULL,

    trimestre INT NOT NULL,

    nome_mes VARCHAR(20)
);
GO


/* ==========================
   FATO_COTACAO
   ========================== */

CREATE TABLE fato_cotacao
(
    id_fato BIGINT IDENTITY(1,1) PRIMARY KEY,

    id_empresa INT NOT NULL,

    id_evento INT NOT NULL,

    id_tempo INT NOT NULL,

    dias_para_eleicao INT,

    fechamento DECIMAL(18,4),

    volume BIGINT,

    retorno_diario DECIMAL(18,6),

    CONSTRAINT FK_FATO_EMPRESA
        FOREIGN KEY(id_empresa)
        REFERENCES dim_empresa(id_empresa),

    CONSTRAINT FK_FATO_EVENTO
        FOREIGN KEY(id_evento)
        REFERENCES dim_evento(id_evento),

    CONSTRAINT FK_FATO_TEMPO
        FOREIGN KEY(id_tempo)
        REFERENCES dim_tempo(id_tempo)
);
GO