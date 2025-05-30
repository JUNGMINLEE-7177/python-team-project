import face_recognition

# 이미지 로드 및 얼굴 인식
image = face_recognition.load_image_file("a.jpg")
face_encodings = face_recognition.face_encodings(image)

# 비교할 이미지
unknown_image = face_recognition.load_image_file("b.jpg")
unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

# 얼굴 비교
results = face_recognition.compare_faces([face_encodings[0]], unknown_face_encoding)
if results[0]:
    print("이 얼굴은 같은 사람입니다.")
else:
    print("이 얼굴은 다른 사람입니다.")