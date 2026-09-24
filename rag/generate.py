import anthropic

from search import search

MODEL = "claude-opus-5"

SYSTEM_PROMPT = (
    "You are a Q&A assistant. Answer the user's question using only the "
    "numbered context passages below. If the passages don't contain the "
    "answer, say you don't have enough information. Cite passage numbers "
    "like [1] that support each claim."
)


def build_context(results):
    return "\n\n".join(f"[{i + 1}] {content}" for i, (content, _) in enumerate(results))


def answer(question, top_k=3):
    results = search(question, top_k=top_k)
    context = build_context(results)

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}",
        }],
    )

    return next(block.text for block in response.content if block.type == "text")


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) or "What is retrieval-augmented generation?"
    print(answer(question))
