from sqlalchemy import create_engine, MetaData, Table, select, and_, inspect
from sqlalchemy.orm import sessionmaker
from datetime import date
import pandas as pd


def fetch_stock_data(ticker: str, start_date: date, end_date: date) -> pd.DataFrame:
        engine = create_engine("mysql+mysqlconnector://root:admin@localhost/stock_data_db")
        Session = sessionmaker(bind=engine)
        metadata = MetaData()

        inspector = inspect(engine)
        if ticker.lower() not in inspector.get_table_names():
            raise ValueError(f"Table {ticker} does not exist.")
        
        table = Table(
            ticker.lower(),
            metadata,
            autoload_with=engine  # No schema needed for MySQL
        )
        
        query = (
            select(table)
            .where(and_(
                table.c.date >= start_date,
                table.c.date < end_date
            ))
        )
        
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        
        return df