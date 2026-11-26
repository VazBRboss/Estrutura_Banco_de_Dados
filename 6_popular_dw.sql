INSERT INTO dim_empresa
(
    ticker,
    grupo
)
SELECT DISTINCT
    ticker,
    grupo
FROM cotacoes_stg;
GO
INSERT INTO dim_evento
(
    evento_eleitoral,
    data_eleicao
)
SELECT DISTINCT
    evento_eleitoral,
    data_eleicao
FROM cotacoes_stg;
GO
INSERT INTO dim_tempo
(
    data,
    dia,
    mes,
    ano,
    trimestre,
    nome_mes
)
SELECT DISTINCT

    data_pregao,

    DAY(data_pregao),

    MONTH(data_pregao),

    YEAR(data_pregao),

    DATEPART(QUARTER, data_pregao),

    DATENAME(MONTH, data_pregao)

FROM cotacoes_stg;
GO
ALTER TABLE dim_evento
ADD ano_eleitoral INT;
UPDATE dim_evento
SET ano_eleitoral =
    LEFT(evento_eleitoral, 4);