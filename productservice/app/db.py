from sqlmodel import SQLModel, Session, create_engine
from app import settings


connection_string = str(settings.DATABASE_URL).replace("postgresql","postgresql+psycopg")
engine = create_engine(connection_string, connect_args={}, pool_recycle=300, pool_size=10 )

def create_table():
    SQLModel.metadata.create_all(engine)

def get_session(session):
    with Session(engine) as session:
        yield session    


def get_product_from_db(
        
):
    pass