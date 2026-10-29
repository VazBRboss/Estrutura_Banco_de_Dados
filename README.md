# Estrutura_Banco_de_Dados
Used for final project from Estrutura de Banco de Dados - project that will use data from API B3 to get how the elections periods affect brasilian companies.  
We will use the https://dadosb3.com/empresas/WEGE3/indicadores and some others Endpoints.  


## 1.Contextualização

O Mercado financeiro do brasil sofre uma mudança significativa a cada grande evento dentro do nosso cenário.  
Este projeto analisa o comportamento do mercado de capitais brasileiro ao longo dos últimos quatro ciclos eleitorais.  

## 2.Metodologia e Segmentação

Selecionaremos os 3 ou 4 ativos mais impactantes dentro de Comodites, Varejo e Estatais.  E avaliaremos como nas últimas eleições estes indicadores foram afetados em pontos percentuais, em como se comportaram durante o primeiro e segundo turno se caso aplicável e como esse comportamento foi afetado por eleições diretas.  

##3. Fonte de Dados: 

API Dados B3,  Yahoo Finance API e Tribunal Superior Eleitoral do TSE para que tenha os marcadores dasdatas.  

##4.  Coleta de dados:  Rest da API e biblioteca Yahoo otimizada para download.  PANDAS, NUMPY, SCIPY/STATSMODELS. 

##5.  Visualização
Usaremos Full .html com ploty
[API Dados B3 + yfinance] ──> [pandas / numpy] ──> [Plotly (Python)] ──> [Arquivo .html Interativo]
    (Coleta de Dados)         (Tratamento e Estatística)   (Mecanismo de Renderização)       (Artefato Final / Dashboard)


