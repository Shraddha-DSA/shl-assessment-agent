import json
import re
import requests

URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

RAW_FILE = "catalog/catalog_raw.json"
OUTPUT_FILE = "catalog/catalog.json"


def repair_json(text: str) -> str:
    """
    Replace illegal control characters that break JSON parsing.
    Keeps normal whitespace intact.
    """
    return re.sub(
        r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
        "",
        text
    )


def download_catalog():

    print("Downloading catalog...")

    response = requests.get(URL, timeout=60)
    response.raise_for_status()

    raw_text = response.text

    with open(RAW_FILE, "w", encoding="utf-8") as f:
        f.write(raw_text)

    print("Raw catalog saved.")

    repaired_text = repair_json(raw_text)

    data = json.loads(repaired_text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\nDownloaded {len(data)} assessments.")
    print(f"Saved cleaned catalog to {OUTPUT_FILE}")


if __name__ == "__main__":
    download_catalog()