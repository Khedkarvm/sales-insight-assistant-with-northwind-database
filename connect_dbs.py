from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase

# PostgreSQL connection URL
db_url = "postgresql+psycopg2://postgres:9767@localhost:5433/northwind"

# Create SQLAlchemy engine
engine = create_engine(db_url)

# Connect LangChain
db = SQLDatabase(engine)

tables = db.get_table_names()
print("Tables in Northwind Database:")
for t in tables:
    print("-", t)


# Show table metadata

print("Table Metadata:\n")

for table in tables:
    print(f"Table: {table}")
    print(db.get_table_info([table]))
    print("-" * 60)


    