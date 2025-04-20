import os
from duckduckgo_search import DDGS
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

query = "ceramic tile glaze glossy matte color texture"
output_dir = "tiles_raw"
os.makedirs(output_dir, exist_ok=True)

with DDGS() as ddgs:
    results = ddgs.images(query, max_results=100)

metadata = []

for i, result in enumerate(tqdm(results)):
    url = result["image"]
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            
            # Save image
            filename = f"tile_{i:03}.jpg"
            img.save(os.path.join(output_dir, filename))
            
            # Save metadata
            metadata.append({"filename": filename, "url": url})
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Save metadata to a JSON file
import json
with open(os.path.join(output_dir, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=4)
