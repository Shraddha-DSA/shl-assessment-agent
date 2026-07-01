import pickle

import faiss
from sentence_transformers import SentenceTransformer


INDEX_PATH = "catalog/faiss.index"
DOCUMENTS_PATH = "catalog/documents.pkl"

MODEL_NAME = "all-MiniLM-L6-v2"


class SHLRetriever:

    def __init__(self):

        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

        print("Loading FAISS index...")
        self.index = faiss.read_index(INDEX_PATH)

        print("Loading documents...")

        with open(DOCUMENTS_PATH, "rb") as f:
            self.documents = pickle.load(f)

        print(f"Loaded {len(self.documents)} assessments.")

    def retrieve(self, query, top_k=5):

        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = query_embedding.reshape(1, -1)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            assessment = self.documents[idx].copy()

            assessment["score"] = float(score)

            results.append(assessment)

        return results


if __name__ == "__main__":

    retriever = SHLRetriever()

    query = input("Enter hiring query: ")

    results = retriever.retrieve(query)

    print("\nTop Recommendations\n")

    for i, result in enumerate(results, start=1):

        print("=" * 60)

        print(f"{i}. {result['name']}")

        print(f"Score : {result['score']:.4f}")

        print(f"Duration : {result['duration']}")

        print(f"Remote : {result['remote']}")

        print(f"Adaptive : {result['adaptive']}")

        print(f"URL : {result['url']}")