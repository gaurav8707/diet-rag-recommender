import os
import faiss
import pickle
import numpy as np
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Load sentence transformer model (768-dim embedding)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# FAISS index and metadata paths
INDEX_PATH = "faiss_index.bin"
META_PATH = "faiss_meta.pkl"

# Load or create FAISS index and metadata
if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
else:
    index = faiss.IndexFlatL2(768)
    metadata = []

# Generate embedding
def get_embedding(text):
    return model.encode([text])[0]

# Upload new chunks to FAISS
def upload_chunks(chunks):
    global metadata
    embeddings = [get_embedding(ch["text"]) for ch in chunks]
    index.add(np.array(embeddings))
    metadata.extend([
        {"text": ch["text"], "tags": ch["tags"], "source": ch["source"]}
        for ch in chunks
    ])
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)
    print(f"✅ Stored {len(chunks)} chunks in FAISS")

# Search FAISS for top-k related chunks
def search_chunks(condition, allergies, top_k=5):
    query = f"{condition} {' '.join(allergies)}"
    emb = get_embedding(query).reshape(1, -1)
    D, I = index.search(emb, top_k)
    return [metadata[i]["text"] for i in I[0]]

# Generate summary using Groq's LLaMA 3 70B model
def generate_response(condition, allergies, reasoning_chunks):
    context = "\n".join(reasoning_chunks[:5])  # Limit chunk context

    prompt = f"""You are a clinical nutrition assistant AI.

A patient presents with the following condition: {condition}.
They are allergic to: {', '.join(allergies)}.

Based on the dietary guidance below, provide a concise 2–3 sentence dietary recommendation that avoids the allergens and supports the condition.

Dietary guidance:
{context}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful dietary assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Groq API error: {str(e)}"
