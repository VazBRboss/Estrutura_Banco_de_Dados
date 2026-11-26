CREATE TABLE cotacoes_stg (
    id_stg INT IDENTITY(1,1) PRIMARY KEY,

    ticker VARCHAR(10),
    grupo VARCHAR(50),

    evento_eleitoral VARCHAR(20),
    data_eleicao DATE,

    dias_para_eleicao INT,
    data_pregao DATE,

    abertura DECIMAL(18,4),
    maxima DECIMAL(18,4),
    minima DECIMAL(18,4),
    fechamento DECIMAL(18,4),
    volume BIGINT,

    retorno_diario DECIMAL(18,6),

    ano INT,
    mes INT,
    trimestre INT
);
GO

INSERT INTO cotacoes_stg
(
    ticker,
    grupo,
    evento_eleitoral,
    data_eleicao,
    dias_para_eleicao,
    data_pregao,
    abertura,
    maxima,
    minima,
    fechamento,
    volume,
    retorno_diario,
    ano,
    mes,
    trimestre
)

SELECT

    ticker,
    grupo,

    evento_eleitoral,
    data_eleicao,

    dias_para_eleicao,

    data,

    abertura,
    maxima,
    minima,
    fechamento,

    volume,

    ROUND(
        (
            fechamento -
            LAG(fechamento) OVER(
                PARTITION BY
                    ticker,
                    evento_eleitoral
                ORDER BY data
            )
        )
        /
        NULLIF(
            LAG(fechamento) OVER(
                PARTITION BY
                    ticker,
                    evento_eleitoral
                ORDER BY data
            ),
            0
        )
        * 100,
        6
    ) AS retorno_diario,

    YEAR(data),

    MONTH(data),

    DATEPART(
        QUARTER,
        data
    )

FROM cotacoes_raw;