from deepface import DeepFace

# 이미지 파일 경로를 img_path로 지정합니다.
result = DeepFace.analyze(
    img_path="a.jpg",
    actions=['age', 'gender', 'race', 'emotion']
)

print("-----------------------------------------결과확인-----------------------------------------")
print(result)
