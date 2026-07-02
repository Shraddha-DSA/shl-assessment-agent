import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class RecommendationEngine:

    def __init__(self):
        self.client = client

    def recommend(self, query: str, retrieved_docs: list):

        catalog = []

        for doc in retrieved_docs:
            catalog.append({
                "name": doc["name"],
                "url": doc["url"],
                "description": doc["description"],
                "duration": doc["duration"],
                "job_levels": doc["job_levels"],
                "languages": doc["languages"],
                "remote": doc["remote"],
                "adaptive": doc["adaptive"]
            })

        prompt = f"""
You are an SHL Assessment Recommendation Expert.

The user request is:

{query}

You MUST use ONLY the assessments below.

Do NOT invent assessment names.
Do NOT invent URLs.

Recommend between 1 and 10 assessments.

For each recommendation explain WHY it is suitable.

Catalog:

{json.dumps(catalog, indent=2)}

Return ONLY valid JSON.

Example:

{{
    "reply": "...",
    "recommendations": [
        {{
            "name": "",
            "url": "",
            "reason": ""
        }}
    ]
}}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text


if __name__ == "__main__":

    from retriever import SHLRetriever

    retriever = SHLRetriever()
    engine = RecommendationEngine()

    query = input("Hiring Query: ")

    docs = retriever.retrieve(query, top_k=10)

    answer = engine.recommend(query, docs)

    print(answer)