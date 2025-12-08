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


plano_contas = ('C:/Users/rafad/Documents/Repositorios_Git/fluxo_de_caixa/src/data/plano_contas.csv')

carga_plano_contas = CarregarCsv(plano_contas)

carga_plano_contas.carregar_csv()

carga_plano_contas.carregar_no_banco(
    tabela="tbl_plano_contas",
    con=engine,
    metodo="replace",
    index=False
)

instituicoes = ('C:/Users/rafad/Documents/Repositorios_Git/fluxo_de_caixa/src/data/instituicoes.csv')

carga_instituicoes = CarregarCsv(instituicoes)

carga_instituicoes.carregar_csv()

carga_instituicoes.carregar_no_banco(
    tabela='tbl_instituicoes',
    con=engine,
    metodo='replace',
    index=False
)

lancamentos_fluxo = ('C:/Users/rafad/Documents/Repositorios_Git/fluxo_de_caixa/src/data/fluxo_caixa.csv')

carga_lancamentos_fluxo = CarregarCsv(lancamentos_fluxo)

carga_lancamentos_fluxo.carregar_csv()

carga_lancamentos_fluxo.carregar_no_banco(
    tabela='tbl_lancamentos_fluxo',
    con=engine,
    metodo="replace",
    index=False
)

print("✅ Dados carregados com sucesso na tabela tbl_fluxo")

print("✅ Dados carregados com sucesso na tabela tbl_plano_contas")

print("✅ Dados carregados com sucesso na tabela tbl_instituicoes")

print("✅ Dados carregados com sucesso na tabela tbl_lancamentos_fluxo")
