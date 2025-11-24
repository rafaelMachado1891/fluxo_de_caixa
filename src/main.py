from utils import CarregarCsv, Conexao_com_Banco


arquivo_fluxo = ('C:/Users/rafad/Documents/Repositorios_Git/fluxo_de_caixa/src/data/fluxo_caixa.csv')

titulos = ('C:/Users/rafad/Documents/Repositorios_Git/fluxo_de_caixa/src/data/titulos.csv')

conexao = Conexao_com_Banco()
engine = conexao.criar_engine()

carregador_fluxo = CarregarCsv(arquivo_fluxo)

carregador_fluxo.carregar_csv()

rename_columns_fluxo = {
    'codigo': 'id_lancamento',
    'tipo': 'tipo',
    'Tipo_C': 'tipo_lancamento',
    'DataReceb': 'data_recebimento',
    'Descricao': 'descricao_do_lancamento',
    'complemento': 'origem_lancamento',
    'valor': 'valor',
    'NumTitulo': 'numero_titulo',
    'ordem': 'ordem',
    'Instituicao': 'instituicao_de_pagamento',
    'ContaContabil': 'conta_contabil',
    'ContaContabilDebito': 'conta_contabil_debito',
    'Serie': 'serie',
    'Codigo_C': 'id_cliente',
    'Num_Pag': 'parcela'
}

tbl_fluxo = carregador_fluxo.renomear_colunas(rename_columns_fluxo)

carregador_fluxo.carregar_no_banco(
    tabela="tbl_fluxo",
    con=engine,
    metodo="replace",
    index=False
)

print("✅ Dados carregados com sucesso na tabela tbl_fluxo")