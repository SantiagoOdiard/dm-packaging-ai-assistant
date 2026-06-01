import os

def get_embedding(text: str):
    """Return embedding vector for text using OpenAI embeddings.

    This function lazy-imports `openai` so the module can be imported
    even if the package is not installed (useful for local tests that
    don't call the function).
    """
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    try:
        import openai
    except Exception:
        raise RuntimeError('openai package not installed')
    openai.api_key = OPENAI_API_KEY
    resp = openai.Embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return resp["data"][0]["embedding"]
