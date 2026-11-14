CREATE DATABASE BolsaEleicoes;
GO

USE BolsaEleicoes;
GO

CREATE TABLE cotacoes_raw (
    fonte VARCHAR(100),
    ticker VARCHAR(10),
    grupo VARCHAR(50),
    evento_eleitoral VARCHAR(20),
    data_eleicao DATE,
    dias_para_eleicao INT,
    data DATE,
    abertura DECIMAL(18,4),
    maxima DECIMAL(18,4),
    minima DECIMAL(18,4),
    fechamento DECIMAL(18,4),
    fechamento_ajustado DECIMAL(18,4),
    volume BIGINT
);
GO

SELECT name
FROM sys.databases
ORDER BY name;
USE BolsaEleicoes;
GO
USE BolsaEleicoes;
GO

CREATE TABLE teste (
    id INT PRIMARY KEY,
    nome VARCHAR(100)
);
GO