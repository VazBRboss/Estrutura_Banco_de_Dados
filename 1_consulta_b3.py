from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

# =====================================================
# ATIVOS DE ESTUDO
# =====================================================

ATIVOS = {
    # Financeiro
    "ITUB4": "Financeiro",
    "BBAS3": "Financeiro",
    "BBDC4": "Financeiro",
    "SANB11": "Financeiro",

    # Petróleo, Gás e Biocombustíveis
    "PETR3": "Petroleo_Gas",
    "PETR4": "Petroleo_Gas",
    "PRIO3": "Petroleo_Gas",
    "BRAV3": "Petroleo_Gas",
    "RECV3": "Petroleo_Gas",

    # Energia Elétrica
    "ELET3": "Energia",
    "ELET6": "Energia",
    "EGIE3": "Energia",
    "CPFE3": "Energia",
    "ISAE4": "Energia",

    # Varejo
    "MGLU3": "Varejo",
    "LREN3": "Varejo",
    "MELI34": "Varejo",
    "SOMA3": "Varejo",

    # Construção Civil
    "CYRE3": "Construcao",
    "MRVE3": "Construcao",
    "DIRR3": "Construcao",
    "EZTC3": "Construcao",
}

# =====================================================
# ELEIÇÕES PRESIDENCIAIS
# =====================================================

EVENTOS_ELEITORAIS = {
    "2014_1T": "2014-10-05",
    "2014_2T": "2014-10-26",

    "2018_1T": "2018-10-07",
    "2018_2T": "2018-10-28",

    "2022_1T": "2022-10-02",
    "2022_2T": "2022-10-30",

    "2026_1T": "2026-10-04",
    "2026_2T": "2026-10-25",
}

# 10 dias antes e depois
JANELA_PRE = 30
JANELA_POS = 30

COLUNAS = [
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
    "volume",
]

# =====================================================
# FUNÇÕES
# =====================================================

def salvar_csv(df, nome_arquivo):
    caminho = Path(nome_arquivo)

    df.to_csv(
        caminho,
        index=False,
        sep=";",
        decimal=",",
        encoding="utf-8-sig"
    )

    print(f"Arquivo salvo: {caminho.resolve()}")

# =====================================================
# EXECUÇÃO
# =====================================================

def main():

    resultados = []
    avisos = []

    total_coletas = (
        len(ATIVOS)
        * len(EVENTOS_ELEITORAIS)
    )

    contador = 0

    for evento, data_evento_str in EVENTOS_ELEITORAIS.items():

        data_evento = datetime.strptime(
            data_evento_str,
            "%Y-%m-%d"
        )

        data_inicial = (
            data_evento - timedelta(days=JANELA_PRE)
        ).strftime("%Y-%m-%d")

        data_final = (
            data_evento + timedelta(days=JANELA_POS)
        ).strftime("%Y-%m-%d")

        fim_exclusivo = (
            datetime.strptime(
                data_final,
                "%Y-%m-%d"
            ).date()
            + timedelta(days=1)
        ).isoformat()

        print()
        print("=" * 70)
        print(
            f"Evento: {evento}"
            f" | Eleição: {data_evento_str}"
        )
        print(
            f"Período: {data_inicial} a {data_final}"
        )
        print("=" * 70)

        for ticker, grupo in ATIVOS.items():

            contador += 1

            simbolo = f"{ticker}.SA"

            print(
                f"[{contador}/{total_coletas}] "
                f"Coletando {ticker}..."
            )

            try:

                dados = yf.download(
                    simbolo,
                    start=data_inicial,
                    end=fim_exclusivo,
                    interval="1d",
                    auto_adjust=False,
                    progress=False,
                    threads=False,
                    timeout=30,
                    multi_level_index=False
                )

                if dados.empty:
                    raise ValueError(
                        "Nenhuma cotação retornada."
                    )

                dados = dados.dropna(
                    subset=["Close"]
                ).copy()

                dados.index.name = "data"
                dados = dados.reset_index()

                dados["data"] = (
                    pd.to_datetime(
                        dados["data"]
                    )
                    .dt.strftime("%Y-%m-%d")
                )

                dados = dados.rename(
                    columns={
                        "Open": "abertura",
                        "High": "maxima",
                        "Low": "minima",
                        "Close": "fechamento",
                        "Adj Close":
                            "fechamento_ajustado",
                        "Volume": "volume",
                    }
                )

                if (
                    "fechamento_ajustado"
                    not in dados.columns
                ):
                    dados[
                        "fechamento_ajustado"
                    ] = pd.NA

                dados["fonte"] = (
                    "Yahoo Finance"
                )

                dados["ticker"] = ticker

                dados["grupo"] = grupo

                dados[
                    "evento_eleitoral"
                ] = evento

                dados[
                    "data_eleicao"
                ] = data_evento_str

                dados[
                    "dias_para_eleicao"
                ] = (
                    pd.to_datetime(
                        dados["data"]
                    )
                    - pd.to_datetime(
                        data_evento_str
                    )
                ).dt.days

                resultados.append(
                    dados[COLUNAS]
                )

            except Exception as erro:

                avisos.append(
                    {
                        "ticker": ticker,
                        "evento": evento,
                        "erro": str(erro),
                    }
                )

                print(
                    f"Erro {ticker}: {erro}"
                )

    # =================================================
    # CSV PRINCIPAL
    # =================================================

    if resultados:

        resultado_final = pd.concat(
            resultados,
            ignore_index=True
        )

        resultado_final = (
            resultado_final
            .sort_values(
                [
                    "evento_eleitoral",
                    "ticker",
                    "data",
                ]
            )
        )

        salvar_csv(
            resultado_final,
            "cotacoes_eleicoes.csv"
        )

        print()
        print(
            f"Registros coletados: "
            f"{len(resultado_final):,}"
        )

    # =================================================
    # AVISOS
    # =================================================

    if avisos:

        salvar_csv(
            pd.DataFrame(avisos),
            "avisos_coleta.csv"
        )

        print(
            f"Ocorreram "
            f"{len(avisos)} aviso(s)."
        )

    print()
    print("Concluído.")


if __name__ == "__main__":
        main()
