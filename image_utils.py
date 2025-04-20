from PIL import Image
import torchvision.transforms as T
import torch

def preprocess_image(image: Image.Image):
    transform = T.Compose([
        T.Resize(224),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                    std=[0.26862954, 0.26130258, 0.27577711])
    ])
    return transform(image)
