from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "postgresql://yukeon:d4594283!@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def table_has_data(table_name: str) -> bool:
    """Checks if a table has any data."""
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT EXISTS(SELECT 1 FROM {table_name} LIMIT 1);"))
        return result.scalar()


def execute_sql_file_if_empty(sql_file_path: str, table_name: str):
    if not table_has_data(table_name):
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read()
            with engine.connect() as connection:
                connection.execute(text(sql_commands))
    else:
        print("Data already exists")


if __name__ == "__main__":
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'insert.text')
    table_name = "complaints"
    execute_sql_file_if_empty(sql_file_path, table_name)
