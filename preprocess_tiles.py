import os
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

input_dir = "tiles_raw"
output_dir = "tiles"
os.makedirs(output_dir, exist_ok=True)

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224)
])

for fname in tqdm(os.listdir(input_dir)):
    if not fname.lower().endswith((".jpg", ".png")):
        print(f"Unsupported file format: {fname}")
        continue
    try:
        img = Image.open(os.path.join(input_dir, fname))
        
        # カラーモードのチェックと変換
        if img.mode != "RGB":
            if img.mode == "L":  # グレースケール
                img = img.convert("RGB")
            else:
                print(f"Unsupported color mode ({img.mode}) in file: {fname}")
                continue
        
        img = transform(img)
        img.save(os.path.join(output_dir, fname))
    except Exception as e:
        print(f"Failed to process {fname}: {e}")
