import pandas as pd
from pandas import DataFrame
import os
from sqlalchemy import create_engine, text, Engine
import psycopg2
from urllib.parse import quote_plus
from dotenv import load_dotenv
from typing import Optional


class CarregarCsv():
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df: DataFrame = None


    def carregar_csv(self) -> DataFrame:
        """
        carrega o csv e retorna um DataFrame.
        """
        self.df = pd.read_csv(self.file_path)
        return self.df
    

    def renomear_colunas(self, colunas: Optional[dict[str, str]]) -> DataFrame:
        """
        metodo para renomear as colunas do DataFrame
        exemplo de uso {"coluna": "nova_coluba"}
        """
        
        if self.df is None:
            raise ValueError("O csv não foi carregado ainda usar o metodo carregar csv")
        
        if colunas is not None:
            self.df.rename(columns=colunas, inplace = True)

        return self.df
    

    def carregar_no_banco(self, tabela:str, con:Engine, metodo: str = "replace", index: bool = False) -> None:
        """
         Carrega o DataFrame no banco de dados.
        - tabela: nome da tabela
        - con: conexão/engine SQLAlchemy
        - metodo: 'fail', 'replace' ou 'append'
        - index: se deve salvar o índice
        """
        if metodo == 'replace':
            with con.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {tabela} CASCADE"))
                conn.commit()
                
        self.df.to_sql(
            name=tabela,
            con=con,
            if_exists=metodo,
            index=index
        )

    def processar(self, tabela, con, metodo: str = "replace", index: bool = False):
        
        self.carregar_csv()
        self.carregar_no_banco(
            tabela=tabela,
            con=con,
            metodo=metodo,
            index=index
        )


class Conexao_com_Banco():
    def __init__(self):
        load_dotenv()
        self.database = os.getenv("DATABASE")
        self.usuario = os.getenv("USER")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.password = os.getenv("PASSWORD")

        self.url = f"postgresql://{self.usuario}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine: Engine | None = None

    def criar_engine(self) -> Engine:
        self.engine = create_engine(self.url)
        return self.engine
        