from utils_db import Conexao_dw

c = Conexao_dw()
print("host:", c.host)
print("port:", c.port)

engine = c.criar_engine()
print("OK - conectou")