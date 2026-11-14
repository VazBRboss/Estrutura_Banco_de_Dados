import pandas as pd
import pyodbc

# ==================================
# ARQUIVO
# ==================================

ARQUIVO_CSV = (
    r"C:\VirtualDev\Fatec\Estrutura de Dados"
    r"\Estrutura_Banco_de_Dados-main"
    r"\cotacoes_eleicoes.csv"
)

# ==================================
# SQL SERVER
# ==================================

SERVIDOR = r"DESKTOP-R8C4SUV\SQLEXPRESS"
BANCO = "BolsaEleicoes"

# ==================================
# LEITURA
# ==================================

df = pd.read_csv(
    ARQUIVO_CSV,
    sep=";",
    decimal=",",
    encoding="utf-8-sig"
)

# Remove espaços acidentais
df.columns = df.columns.str.strip()

print("Colunas encontradas:")
print(df.columns.tolist())

# ==================================
# VALIDAÇÃO
# ==================================

colunas_esperadas = [
    "fonte",
    "ticker",
    "grupo",
    "evento_eleitoral",
    "data_eleicao",
    "dias_para_eleicao",
    "data",
    "abertura",
    "maxima",
    "minima",
    "fechamento",
    "fechamento_ajustado",
    "volume"
]

faltantes = [
    c for c in colunas_esperadas
    if c not in df.columns
]

if faltantes:
    raise Exception(
        f"Colunas ausentes: {faltantes}"
    )

# ==================================
# TIPOS
# ==================================

df["data"] = pd.to_datetime(df["data"])

df["data_eleicao"] = pd.to_datetime(
    df["data_eleicao"]
)

# ==================================
# CONEXÃO
# ==================================

conn = pyodbc.connect(
    f"""
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={SERVIDOR};
    DATABASE={BANCO};
    Trusted_Connection=yes;
    """
)

cursor = conn.cursor()

cursor.fast_executemany = True

# ==================================
# INSERT
# ==================================

sql = """
INSERT INTO cotacoes_raw
(
    fonte,
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
    fechamento_ajustado,
    volume
)
VALUES
(
    ?,?,?,?,?,?,?,?,?,?,?,?,?
)
"""

# Troca NaN por None
df = df.where(
    pd.notnull(df),
    None
)

dados = list(
    df.itertuples(
        index=False,
        name=None
    )
)

cursor.executemany(
    sql,
    dados
)

conn.commit()

print(
    f"{len(dados)} registros inseridos."
)

cursor.close()
conn.close()

print("Carga concluída.")