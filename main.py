from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query_model import Query
from utils import load_csv, load_jsonl
from doc_chunker import kag_semantic_pipeline
from food_filter import filter_foods
from embed_retrieve import search_chunks, generate_response, upload_chunks
import os

app = FastAPI()

# ✅ Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Paths to your files
csv_path = r"C:\Users\Gaurav sharan\Downloads\final_diet_dataset_with_hypertension_diabetes.csv"
jsonl_path = r"C:\Users\Gaurav sharan\Downloads\expanded_300_diet_guideline_dataset.jsonl"
docx_path = r"C:\Users\Gaurav sharan\Downloads\FoodData Central Foundation Foods Documentation.docx"

csv_data = load_csv(csv_path)
jsonl_chunks = load_jsonl(jsonl_path)
doc_chunks = kag_semantic_pipeline(docx_path)

if not os.path.exists("faiss_index.bin"):
    print("📤 Uploading chunks to FAISS (first time only)...")
    upload_chunks(jsonl_chunks + doc_chunks)
else:
    print("✅ FAISS index already exists. Skipping upload.")

@app.post("/recommend")
def recommend(query: Query):
    foods = filter_foods(csv_data, query.condition, query.allergies)
    reasoning = search_chunks(query.condition, query.allergies)
    summary = generate_response(query.condition, query.allergies, reasoning)
    return {
        "recommendations": foods,
        "reasoning_chunks": reasoning,
        "generated_summary": summary
    }
