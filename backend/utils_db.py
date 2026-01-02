import os
from sqlalchemy import create_engine, Engine
from dotenv import load_dotenv


class Conexao_dw:
    def __init__(self):
        load_dotenv()

        self.database = os.getenv("POSTGRES_DB")
        self.usuario = os.getenv("POSTGRES_USER")
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.password = os.getenv("POSTGRES_PASSWORD")

        self.url = (
            f"postgresql+psycopg2://"
            f"{self.usuario}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

        self.engine: Engine | None = None

    def criar_engine(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(self.url)
        return self.engine