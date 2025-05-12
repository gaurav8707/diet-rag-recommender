from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def keyword_chunk_docx(path, min_len=100):
    doc = Document(path)
    return [p.text.strip() for p in doc.paragraphs if len(p.text.strip()) >= min_len]

def merge_semantic_chunks(chunks, sim_threshold=0.75):
    embeddings = model.encode(chunks)
    final_chunks = []
    buffer = chunks[0]
    prev_embed = embeddings[0]
    for i in range(1, len(chunks)):
        sim = cosine_similarity([prev_embed], [embeddings[i]])[0][0]
        if sim >= sim_threshold:
            buffer += " " + chunks[i]
        else:
            final_chunks.append(buffer)
            buffer = chunks[i]
        prev_embed = embeddings[i]
    final_chunks.append(buffer)
    return final_chunks

def tag_chunk(text):
    keyword_map = {
        "sodium": "hypertension", "salt": "hypertension", "fiber": "diabetes",
        "glucose": "diabetes", "sugar": "diabetes", "cholesterol": "cholesterol",
        "iron": "anemia", "vitamin a": "deficiency", "vitamin d": "bone health",
        "potassium": "blood pressure", "protein": "muscle", "fat": "obesity",
        "omega-3": "heart health", "calcium": "bones", "magnesium": "blood sugar",
        "zinc": "immunity", "folate": "pregnancy", "lactose": "dairy allergy",
        "milk": "dairy allergy", "nuts": "nut allergy", "soy": "soy allergy",
        "shellfish": "seafood allergy", "celiac": "gluten", "gluten": "gluten",
        "gout": "uric acid", "anemia": "anemia", "kidney": "renal health",
        "liver": "liver health", "obesity": "obesity", "diarrhea": "gut health"
    }
    return list({v for k, v in keyword_map.items() if k in text.lower()})

def kag_semantic_pipeline(path):
    raw = keyword_chunk_docx(path)
    merged = merge_semantic_chunks(raw)
    return [{"text": ch, "tags": tag_chunk(ch), "source": "USDA Word Doc"} for ch in merged]
