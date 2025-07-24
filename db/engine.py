from sqlalchemy import create_engine
from config.database import DATABASES, build_connection_string

def get_engine(db_name: str):
    db_config = DATABASES.get(db_name)
    conn_str = build_connection_string(db_config)
    return create_engine(conn_str)