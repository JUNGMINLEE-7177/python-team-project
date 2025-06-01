# emotion_check.py – 웹캠 감정 분석 모듈 (분리형)
"""
analyze_emotion(callback, interval_sec=15, show=True, stop_event=None)

Args:
    callback: (elapsed_minute:int, dominant_emotion:str) 를 인자로 받는 함수
    interval_sec: 분석 주기 (초)
    show: True → 프리뷰 창 표시 / False → 창 숨김
    stop_event: threading.Event; set() 되면 루프를 즉시 종료

사용 예 (main.py 내):
    from emotion_check import analyze_emotion
    stop_evt = threading.Event()

    def cb(minute, emo):
        save_emotion_to_sheet(...)

    threading.Thread(target=analyze_emotion,
                     args=(cb,),
                     kwargs={"interval_sec": 15, "show": SHOW_WINDOW, "stop_event": stop_evt},
                     daemon=True).start()

    # 중지 시 stop_evt.set()
"""
import cv2
import time
from typing import Callable, Optional
from deepface import DeepFace

def analyze_emotion(
    callback: Callable[[int, str], None],
    interval_sec: int = 15,
    show: bool = True,
    stop_event: Optional[object] = None,
):
    """웹캠에서 interval_sec 주기로 얼굴 감정을 분석하고 callback으로 전달한다."""

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    start_time = time.time()
    last_time = start_time - interval_sec  # 즉시 첫 분석 수행

    while True:
        # 외부 중지 신호 확인
        if stop_event is not None and stop_event.is_set():
            break

        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        if now - last_time >= interval_sec:
            elapsed_minute = int((now - start_time) // 60)
            try:
                result = DeepFace.analyze(
                    frame,
                    actions=["emotion"],
                    enforce_detection=False,
                )
                if isinstance(result, list):
                    result = result[0]
                dominant = result.get("dominant_emotion", "unknown")
                callback(elapsed_minute, dominant)
            except Exception as e:
                print("감정 분석 오류:", e)
            last_time = now

        if show:
            cv2.imshow("Emotion Check (ESC to quit)", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    if show:
        cv2.destroyAllWindows()
