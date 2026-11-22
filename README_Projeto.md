# Projeto - Análise da Bolsa Brasileira em Períodos Eleitorais

## Objetivo

Avaliar o comportamento de ações da B3 durante períodos eleitorais brasileiros.

---

# Empresas Analisadas

## Financeiro

- ITUB4
- BBAS3
- BBDC4
- SANB11

## Petróleo e Gás

- PETR3
- PETR4
- PRIO3
- BRAV3
- RECV3

## Energia Elétrica

- ELET3
- ELET6
- EGIE3
- CPFE3
- ISAE4

## Varejo

- MGLU3
- LREN3
- MELI34
- SOMA3

## Construção Civil

- CYRE3
- MRVE3
- DIRR3
- EZTC3

---

# Arquitetura

## Coleta

Python + Yahoo Finance

↓

cotacoes_eleicoes.csv

## Ingestão

Python + SQL Server

↓

cotacoes_raw

## ETL

SQL Server

↓

cotacoes_stg

## Data Warehouse

Modelo Estrela

↓

Power BI

---

# Justificativa do ETL

Foi adotada uma camada STAGING para:

- Preservar os dados originais.
- Realizar transformações controladas.
- Calcular indicadores analíticos.
- Separar carga de análise.

---

# Justificativa do Modelo Estrela

O modelo estrela foi escolhido por:

- Melhor desempenho analítico.
- Facilidade de uso no Power BI.
- Simplicidade dos relacionamentos.
- Baixa complexidade de manutenção.

---

# Estrutura do DW

## Dimensões

### dim_empresa

Informações das empresas e segmentos.

### dim_evento

Informações dos eventos eleitorais.

### dim_tempo

Informações temporais.

---

## Fato

### fato_cotacao

Métricas observáveis:

- Fechamento
- Volume
- Retorno Diário

---

# ETLs Implementados

## RAW → STG

Transformações:

- Ano
- Mês
- Trimestre
- Retorno Diário

---

## STG → DW

População de:

- dim_empresa
- dim_evento
- dim_tempo
- fato_cotacao

---

# Power BI

## Filtros

### Ano Eleitoral

Slicer tipo Between.

### Segmento

Slicer com seleção múltipla.

---

# Indicadores

## Retorno Médio

```DAX
Retorno Médio =
AVERAGE(
    fato_cotacao[retorno_diario]
)
```

## Volume Médio

```DAX
Volume Médio =
AVERAGE(
    fato_cotacao[volume]
)
```

## Quantidade de Empresas

```DAX
Qtd Empresas =
DISTINCTCOUNT(
    dim_empresa[ticker]
)
```

## Quantidade de Eventos

```DAX
Qtd Eventos =
DISTINCTCOUNT(
    dim_evento[evento_eleitoral]
)
```

---

# Resultado Esperado

Identificar padrões do mercado brasileiro durante eleições e comparar o comportamento dos setores:

- Financeiro
- Petróleo e Gás
- Energia Elétrica
- Varejo
- Construção Civil