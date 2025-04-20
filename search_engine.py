import hnswlib
import numpy as np
import torch
import open_clip
import json
from image_utils import preprocess_image

class TileSearchEngine:
    def __init__(self, index_path="index/index.bin", meta_path="index/meta.json"):
        # モデルロード（CLIP ViT-B/32）
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
        self.tokenizer = open_clip.get_tokenizer('ViT-B-32')
        self.model.eval()

        # インデックスロード
        self.index = hnswlib.Index(space='cosine', dim=512)
        self.index.load_index(index_path)
        
        with open(meta_path, 'r') as f:
            self.meta = json.load(f)

    def extract_features(self, image):
        image_tensor = preprocess_image(image).unsqueeze(0)  # (1, 3, 224, 224)
        with torch.no_grad():
            embedding = self.model.encode_image(image_tensor)
            embedding /= embedding.norm(dim=-1, keepdim=True)
        return embedding.squeeze(0).cpu().numpy()

    def query(self, vec, top_k=5):
        labels, distances = self.index.knn_query(vec, k=top_k)
        return labels[0], distances[0]
