import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from airflow.hooks.base import BaseHook
from typing import Optional


class CarregarCsv:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df: DataFrame | None = None

    def carregar_csv(self) -> DataFrame:
        self.df = pd.read_csv(self.file_path)
        return self.df

    def renomear_colunas(
        self,
        colunas: Optional[dict[str, str]] = None
    ) -> DataFrame:
        if self.df is None:
            raise ValueError("CSV ainda não carregado")

        if colunas:
            self.df.rename(columns=colunas, inplace=True)

        return self.df

    def carregar_no_banco(
        self,
        tabela: str,
        engine: Engine,
        metodo: str = "replace",
        index: bool = False
    ) -> None:

        if self.df is None:
            raise ValueError("DataFrame não carregado")

        if metodo == "replace":
            # begin() = abre transação e COMMIT automático
            with engine.begin() as conn:
                conn.execute(
                    text(f'DROP TABLE IF EXISTS "{tabela}" CASCADE')
                )

        # pandas recebe SEMPRE o ENGINE
        self.df.to_sql(
            name=tabela,
            con=engine,
            if_exists=metodo,
            index=index,
            method="multi"
        )

class ConexaoComBanco:
    def __init__(self, conn_id: str):
        conn = BaseHook.get_connection(conn_id)

        self.url = (
            f"postgresql+psycopg2://"
            f"{conn.login}:{conn.password}"
            f"@{conn.host}:{conn.port}/{conn.schema}"
        )

        self.engine: Engine | None = None

    def criar_engine(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(self.url)
        return self.engine