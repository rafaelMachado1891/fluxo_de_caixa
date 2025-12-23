from src.utils import CarregarCsv, ConexaoComBanco
import os


def rodar_pipeline():
    conexao = ConexaoComBanco(conn_id="postgres_fluxo")
    engine = conexao.criar_engine()

    diretorio = os.path.dirname(os.path.abspath(__file__))

    arquivos = {
        "tbl_fluxo": "consulta_titulos.csv",
        "tbl_plano_contas": "plano_contas.csv",
        "tbl_lancamentos_fluxo": "fluxo_caixa.csv",
        "tbl_instituicoes": "instituicoes.csv",
        "tbl_saldo_inicial": "saldo_inicial.csv",
    }

    for tabela, nome_arquivo in arquivos.items():
        caminho = os.path.join(diretorio, "data", nome_arquivo)

        carga = CarregarCsv(caminho)
        carga.carregar_csv()
        carga.carregar_no_banco(
            tabela=tabela,
            engine=engine,
            metodo="replace",
            index=False
        )

        print(f"dados carregados com sucesso na tabela {tabela}")