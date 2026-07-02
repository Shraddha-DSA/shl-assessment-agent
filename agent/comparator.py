import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class Comparator:

    def __init__(self):
        self.client = client

    def compare(self, query: str, retrieved_docs: list):

        catalog = []

        for doc in retrieved_docs:
            catalog.append({
                "name": doc["name"],
                "description": doc["description"],
                "duration": doc["duration"],
                "job_levels": doc["job_levels"],
                "languages": doc["languages"],
                "remote": doc["remote"],
                "adaptive": doc["adaptive"],
                "url": doc["url"]
            })

        prompt = f"""
You are an SHL Assessment expert.

The user asked:

{query}

Use ONLY the assessments provided below.

Do NOT invent assessment names.
Do NOT invent URLs.
Do NOT use outside knowledge.

Assessments:

{json.dumps(catalog, indent=2)}

Compare the relevant assessments.

For each assessment explain:
- Purpose
- Skills measured
- Target job levels
- Duration
- Remote support
- Adaptive support
- When it should be used

Return ONLY valid JSON.

Example:

{{
    "reply": "Comparison of the requested assessments.",
    "comparisons": [
        {{
            "name": "",
            "url": "",
            "purpose": "",
            "skills": "",
            "job_levels": "",
            "duration": "",
            "remote": "",
            "adaptive": "",
            "when_to_use": ""
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
    comparator = Comparator()

    query = input("Compare Query: ")

    docs = retriever.retrieve(query, top_k=10)

    result = comparator.compare(query, docs)

    print(result)