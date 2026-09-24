import os

import psycopg2
from pgvector.psycopg2 import register_vector

DSN = os.environ.get(
    "DATABASE_URL",
    "dbname=rag_demo user=rag_demo password=rag_demo host=localhost port=5432",
)
EMBEDDING_DIM = 384


def get_connection():
    conn = psycopg2.connect(DSN)
    register_vector(conn)
    return conn


def init_db():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding VECTOR({EMBEDDING_DIM})
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS documents_embedding_idx
            ON documents USING hnsw (embedding vector_cosine_ops)
        """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
