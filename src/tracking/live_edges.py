import cv2
import mediapipe as mp
import numpy as np
import urllib.request
import os

MODEL_PATH = "selfie_segmenter.tflite"
if not os.path.exists(MODEL_PATH):
    print("A descarregar modelo...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/selfie_segmenter.tflite",
        MODEL_PATH
    )
    print("Modelo descarregado!")

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.ImageSegmenterOptions(
    base_options=base_options,
    output_confidence_masks=True 
)
segmentor = vision.ImageSegmenter.create_from_options(options)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = segmentor.segment(mp_image)
    mask = result.confidence_masks[0].numpy_view()  

    binary_mask = (mask > 0.5).astype(np.uint8) * 255  
    binary_mask = cv2.GaussianBlur(binary_mask, (5, 5), 0)

    edges = cv2.Canny(binary_mask, 50, 150)
    edges = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)

    output = np.zeros_like(frame)
    output[edges > 0] = (255, 255, 255)

    cv2.imshow("Outline", output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()