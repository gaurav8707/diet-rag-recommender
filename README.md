# 🧠 NutriGuard: AI-Powered Personalized Dietary Recommendation System

NutriGuard is an AI-powered dietary assistant that provides personalized food recommendations based on medical conditions and allergies, using semantic search and Groq's LLaMA-3 model.

---

## 📊 Project Overview

The NutriGuard system processes a user query like:

```json
{
  "condition": "type 2 diabetes with hypertension",
  "allergies": ["dairy", "nuts"]
}
```

And returns:

* ✅ 10 Safe food items
* 💬 5 Relevant knowledge chunks from USDA or expert tips
* 🧠 A concise AI-generated summary using Groq LLaMA-3

---

## 🖼 User Interface

Below is a screenshot of the NutriGuard user interface:

![image](https://github.com/user-attachments/assets/239d4b72-09df-4010-8046-e136be1e419b)


## ⚙️ Tech Stack

| Layer        | Tool/Service                                                                                             |
| ------------ | -------------------------------------------------------------------------------------------------------- |
| Backend      | FastAPI                                                                                                  |
| Frontend     | React (Next.js, CSS-only styling) \[CORS-ready]                                                          |
| Embedding    | SentenceTransformer (all-mpnet)                                                                          |
| Vector Store | FAISS (Facebook AI Similarity Search)                                                                    |
| LLM API      | Groq LLaMA-3 70B                                                                                         |
| Data Input   | CSV (Food DB), JSONL (Expert Tips), DOCX (curated from USDA, EatRight.org, and Harvard Nutrition Source) |
| Styling      | CSS only (custom styling)                                                                                |

---

## 🔐 Environment Variables

Place these in a `.env` file for backend use:

```env
GROQ_API_KEY=<your_groq_api_key_here>
```

---

## 🧪 Sample Output

```json
{
  "recommendations": [
    {"Food Name": "Kale, raw", "Category": "Vegetables"},
    {"Food Name": "Brown rice", "Category": "Grains"}
  ],
  "reasoning_chunks": [
    "The DASH diet supports hypertension management...",
    "Diabetic patients benefit from low GI, fiber-rich foods..."
  ],
  "generated_summary": "Focus on whole grains, greens, and legumes while avoiding dairy and processed sugar."
}
```

---

## 🧱 Folder Structure

```
diet-rag/
├── main.py                  # FastAPI app entrypoint
├── utils.py                 # Loaders, duplicate remover
├── doc_chunker.py           # KAG chunking pipeline
├── embed_retrieve.py        # Embedding, FAISS (Facebook AI Similarity Search), Groq API logic
├── food_filter.py           # Condition/allergy filtering logic
├── query_model.py           # Pydantic schema for input validation
├── requirements.txt         # Python dependencies
├── .env                     # API key (excluded from Git)
│
├── faiss_index.bin          # Vector DB (auto-generated)
├── faiss_meta.pkl           # Chunk metadata
├── final_diet_dataset.csv   # Master food dataset (local only)
├── expanded_300_diet_guideline_dataset.jsonl  # Expert JSON chunks
├── FoodData_Central.docx    # USDA food guidance document
└── frontend/                # React frontend code (optional)
```

---

## 🚀 Running the App Locally

### 🔧 Backend Setup

```bash
git clone https://github.com/yourusername/diet-rag.git
cd diet-rag

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

### 🔍 Access API Docs

Open [http://localhost:8000/docs](http://localhost:8000/docs) to test the API via Swagger UI.

---

### 💻 Frontend Setup (Next.js)

Navigate to your frontend directory (if applicable):

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Visit your frontend app at: [http://localhost:3000](http://localhost:3000)

Ensure the frontend connects to the backend API URL correctly in your React config or environment.

---

## ⚠️ Challenges Faced

* **Duplicate reasoning**: Solved using deduplication logic before summary generation.
* **CORS issues**: Resolved via FastAPI middleware for smooth frontend integration.
* **Vector size optimization**: Controlled chunk merging using cosine similarity thresholds.

---

## 🔮 Future Enhancements

* 🍱 Integrate dynamic meal planning (macros + quantities).
* 🏥 Sync with electronic medical records (EMR) for real-world use.
* 🧬 Add multi-lingual support and speech-based input.
* 📈 Incorporate nutritional scoring (Glycemic Load, Heart-Healthy Index, etc.).

---

## 📚 Data Sources

NutriGuard uses various trusted data sources to extract and enrich nutritional knowledge, including:

* [PubMed](https://pubmed.ncbi.nlm.nih.gov/) – Biomedical and clinical literature
* [USDA FoodData Central](https://fdc.nal.usda.gov/) – Nutritional data from official food databases
* [EatRight.org – Academy of Nutrition and Dietetics](https://www.eatright.org/) – Expert articles and dietary guidelines
* [Harvard T.H. Chan Nutrition Source](https://nutritionsource.hsph.harvard.edu/) – Evidence-based nutrition recommendations

---

## 🧠 Built With

* **FastAPI** – Lightweight backend API framework
* **FAISS (Facebook AI Similarity Search)** – Efficient vector search
* **Sentence-Transformers** – Text embeddings (`all-mpnet-base-v2`)
* **Groq AI** – LLaMA 3 (70B) for concise summarization
* **Pandas** – Data handling for filtering
* **Python-Docx** – DOCX parsing and extraction

---
