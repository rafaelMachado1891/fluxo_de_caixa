select 
Codigo,
tipo,
DataReceb,
descricao,
valor,
NumTitulo,
Serie,
Instituicao,
ContaContabil,
ContaContabilDebito,
N,
Tipo_C,
Codigo_C
from FluxoCaixa 
where year(datareceb) = 2025