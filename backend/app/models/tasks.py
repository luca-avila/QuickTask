from sqlalchemy import text, create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, func
from backend.app.config import Config

# Create engine and metadata
engine = create_engine(Config.DATABASE_URL, echo=True)
meta = MetaData()

# Define tasks table
tasks = Table(
    'tasks',
    meta,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String),
    Column('priority', Integer, nullable=False),
    Column('completed', Boolean, server_default=text('0')),
    Column('date', Date, server_default=func.current_date())
)

def init_db():
    meta.create_all(engine)