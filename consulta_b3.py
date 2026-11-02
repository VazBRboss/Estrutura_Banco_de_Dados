from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

ATIVOS = {
    "ASAI3": "Varejo",
    "LREN3": "Varejo",
    "MGLU3": "Varejo",
    "PETR4": "Estatais|Commodities",
    "BBAS3": "Estatais",
    "CMIG4": "Estatais",
    "VALE3": "Commodities",
    "GGBR4": "Commodities",
    "SUZB3": "Commodities",
    "KLBN11": "Commodities",
}

DATA_INICIAL = "2026-10-01"
DATA_FINAL = "2026-10-30"

DATAS_ALVO = {
    "2026-10-05": "Data de estudo 1",
    "2026-10-26": "Data de estudo 2",
}

COLUNAS = [
    "fonte", "ticker", "grupos", "data", "marcador",
    "abertura", "maxima", "minima", "fechamento",
    "fechamento_ajustado", "volume",
]


def salvar_csv(dados, nome):
    caminho = Path(nome)

    dados.to_csv(
        caminho,
        index=False,
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    )

    print(f"Arquivo salvo: {caminho.resolve()}")


def main():
    tabelas = []
    avisos = []

    # O parâmetro end é exclusivo.
    # Acrescentamos um dia para incluir DATA_FINAL.
    fim_exclusivo = (
        date.fromisoformat(DATA_FINAL) + timedelta(days=1)
    ).isoformat()

    for ticker, grupos in ATIVOS.items():
        simbolo = f"{ticker}.SA"

        try:
            dados = yf.download(
                simbolo,
                start=DATA_INICIAL,
                end=fim_exclusivo,
                interval="1d",
                auto_adjust=False,
                multi_level_index=False,
                progress=False,
                threads=False,
                timeout=30,
            )

            if dados is None or dados.empty:
                raise ValueError("Nenhuma cotação retornada.")

            obrigatorias = ["Open", "High", "Low", "Close", "Volume"]
            faltantes = [
                coluna for coluna in obrigatorias
                if coluna not in dados.columns
            ]

            if faltantes:
                raise ValueError(f"Colunas ausentes: {faltantes}")

            # Não considera uma linha sem fechamento como cotação válida.
            dados = dados.dropna(subset=["Close"]).copy()

            if dados.empty:
                raise ValueError("Nenhum fechamento válido retornado.")

            dados.index.name = "data"
            dados = dados.reset_index()

            dados["data"] = pd.to_datetime(
                dados["data"]
            ).dt.strftime("%Y-%m-%d")

            dados = dados.rename(columns={
                "Open": "abertura",
                "High": "maxima",
                "Low": "minima",
                "Close": "fechamento",
                "Adj Close": "fechamento_ajustado",
                "Volume": "volume",
            })

            if "fechamento_ajustado" not in dados.columns:
                dados["fechamento_ajustado"] = pd.NA

            dados["fonte"] = "Yahoo Finance via yfinance"
            dados["ticker"] = ticker
            dados["grupos"] = grupos
            dados["marcador"] = dados["data"].map(
                DATAS_ALVO
            ).fillna("")

            # Confere também o intervalo localmente.
            dados = dados[
                dados["data"].between(DATA_INICIAL, DATA_FINAL)
            ]

            if dados.empty:
                raise ValueError("Nenhuma cotação no intervalo solicitado.")

            tabelas.append(dados[COLUNAS])
            print(f"{ticker}: {len(dados)} registros coletados.")

            datas_recebidas = set(dados["data"])

            for data_alvo in DATAS_ALVO:
                if data_alvo not in datas_recebidas:
                    avisos.append({
                        "ticker": ticker,
                        "aviso": f"Sem cotação retornada para {data_alvo}",
                    })

        except Exception as erro:
            avisos.append({
                "ticker": ticker,
                "aviso": str(erro),
            })
            print(f"{ticker}: falha na coleta: {erro}")

    if tabelas:
        resultado = pd.concat(tabelas, ignore_index=True)
        resultado = resultado.sort_values(["ticker", "data"])

        salvar_csv(resultado, "cotacoes_periodo.csv")

        recorte = resultado[
            resultado["data"].isin(DATAS_ALVO)
        ]

        salvar_csv(recorte, "cotacoes_datas_alvo.csv")
    else:
        print("Nenhuma cotação foi coletada.")

    if avisos:
        salvar_csv(
            pd.DataFrame(avisos),
            "avisos_coleta.csv",
        )


if __name__ == "__main__":
    try:
        main()
    except OSError as erro:
        print(f"Erro ao salvar os arquivos: {erro}")