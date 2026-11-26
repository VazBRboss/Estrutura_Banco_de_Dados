arquivo = r"C:\VirtualDev\Fatec\Estrutura de Dados\Estrutura_Banco_de_Dados-main\cotacoes_eleicoes.csv"

with open(
    arquivo,
    encoding="utf-8-sig"
) as f:

    cabecalho = f.readline()

    qtd_colunas = len(
        cabecalho.strip().split(";")
    )

    for numero, linha in enumerate(f, start=2):

        colunas = len(
            linha.strip().split(";")
        )

        if colunas != qtd_colunas:

            print(
                f"Linha {numero}: "
                f"{colunas} colunas "
                f"(esperado {qtd_colunas})"
            )