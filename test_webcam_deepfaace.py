import cv2
from deepface import DeepFace

def main():
    # 0번 장치(기본 웹캠) 연결
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # DeepFace로 프레임 단위 얼굴 분석
        try:
            result = DeepFace.analyze(
                frame,
                actions=['age', 'gender', 'emotion'],  # 분석할 항목
                enforce_detection=False                 # 얼굴이 없을 때 에러 방지
            )
            # 결과 출력 (프레임 상단에 텍스트로)
            info = f"{result['dominant_emotion']}, {result['age']}, {result['gender']}"
            cv2.putText(frame, info, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        except Exception as e:
            # 얼굴 인식 실패 시 그냥 넘어감
            pass

        # 화면에 보여주기
        cv2.imshow("DeepFace Webcam", frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
