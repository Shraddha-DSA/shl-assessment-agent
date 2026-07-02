import json


INPUT_FILE = "catalog/catalog_raw.json"
OUTPUT_FILE = "catalog/catalog.json"


def clean_text(text):
    """Convert None to empty string and strip whitespace."""
    if text is None:
        return ""
    return str(text).replace("\n", " ").replace("\r", " ").strip()


def preprocess():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} assessments.")

    seen = set()
    cleaned = []

    for item in data:

        name = clean_text(item.get("name"))

        if name.lower() in seen:
            continue

        seen.add(name.lower())

        assessment = {
            "entity_id": item.get("entity_id"),
            "name": name,
            "url": clean_text(item.get("link")),
            "description": clean_text(item.get("description")),
            "duration": clean_text(item.get("duration")),
            "remote": clean_text(item.get("remote")),
            "adaptive": clean_text(item.get("adaptive")),
            "job_levels": item.get("job_levels", []),
            "languages": item.get("languages", []),
            "test_types": item.get("test_types", []),
        }

        searchable_text = f"""
Assessment Name:
{name}

Description:
{assessment['description']}

Job Levels:
{", ".join(assessment["job_levels"])}

Languages:
{", ".join(assessment["languages"])}

Duration:
{assessment["duration"]}

Remote Testing:
{assessment["remote"]}

Adaptive Testing:
{assessment["adaptive"]}

URL:
{assessment["url"]}
"""

        assessment["searchable_text"] = searchable_text.strip()

        cleaned.append(assessment)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(cleaned)} cleaned assessments.")


if __name__ == "__main__":
    preprocess()