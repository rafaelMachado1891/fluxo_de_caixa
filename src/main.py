from utils import CarregarCsv, Conexao_com_Banco

conexao = Conexao_com_Banco()
engine = conexao.criar_engine()

titulos = ('C:/Users/rafad/Documents/Repositorios_Git/fluxo_de_caixa/src/data/consulta_titulos.csv')

carga_fluxo = CarregarCsv(titulos)

carga_fluxo.carregar_csv()

carga_fluxo.carregar_no_banco(
    tabela="tbl_fluxo",
    con=engine,
    metodo="replace",
    index=False
)

print("✅ Dados carregados com sucesso na tabela tbl_fluxo")