# login.py
import cv2
from deepface import DeepFace

def compare_webcam_to_image(student_id: str) -> bool:
    """
    웹캠에서 캡처한 얼굴과 students/{student_id}.jpg를 비교하여
    인증되면 True 반환.
    """
    reference_path = f"students/{student_id}.jpg"
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return False

    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("캡처 실패")
        return False

    try:
        result = DeepFace.verify(
            img1_path=frame,
            img2_path=reference_path,
            detector_backend='retinaface'
        )
        return result["verified"]
    except Exception as e:
        print("인증 중 오류:", e)
        return False
