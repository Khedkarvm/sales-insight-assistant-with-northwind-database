# nl_to_sql.py

import os
import re
import pandas as pd
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# env
load_dotenv()


# LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-lite-latest",
    temperature=0
)


# db connection
DB_URL = "postgresql+psycopg2://postgres:9767@localhost:5433/northwind"
engine = create_engine(DB_URL)


# schema
BASE_SCHEMA = """
customers(customer_id, company_name, contact_name, city, country)
orders(order_id, customer_id, employee_id, order_date, shipped_date, ship_country)
employees(employee_id, first_name, last_name, title)
products(product_id, product_name, supplier_id, category_id, unit_price)
categories(category_id, category_name)
suppliers(supplier_id, company_name)
"""


# LOV config
LOV_COLUMNS = {
    "customers": ["city", "country"],
    "orders": ["ship_country"],
    "employees": ["title"]
}


def extract_lovs(engine, config, limit=10):
    lovs = []
    with engine.connect() as conn:
        for table, columns in config.items():
            for column in columns:
                query = text(f"""
                    SELECT DISTINCT {column}
                    FROM {table}
                    WHERE {column} IS NOT NULL
                    LIMIT :limit
                """)
                result = conn.execute(query, {"limit": limit})
                values = [row[0] for row in result]
                lovs.append(f"{table}.{column} sample values: {values}")
    return "\n".join(lovs)


LOV_TEXT = extract_lovs(engine, LOV_COLUMNS)


# prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template=f"""
You are an expert PostgreSQL SQL generator.

Database schema:
{BASE_SCHEMA}

Sample values:
{LOV_TEXT}

Rules:
- Use only the tables above
- PostgreSQL syntax
- Return ONLY SQL (no explanation, no markdown)

Question: {{question}}

SQL:
"""
)

chain = prompt | llm | StrOutputParser()


# main idea of function
def run_question(question: str):
    """
    Returns:
        df (DataFrame)
        sql (str)
    """

    try:
        # basic validation
        if len(question.split()) < 2 or not re.search(r"[a-zA-Z]", question):
            raise ValueError("Invalid or unclear question")

        #  LLM SQL generation
        sql_query = chain.invoke({"question": question})
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        # safety check
        if not sql_query.lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed")

        # SQL execution
        with engine.connect() as conn:
            df = pd.read_sql(text(sql_query), conn)

        return df, sql_query

    except Exception as e:
        error_df = pd.DataFrame({"error": [str(e)]})
        return error_df, "SQL generation failed"
