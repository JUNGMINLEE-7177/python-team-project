# main.py – DeepFace 감정 분석 UI (emotion_check 모듈 연결)
import tkinter as tk
from tkinter import messagebox
import threading
import webbrowser
import os
import platform
import subprocess

from login import compare_webcam_to_image
from datasave import save_emotion_to_sheet
from emotion_check import analyze_emotion

# ---------------- 사용자 설정 ----------------
SHOW_WINDOW = True   # True → 웹캠 프리뷰 창 표시, False → 숨김
INTERVAL_SEC = 15    # 감정 분석 주기(초)
# ---------------------------------------------

class DeepFaceUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepFace 감정 분석 UI")
        self.root.geometry("400x300")

        self.running = False           # 감정 분석 스레드 실행 여부
        self.class_name = None         # 현재 수업명
        self.student_id = None         # 학번
        self.thread = None             # 분석 스레드
        self.stop_evt = None           # threading.Event → 루프 종료 신호

        # ---- 학번 입력 UI ----
        self.id_label = tk.Label(root, text="학번을 입력하세요:")
        self.id_label.pack(pady=10)

        self.id_entry = tk.Entry(root)
        self.id_entry.pack()

        self.check_button = tk.Button(root, text="확인", command=self.verify_student)
        self.check_button.pack(pady=10)

        # ---- 로그인 후 버튼 (처음엔 숨김) ----
        self.attend_button = tk.Button(root, text="수업 듣기", command=self.select_class, font=("Arial", 12))
        self.focus_button = tk.Button(root, text="집중도 분석 확인", command=self.show_focus_result, font=("Arial", 12))

    # ------------------------------------------
    # 1) 학번 입력 → 얼굴 인증
    # ------------------------------------------
    def verify_student(self):
        sid = self.id_entry.get().strip()
        if not sid:
            messagebox.showwarning("입력 오류", "학번을 입력하세요.")
            return

        if compare_webcam_to_image(sid):
            self.student_id = sid
            messagebox.showinfo("인식 성공", f"{sid} 학생 확인 완료")
            self.show_action_buttons()
        else:
            messagebox.showerror("인식 실패", "학생 사진과 일치하지 않습니다.")

    # ------------------------------------------
    # 2) 로그인 성공 → 액션 버튼 표시
    # ------------------------------------------
    def show_action_buttons(self):
        self.id_label.pack_forget()
        self.id_entry.pack_forget()
        self.check_button.pack_forget()

        self.attend_button.pack(pady=20)
        self.focus_button.pack(pady=10)

    # ------------------------------------------
    # 3) 강의 선택 팝업
    # ------------------------------------------
    def select_class(self):
        popup = tk.Toplevel(self.root)
        popup.title("수업 선택")
        popup.geometry("300x150")
        tk.Label(popup, text="수업을 선택하세요:", font=("Arial", 12)).pack(pady=10)

        tk.Button(popup, text="1강", command=lambda: self.start_class("1강", popup)).pack(pady=5)
        tk.Button(popup, text="2강", command=lambda: self.start_class("2강", popup)).pack(pady=5)
        tk.Button(popup, text="3강", command=lambda: self.start_class("3강", popup)).pack(pady=5)

    # ------------------------------------------
    # 4) 강의 시작 + 감정 분석 스레드 시작
    # ------------------------------------------
    def start_class(self, class_name: str, popup):
        self.class_name = class_name
        popup.destroy()

        youtube_links = {
            "1강": "https://www.youtube.com/watch?v=jPs3n9Vou9c",
            "2강": "https://www.youtube.com/watch?v=jPs3n9Vou9c",
            "3강": "https://www.youtube.com/watch?v=jPs3n9Vou9c",
        }
        url = youtube_links.get(class_name)
        if url:
            webbrowser.open(url)
        else:
            messagebox.showerror("오류", "링크가 없습니다.")
            return

        self.start_analysis_thread()

    # ------------------------------------------
    # 5) 감정 분석 스레드 관리
    # ------------------------------------------
    def start_analysis_thread(self):
        if self.running:
            return
        self.running = True
        self.stop_evt = threading.Event()

        self.thread = threading.Thread(target=self.run_analysis, daemon=True)
        self.thread.start()

        # 메인 창 최소화 & ⏸ 버튼 창 표시
        self.root.withdraw()
        self.show_stop_button()

    def run_analysis(self):
        def cb(minute: int, emo: str):
            save_emotion_to_sheet(self.student_id, self.class_name, minute, emo)
            print(f"[{minute}분] dominant_emotion = {emo}")

        analyze_emotion(
            cb,
            interval_sec=INTERVAL_SEC,
            show=SHOW_WINDOW,
            stop_event=self.stop_evt,
        )
        # analyze_emotion 리턴 → 루프 종료
        self.running = False

    # ------------------------------------------
    # 6) ⏸ 버튼으로 분석 중지
    # ------------------------------------------
    def stop_deepface(self):
        if self.stop_evt:
            self.stop_evt.set()  # 루프 종료 신호
        if self.stop_window:
            self.stop_window.destroy()
        self.root.deiconify()   # 메인 창 다시 보이기

    def show_stop_button(self):
        self.stop_window = tk.Toplevel()
        self.stop_window.overrideredirect(True)
        self.stop_window.attributes("-topmost", True)

        screen_w = self.stop_window.winfo_screenwidth()
        self.stop_window.geometry(f"40x30+{screen_w - 50}+10")

        tk.Button(self.stop_window, text="⏸", command=self.stop_deepface, width=3).pack()

    # ------------------------------------------
    # 7) CSV 결과 열기
    # ------------------------------------------
    def show_focus_result(self):
        csv_path = "emotion_summary.csv"
        if not os.path.isfile(csv_path):
            messagebox.showerror("파일 없음", f"{csv_path} 파일이 존재하지 않습니다.")
            return
        try:
            if platform.system() == "Windows":
                os.startfile(csv_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", csv_path])
            else:
                subprocess.call(["xdg-open", csv_path])
        except Exception as e:
            messagebox.showerror("실패", f"CSV 파일을 열 수 없습니다:\n{e}")

# ----------------------------------------------
# 실행 엔트리 포인트
# ----------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DeepFaceUI(root)
    root.mainloop()
