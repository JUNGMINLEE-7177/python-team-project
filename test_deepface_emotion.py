from deepface import DeepFace

result = DeepFace.analyze(
    img_path="a.jpg",
    actions=['emotion']
)

# 리스트의 첫 번째(그리고 보통 유일한) 얼굴 결과에 접근
face_data = result[0]

print("-----------------------------------------감정 분석 결과-----------------------------------------")
print("우세 감정:", face_data["dominant_emotion"])
print("감정 분포:", face_data["emotion"])
