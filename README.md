# RAG Sample with Claude + pgvector

A minimal, end-to-end Retrieval-Augmented Generation (RAG) example: Postgres +
[pgvector](https://github.com/pgvector/pgvector) for vector storage/search, a
local [sentence-transformers](https://www.sbert.net/) model for embeddings,
and [Claude](https://docs.claude.com/) for the answer-generation step.

Built as a training reference — read through `db.py`, `embeddings.py`,
`ingest.py`, `search.py`, and `generate.py` in that order to follow the RAG
pipeline end to end.

## Pipeline

1. **Ingest** ([ingest.py](ingest.py)) — split `data/sample_docs.txt` into
   chunks, embed each chunk, store the text + vector in Postgres.
2. **Search** ([search.py](search.py)) — embed a query and run a cosine
   nearest-neighbor lookup against the stored vectors.
3. **Generate** ([generate.py](generate.py)) — pass the retrieved chunks to
   Claude as context and ask it to answer strictly from that context.

## Setup

```bash
docker compose up -d
pip install -r requirements.txt
cp .env.example .env   # then fill in ANTHROPIC_API_KEY
```

Load environment variables from `.env` before running any script (e.g.
`export $(cat .env | xargs)` on Linux/macOS, or set them manually on
Windows).

## Usage

```bash
python db.py                              # create the table + index
python ingest.py                          # embed and load data/sample_docs.txt
python search.py "what is pgvector?"      # raw vector search, no LLM
python generate.py "what is pgvector?"    # full RAG: retrieve + Claude answer
```

## Notes

- Embeddings use `all-MiniLM-L6-v2` (384 dimensions) — swap the model in
  [embeddings.py](embeddings.py) if you need a different embedding size, and
  update `EMBEDDING_DIM` in [db.py](db.py) to match.
- `generate.py` defaults to `claude-opus-5`. Change `MODEL` there to use a
  different Claude model.
- Chunking in `ingest.py` splits `data/sample_docs.txt` on blank lines —
  swap in your own loader for real documents (PDFs, HTML, etc.).

## Disclosure

This sample was generated with AI assistance (Claude Code). Review and adapt
it before using it beyond training/demo purposes.
