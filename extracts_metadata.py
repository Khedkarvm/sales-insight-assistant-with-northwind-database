from sqlalchemy import create_engine, inspect

DB_URL = "postgresql+psycopg2://postgres:9767@localhost:5433/northwind"

engine = create_engine(DB_URL)

# Inspector to fetch metadata
inspector = inspect(engine)

print("== Northwind Database Metadata ==\n")

# Get all table names
tables = inspector.get_table_names()

for table in tables:
    print(f"Table: {table}")
    
    columns = inspector.get_columns(table)
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")

    print("-" * 40)
