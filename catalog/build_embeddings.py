import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


CATALOG_FILE = Path("catalog/catalog.json")
FAISS_INDEX_FILE = Path("catalog/faiss.index")
DOCUMENTS_FILE = Path("catalog/documents.pkl")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 32


def load_catalog():
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def build_embeddings():

    print("=" * 60)
    print("Loading catalog...")
    assessments = load_catalog()

    print(f"Loaded {len(assessments)} assessments.")

    print("\nLoading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = []

    for assessment in assessments:
        texts.append(assessment["searchable_text"])

    print("\nGenerating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    dimension = embeddings.shape[1]

    print(f"\nEmbedding Dimension : {dimension}")

    print("\nBuilding FAISS Index...")

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print("Saving FAISS index...")

    faiss.write_index(index, str(FAISS_INDEX_FILE))

    print("Saving documents...")

    with open(DOCUMENTS_FILE, "wb") as f:
        pickle.dump(assessments, f)

    print("\n" + "=" * 60)
    print("Embedding Pipeline Completed Successfully")
    print("=" * 60)
    print(f"Total Documents : {len(assessments)}")
    print(f"Embedding Size  : {dimension}")
    print(f"Index File      : {FAISS_INDEX_FILE}")
    print(f"Documents File  : {DOCUMENTS_FILE}")
    print("=" * 60)



if __name__ == "__main__":
    build_embeddings()