import sys

from db import get_connection
from embeddings import embed

DEFAULT_DOCS_PATH = "data/sample_docs.txt"


def load_docs(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def ingest(docs):
    vectors = embed(docs)
    conn = get_connection()
    with conn.cursor() as cur:
        for doc, vector in zip(docs, vectors):
            cur.execute(
                "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                (doc, vector),
            )
    conn.commit()
    conn.close()
    print(f"Ingested {len(docs)} documents.")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOCS_PATH
    ingest(load_docs(path))
