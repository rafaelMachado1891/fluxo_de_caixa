from utils import CarregarCsv, Conexao_com_Banco
import os


conexao = Conexao_com_Banco()
engine = conexao.criar_engine()

diretorio = os.path.dirname(os.path.abspath(__file__))

arquivos = {
    "tbl_fluxo": "consulta_titulos.csv",
    "tbl_plano_contas": "plano_contas.csv",
    "tbl_lancamentos_fluxo": "fluxo_caixa.csv",
    "tbl_instituicoes": "instituicoes.csv",
    "tbl_saldo_inicial":"saldo_inicial.csv",
    "tbl_clientes": "clientes.csv"
}

for tabela, nome_arquivo in arquivos.items():
    caminho_arquivo = os.path.join(diretorio, "data", nome_arquivo)
    
    carga = CarregarCsv(caminho_arquivo)
    carga.processar(
        tabela=tabela,
        con=engine,
        metodo="replace",
        index=False
)
    
    print(f"dados carregados com sucesso na tabela {tabela}")
    
