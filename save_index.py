import os
import numpy as np
import hnswlib
import json
from PIL import Image
from image_utils import preprocess_image
import open_clip
import torch

tiles_dir = "tiles/"
index_dir = "index/"
os.makedirs(index_dir, exist_ok=True)

model, _, _ = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
model.eval()

filenames = sorted([f for f in os.listdir(tiles_dir) if f.endswith((".jpg", ".png"))])
features = []
meta = {}

for idx, fname in enumerate(filenames):
    path = os.path.join(tiles_dir, fname)
    img = Image.open(path).convert("RGB")
    tensor = preprocess_image(img).unsqueeze(0)
    with torch.no_grad():
        feat = model.encode_image(tensor)
        feat = feat / feat.norm(dim=-1, keepdim=True)
    features.append(feat.squeeze(0).cpu().numpy())
    meta[idx] = path

features_np = np.vstack(features)

index = hnswlib.Index(space='cosine', dim=512)
index.init_index(max_elements=len(features_np), ef_construction=100, M=16)
index.add_items(features_np, list(meta.keys()))
index.save_index(os.path.join(index_dir, "index.bin"))

with open(os.path.join(index_dir, "meta.json"), 'w') as f:
    json.dump(meta, f)

print("Index and meta saved.")
