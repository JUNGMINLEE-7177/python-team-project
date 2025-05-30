from deepface import DeepFace
import cv2

result = DeepFace.verify(
    img1_path = "a.jpg",
    img2_path = "b.jpg",
    detector_backend = 'retinaface',  # 또는 'mtcnn', 'mediapipe'
)


print("-----------------------------------------결과확인-----------------------------------------")
print(result)