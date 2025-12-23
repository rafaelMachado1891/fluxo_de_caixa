import pandas as pd
from pandas import DataFrame
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import psycopg2
from urllib.parse import quote_plus
from dotenv import load_dotenv
from typing import Optional
from airflow.hooks.base import BaseHook


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
    

class CarregarCsv:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def carregar_csv(self):
        self.df = pd.read_csv(self.file_path)
        return self.df

    def carregar_no_banco(
        self,
        tabela: str,
        con: Engine,
        metodo: str = "replace",
        index: bool = False
    ) -> None:

        if self.df is None:
            raise ValueError("DataFrame não carregado")

        # Drop controlado
        if metodo == "replace":
            with con.begin() as conn:
                conn.execute(
                    text(f'DROP TABLE IF EXISTS "{tabela}" CASCADE')
                )

        # Pandas SEMPRE recebe ENGINE
        self.df.to_sql(
            name=tabela,
            con=con,
            if_exists=metodo,
            index=index,
            method="multi"
        )

class Conexao_com_Banco:
    def __init__(self, conn_id: str):
        conn = BaseHook.get_connection(conn_id)

        if not conn.port:
            raise ValueError("Porta não configurada na Connection do Airflow")

        self.url = (
            f"postgresql+psycopg2://"
            f"{conn.login}:{conn.password}"
            f"@{conn.host}:{conn.port}/{conn.schema}"
        )

        self.engine: Engine | None = None

    def criar_engine(self) -> Engine:
        self.engine = create_engine(self.url)
        return self.engine