import cv2
import mediapipe as mp
import numpy as np

# MediaPipe setup (landmarks e pose estimation)
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

model_path = "pose_landmarker.task"

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)

pose_landmarker = PoseLandmarker.create_from_options(options)

# Função ângulo
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    denom = np.linalg.norm(ba) * np.linalg.norm(bc)
    if denom == 0:
        return None

    cosine_angle = np.dot(ba, bc) / denom
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    angle = np.degrees(np.arccos(cosine_angle))
    return angle

# Ligações do esqueleto
connections = [
    (11, 13), (13, 15),  # braço esquerdo
    (12, 14), (14, 16),  # braço direito
    (11, 12),
    (11, 23), (12, 24),
    (23, 24),
    (23, 25), (25, 27),
    (24, 26), (26, 28)
]

# Webcam
cap = cv2.VideoCapture(0)
timestamp = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = pose_landmarker.detect_for_video(mp_image, timestamp)
    timestamp += 1

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]

        # converter para pixels
        points = []
        for lm in landmarks:
            x = int(lm.x * w)
            y = int(lm.y * h)
            points.append((x, y))

        # desenhar pontos
        for (x, y) in points:
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

        #  desenhar ligações
        for start, end in connections:
            cv2.line(frame, points[start], points[end], (255, 0, 0), 2)

        # BRAÇO DIREITO (12,14,16)
        if (landmarks[12].visibility > 0.5 and
            landmarks[14].visibility > 0.5 and
            landmarks[16].visibility > 0.5):

            angle_r = calculate_angle(points[12], points[14], points[16])

            if angle_r is not None:
                cv2.putText(frame, f"R: {int(angle_r)}",
                            points[14],
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 255), 2)

        # BRAÇO ESQUERDO (11,13,15)
        if (landmarks[11].visibility > 0.5 and
            landmarks[13].visibility > 0.5 and
            landmarks[15].visibility > 0.5):

            angle_l = calculate_angle(points[11], points[13], points[15])

            if angle_l is not None:
                cv2.putText(frame, f"L: {int(angle_l)}",
                            points[13],
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 255, 0), 2)

    cv2.imshow("Skeleton + Angles", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()