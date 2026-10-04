import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
import os
import tempfile

network_app = FastAPI(title="Хештек YOLO11")

model = YOLO('yolo11n.pt')


def detect_labels(frame, labels_set):
    """Прогоняет изображение/кадр через YOLO и добавляет найденные классы в set (уникальные)."""
    results = model(frame)
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            labels_set.add(label)


@network_app.post("/predict")
async def predict_objects(file: UploadFile = File(...)):

    contents = await file.read()
    labels_set = set()

    if file.content_type.startswith("image/"):
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Не удалось декодировать изображение")

        detect_labels(image, labels_set)

    objects = [f'#{label}' for label in labels_set]

    return objects
@network_app.post("/predict-video")
async def predict_objects(file: UploadFile = File(...)):
    contents = await file.read()
    labels_set = set()
    if file.content_type.startswith("video/"):
        suffix = os.path.splitext(file.filename)[1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        try:
            cap = cv2.VideoCapture(tmp_path)

            if not cap.isOpened():
                raise HTTPException(status_code=400, detail="Не удалось открыть видео")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                detect_labels(frame, labels_set)

            cap.release()

        finally:
            os.remove(tmp_path)

    else:
        raise HTTPException(status_code=400, detail="Файл должен быть изображением или видео")

    objects = [f'#{label}' for label in labels_set]

    return objects