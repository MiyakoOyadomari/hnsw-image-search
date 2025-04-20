from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from image_utils import preprocess_image
from search_engine import TileSearchEngine
import io
from PIL import Image

app = FastAPI()
engine = TileSearchEngine()

@app.post("/search")
async def search(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    query_vec = engine.extract_features(image)
    ids, distances = engine.query(query_vec, top_k=5)

    results = [
        {"image_path": engine.meta[str(idx)], "distance": float(dist)}
        for idx, dist in zip(ids, distances)
    ]
    return JSONResponse(content={"results": results})
