from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import io
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

CLASSES = ["airplane", "automobile", "bird", "cat", "deer",
           "dog", "frog", "horse", "ship", "truck"]



class CifarClassification(nn.Module):
    def __init__(self):
        super().__init__()
        self.first = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),   # 0
            nn.ReLU(),                                     # 1
            nn.MaxPool2d(2),                                # 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),   # 3
            nn.ReLU(),                                     # 4
            nn.MaxPool2d(2),                                # 5
            nn.Conv2d(64, 128, kernel_size=3, padding=1),  # 6
            nn.ReLU(),                                     # 7
            nn.MaxPool2d(2),                                # 8
        )
        self.second = nn.Sequential(
            nn.Flatten(),                                   # 0
            nn.Linear(128 * 4 * 4, 256),                    # 1
            nn.ReLU(),                                      # 2
            nn.Linear(256, 10),                              # 3
        )

    def forward(self, x):
        x = self.first(x)
        x = self.second(x)
        return x


transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor()
])

cifar_router = APIRouter(prefix="/cifar", tags=["CIFAR10"])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# check_file.py: mysite/api/check_file.py -> .parent (api/) -> .parent (mysite/)
# модель mysite/nn_models/modelC.pth жайгашкан
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model2_path"


if MODEL_PATH.exists():
    sd = torch.load(MODEL_PATH, map_location="cpu")
    for k, v in sd.items():
        print(k, tuple(v.shape))

model = CifarClassification()
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()


@cifar_router.post("/predict")
async def predict(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Image can't be empty")

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_tensor = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            y_pred = model(img_tensor)
            pred = y_pred.argmax(dim=1).item()

        predicted_class = CLASSES[pred]

        if predicted_class == "airplane":
            return {"Answer": predicted_class, "detail": "Мындай сүрөттү жүктөөгө болбойт"}
        elif predicted_class == "automobile":
            return {"Answer": predicted_class, "detail": "Мындай сүрөттү жүктөөгө болбойт"}
        elif predicted_class == "bird":
            return {"Answer": predicted_class, "detail": "Мындай сүрөттү жүктөөгө болбойт"}
        else:
            return {"Answer": predicted_class}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
