# datasave.py
import csv
import os

CSV_PATH = "emotion_summary.csv"
HEADER = ["학번", "수업명", "분", "dominant_emotion"]

def save_emotion_to_sheet(student_id, class_name, minute, emotion):
    new_file = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(HEADER)
        writer.writerow([student_id, class_name, minute, emotion])
