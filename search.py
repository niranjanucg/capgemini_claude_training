import sys

from db import get_connection
from embeddings import embed


def search(query, top_k=3):
    query_vector = embed([query])[0]
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT content, embedding <=> %s AS distance
            FROM documents
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (query_vector, query_vector, top_k),
        )
        results = cur.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "What is retrieval-augmented generation?"
    for content, distance in search(query):
        print(f"[{distance:.4f}] {content}")
