"""
RAG service: load docs, chunk, embed with Ollama, store in Chroma;
on query: embed, retrieve top-k, build prompt, generate with Ollama.
"""
import pathlib
import re
import requests
import chromadb
from chromadb.config import Settings as ChromaSettings

from config import (
    OLLAMA_HOST,
    OLLAMA_EMBED_MODEL,
    OLLAMA_CHAT_MODEL,
    CHROMA_PATH,
    CHROMA_COLLECTION,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    SAMPLE_DOCS_DIR,
)

SYSTEM_PROMPT = """You are a nutrition-oriented Food Planner assistant. Use only the context below to support your answers—if context is thin, say so and avoid inventing precise nutrient claims.

When the user asks for meal ideas, give 2–3 concrete options with short "because…" rationales (nutrients, balance, constraints).

Recommend meals based on nutrition and the user's stated preferences or restrictions. For medical diagnosis, treatment, or medication questions, do not advise; suggest consulting a qualified professional.

Do not encourage extreme restriction, purging, laxative misuse, fasting for unsafe weight loss, or anything that could enable an eating disorder. If a request asks for dangerously low intake or harmful behaviors, refuse briefly and suggest professional support (clinician, therapist, or eating-disorder–informed dietitian).

If the question is not about food or nutrition, politely redirect to meal planning and nutrition."""


def _backend_dir():
    return pathlib.Path(__file__).resolve().parent


def _get_chroma_path():
    p = pathlib.Path(CHROMA_PATH)
    if not p.is_absolute():
        p = _backend_dir() / p
    return str(p)


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Split text into overlapping chunks by character count."""
    if not text or not text.strip():
        return []
    text = text.strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap if overlap < chunk_size else end
    return chunks


def _split_by_double_newline(text: str):
    """Split by double newline first, then chunk large segments."""
    parts = re.split(r"\n\s*\n", text)
    result = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(part) <= CHUNK_SIZE:
            result.append(part)
        else:
            result.extend(_chunk_text(part, CHUNK_SIZE, CHUNK_OVERLAP))
    return result


def load_docs(docs_dir: pathlib.Path):
    """Load .txt files from docs_dir, split into chunks. Return list of (text, source_id)."""
    chunks_with_meta = []
    if not docs_dir.is_dir():
        return chunks_with_meta
    for path in sorted(docs_dir.glob("*.txt")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        source_id = path.stem
        for chunk in _split_by_double_newline(text):
            if chunk.strip():
                chunks_with_meta.append((chunk.strip(), source_id))
    return chunks_with_meta


def embed_with_ollama(texts: list[str]) -> list[list[float]]:
    """Call Ollama /api/embed: `input` (string or list) and response `embeddings` (see Ollama docs)."""
    if not texts:
        return []
    url = f"{OLLAMA_HOST.rstrip('/')}/api/embed"
    try:
        r = requests.post(
            url,
            json={"model": OLLAMA_EMBED_MODEL, "input": texts},
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        if "embeddings" in data and data["embeddings"] is not None:
            vecs = data["embeddings"]
            if len(vecs) != len(texts):
                raise ValueError(
                    f"Ollama returned {len(vecs)} embeddings for {len(texts)} inputs"
                )
            return [list(v) for v in vecs]
        if "embedding" in data and len(texts) == 1:
            return [list(data["embedding"])]
        raise ValueError("Ollama embed response missing 'embeddings' (or legacy 'embedding')")
    except requests.RequestException as e:
        raise RuntimeError(f"Ollama embed request failed: {e}") from e


def get_client():
    """Persistent Chroma client pointing at CHROMA_PATH."""
    return chromadb.PersistentClient(path=_get_chroma_path(), settings=ChromaSettings(anonymized_telemetry=False))


def ensure_collection(client):
    """Get or create the RAG collection."""
    return client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"description": "RAG documents for Food Planner"},
    )


def ingest_docs(docs_dir: pathlib.Path = None):
    """Load docs from dir, embed, add to Chroma. If docs_dir is None, use SAMPLE_DOCS_DIR."""
    if docs_dir is None:
        docs_dir = _backend_dir() / SAMPLE_DOCS_DIR
    chunks_with_meta = load_docs(docs_dir)
    if not chunks_with_meta:
        return 0
    texts = [c[0] for c in chunks_with_meta]
    vectors = embed_with_ollama(texts)
    client = get_client()
    try:
        client.delete_collection(CHROMA_COLLECTION)
    except Exception:
        pass
    coll = ensure_collection(client)
    ids = [f"doc_{i}" for i in range(len(texts))]
    metadatas = [{"source": c[1]} for c in chunks_with_meta]
    coll.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    return len(texts)


def query_chroma(query: str, top_k: int = TOP_K) -> list[str]:
    """Embed query, run similarity search, return list of document strings."""
    vectors = embed_with_ollama([query])
    if not vectors:
        return []
    client = get_client()
    coll = ensure_collection(client)
    n = coll.count()
    if n == 0:
        return []
    results = coll.query(query_embeddings=vectors, n_results=min(top_k, n))
    docs = results.get("documents")
    if not docs or not docs[0]:
        return []
    return list(docs[0])


def generate_with_ollama(prompt: str, system: str = None) -> str:
    """Build full prompt with optional system, call Ollama /api/generate, return response text."""
    full_prompt = prompt
    if system:
        full_prompt = f"{system}\n\nUse the following context to answer. Stay helpful and on-topic.\n\n{prompt}"
    url = f"{OLLAMA_HOST.rstrip('/')}/api/generate"
    try:
        r = requests.post(
            url,
            json={"model": OLLAMA_CHAT_MODEL, "prompt": full_prompt, "stream": False},
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        return (data.get("response") or "").strip()
    except requests.RequestException as e:
        raise RuntimeError(f"Ollama generate request failed: {e}") from e


def chat(message: str) -> str:
    """RAG pipeline: retrieve context from Chroma, then generate reply with Ollama."""
    context_chunks = query_chroma(message)
    context = "\n\n".join(context_chunks) if context_chunks else "(No relevant context found.)"
    prompt = f"Context:\n{context}\n\nQuestion: {message}"
    return generate_with_ollama(prompt, system=SYSTEM_PROMPT)
