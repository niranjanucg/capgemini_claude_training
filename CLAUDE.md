# CLAUDE.md — Project memory

**What this is:** an **NL2SQL platform over ITSM ticket data**. A service manager types a
plain-English question ("which assignment groups breached SLA most last month?"); the system
writes SQL, runs it **read-only**, and answers in plain English — **with the SQL shown** for trust.

**Build tool vs runtime (keep these separate):**
- We **BUILD** this platform **with Claude Code** — that is the skill being taught.
- The **running app** calls the **OpenAI API** at runtime to generate SQL.

**Stack:** Python 3.11+ · SQLite (swappable to Postgres/Snowflake later) · stdlib where possible.
Only runtime dependency for the spike is the OpenAI SDK (+ python-dotenv for the key).

**Build the database:** `python db/build_db.py`   (creates `db/itsm.db`, prints row counts)
**Run the naive spike:** `python spike/naive_nl2sql.py "your question"`

**Safety posture the platform will enforce (aspirational on Day 1, built Day 2+):**
read-only · **SELECT-only** · auto-LIMIT · **no raw PII (e.g. emails) in output**.

**Folder map (which day fills each):**
- `db/`, `scripts/`, `docs/`, `spike/` — Day 1 (this build: schema, data, ERD, naive spike)
- `semantics/` — Day 2 (meta_* semantic catalog)   · `evals/` — Day 2 (accuracy set)
- `agent/` — Day 2–3 (NL2SQL agent loop)   · `api/` — Day 3 (FastAPI)   · `ui/` — Day 4 (Streamlit)
