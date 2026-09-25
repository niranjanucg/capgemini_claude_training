# agent/ — placeholder

**Filled on Day 2–3.** This will hold the **NL2SQL agent loop**: the code that takes a plain-English
question, pulls in the semantic layer, prompts the OpenAI API for SQL, validates it (SELECT-only,
auto-LIMIT, PII masking), runs it read-only, and turns the rows back into a plain-English answer.
Empty on purpose for now.
