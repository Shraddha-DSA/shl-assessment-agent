import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


FAISS_INDEX_FILE = Path("catalog/faiss.index")
DOCUMENTS_FILE = Path("catalog/documents.pkl")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class SHLRetriever:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        print("Loading FAISS index...")

        self.index = faiss.read_index(str(FAISS_INDEX_FILE))

        print("Loading documents...")

        with open(DOCUMENTS_FILE, "rb") as f:
            self.documents = pickle.load(f)

        print(f"Loaded {len(self.documents)} assessments.")

    def retrieve(self, query: str, top_k: int = 10):

        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        ).reshape(1, -1)

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            doc = self.documents[idx].copy()
            doc["score"] = float(score)

            results.append(doc)

        return results


if __name__ == "__main__":

    retriever = SHLRetriever()

    query = input("Enter hiring query: ")

    results = retriever.retrieve(query)

    print("\nTop Recommendations\n")

    for i, doc in enumerate(results, start=1):

        print("=" * 60)
        print(f"{i}. {doc['name']}")
        print(f"Score      : {doc['score']:.4f}")
        print(f"Duration   : {doc['duration']}")
        print(f"Remote     : {doc['remote']}")
        print(f"Adaptive   : {doc['adaptive']}")
        print(f"URL        : {doc['url']}")