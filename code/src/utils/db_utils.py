import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def insert_into_db(df, table_name):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    for i, row in df.iterrows():
        columns = ','.join(row.index)
        values = ','.join([f'%s'] * len(row.values))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(sql, tuple(row.values))
    conn.commit()
    cursor.close()
    conn.close()