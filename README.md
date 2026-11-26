Estrutura\_Banco\_de\_Dados

Used for final project from Estrutura de Banco de Dados - project that will use data from API B3 to get how the elections periods affect brasilian companies.

We will use the https://dadosb3.com/empresas/WEGE3/indicadores and Https://www.yahoofinanceapi.com some others Endpoints.

## 0. Como as APIs financeiras não eram gratuítas e as poucas que eram tinham limite de aquisição usamos o plugin do VSCode Chamado "yfinance" que conecta a api do Yahoo.  Mas há um script de aquisição e uma aquisição semelhante no repositório



\##1. Contextualização

O Mercado financeiro do brasil sofre uma mudança significativa a cada grande evento dentro do nosso cenário.

Este projeto analisa o comportamento do mercado de capitais brasileiro ao longo dos últimos quatro ciclos eleitorais.



\##2. Metodologia e Segmentação

Selecionaremos os 3 ou 4 ativos mais impactantes dentro de Comodites, Varejo e Estatais. E avaliaremos como nas últimas eleições estes indicadores foram afetados em pontos percentuais, em como se comportaram durante o primeiro e segundo turno se caso aplicável e como esse comportamento foi afetado por eleições diretas.



\##3. Fonte de Dados:



API Dados B3, Yahoo Finance API e Tribunal Superior Eleitoral do TSE para que tenha os marcadores dasdatas.



\##4. Coleta de dados: Rest da API e biblioteca Yahoo otimizada para download. PANDAS, NUMPY, SCIPY/STATSMODELS.



\##5. Visualização Usaremos Full .html com ploty \[API Dados B3 + yfinance] ──> \[pandas / numpy] ──> \[Plotly (Python)] ──> \[Arquivo .html Interativo] (Coleta de Dados) (Tratamento e Estatística) (Mecanismo de Renderização) (Artefato Final / Dashboard)

# Iniciando sua Operação
## 1. Preparação de Ambientes:  

Instale a biblioteca para acessar os dados em Json:  

python -m pip install requests
python -m pip install --upgrade yfinance pandas
python -m pip install pyodbc

# Projeto: Análise do Comportamento da Bolsa Brasileira em Períodos Eleitorais

## Objetivo

Este projeto tem como objetivo analisar o comportamento de empresas listadas na B3 durante períodos eleitorais brasileiros.

Os segmentos analisados são:

- Financeiro
- Petróleo, Gás e Biocombustíveis
- Energia Elétrica
- Varejo
- Construção Civil

A solução utiliza:

- Python para coleta e ingestão dos dados
- SQL Server para armazenamento e ETL
- Power BI para visualização e análise

---

# Estrutura do Projeto

```text
Estrutura_Banco_de_Dados-main
│
├── 1_consulta_b3.py
├── 2_CreateDB.sql
├── 3_Ingestão_dados.py
├── 4_DBStgETL.sql
├── 5_Create_dw.sql
├── 6_popular_dw.sql
│
├── cotacoes_eleicoes.csv
├── avisos_coleta.csv
│
├── Separação_colunas.py
└── README.md
```

---

# Pré-Requisitos

## SQL Server

Instalar:

- SQL Server Express
- SQL Server Management Studio (SSMS)

---

## Python

Versão recomendada:

```text
Python 3.12+
```

---

## Bibliotecas Python

Executar:

```bash
pip install pandas
pip install pyodbc
pip install yfinance
```

---

# Ordem de Execução

A execução deve seguir exatamente a seguinte ordem:

```text
1) 2_CreateDB.sql
2) 3_Ingestão_dados.py
3) 4_DBStgETL.sql
4) 5_Create_dw.sql
5) 6_popular_dw.sql
6) Power BI
```

---

# Passo 1 - Criar Banco de Dados

Abrir o SQL Server Management Studio (SSMS).

Executar:

```sql
2_CreateDB.sql
```

Este script cria:

- Banco de Dados BolsaEleicoes
- Tabela de carga inicial (RAW)

Após a execução validar:

```sql
SELECT DB_NAME();
```

---

# Passo 2 - Configurar a Conexão com SQL Server

Descobrir o nome da instância:

```sql
SELECT @@SERVERNAME;
```

Exemplo:

```text
DESKTOP-R8C4SUV\SQLEXPRESS
```

Abrir:

```text
3_Ingestão_dados.py
```

Verificar a variável:

```python
SERVIDOR = r"DESKTOP-R8C4SUV\SQLEXPRESS"
```

Caso a instância seja diferente, substituir pelo nome encontrado.

---

# Passo 3 - Realizar a Ingestão do CSV

Executar:

```bash
python 3_Ingestão_dados.py
```

O script realiza:

- Leitura do arquivo CSV
- Validação das colunas
- Conexão com SQL Server
- Carga dos dados para a tabela RAW

Arquivo utilizado:

```text
cotacoes_eleicoes.csv
```

---

# Passo 4 - Validar a Quantidade de Registros

No SSMS executar:

```sql
USE BolsaEleicoes;
GO

SELECT COUNT(*) AS TotalRegistros
FROM cotacoes_raw;
```

Também é possível visualizar algumas linhas:

```sql
SELECT TOP 20 *
FROM cotacoes_raw;
```

---

# Passo 5 - Executar o ETL para Staging

Executar:

```sql
4_DBStgETL.sql
```

Este script:

- Cria a tabela STG
- Move os dados da RAW para STG
- Calcula retorno diário
- Calcula atributos de tempo
- Prepara os dados para o Data Warehouse

---

# Passo 6 - Criar o Data Warehouse

Executar:

```sql
5_Create_dw.sql
```

Serão criadas as tabelas:

```text
dim_empresa
dim_evento
dim_tempo
fato_cotacao
```

---

# Passo 7 - Popular o Data Warehouse

Executar:

```sql
6_popular_dw.sql
```

Este script:

- Popula dim_empresa
- Popula dim_evento
- Popula dim_tempo
- Popula fato_cotacao

---

# Validações

## Empresas

```sql
SELECT *
FROM dim_empresa
ORDER BY grupo,ticker;
```

---

## Eventos Eleitorais

```sql
SELECT *
FROM dim_evento
ORDER BY data_eleicao;
```

Eventos esperados:

```text
2014_1T
2014_2T
2018_1T
2018_2T
2022_1T
2022_2T
2026_1T
2026_2T
```

---

## Tabela Fato

```sql
SELECT COUNT(*)
FROM fato_cotacao;
```

Deve retornar milhares de registros.

---

# Conectar ao Power BI

Abrir:

```text
Power BI Desktop
```

Selecionar:

```text
Obter Dados
→ SQL Server
```

Preencher:

```text
Servidor:
NOME_DO_SERVIDOR\SQLEXPRESS

Banco:
BolsaEleicoes
```

---

# Tabelas para Importar

Selecionar:

```text
dim_empresa
dim_evento
dim_tempo
fato_cotacao
```

---

# Relacionamentos

## Empresa

```text
dim_empresa[id_empresa]
      1
      │
      │
      *
fato_cotacao[id_empresa]
```

## Evento

```text
dim_evento[id_evento]
      1
      │
      │
      *
fato_cotacao[id_evento]
```

## Tempo

```text
dim_tempo[id_tempo]
      1
      │
      │
      *
fato_cotacao[id_tempo]
```

---

# Dashboard Recomendado

## Filtro de Ano

Inserir uma Segmentação de Dados (Slicer).

Campo:

```text
ano_eleitoral
```

Configuração:

```text
Tipo = Between
```

Resultado:

```text
2014 ◄────────► 2026
```

Permitindo selecionar um intervalo de anos.

---

## Filtro de Segmento

Inserir outra Segmentação de Dados.

Campo:

```text
grupo
```

Configuração:

```text
Seleção múltipla = habilitada
```

Exibição:

```text
☑ Financeiro
☑ Petróleo e Gás
☑ Energia
☑ Varejo
☑ Construção
```

---

# Visual Principal

Tipo:

```text
Gráfico de Linhas
```

Eixo X:

```text
dias_para_eleicao
```

Legenda:

```text
grupo
```

Valor:

```text
Retorno Médio Diário
```

---

# Objetivo das Análises

Responder questões como:

- Como os bancos se comportam em períodos eleitorais?
- O setor de petróleo e gás reage positivamente ou negativamente?
- Quais segmentos apresentam maior volatilidade?
- Qual segmento apresenta melhor retorno em cada eleição?
- Existe padrão de comportamento entre eleições diferentes?

---

# Empresas Analisadas

## Financeiro

- ITUB4
- BBAS3
- BBDC4
- SANB11

## Petróleo, Gás e Biocombustíveis

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
