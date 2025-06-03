# test_video_simple.py
import cv2
import os

video_path = 'videos/cafeteria.mp4'
output_dir = 'test_frames'
os.makedirs(output_dir, exist_ok=True)

# 비디오 열기
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"비디오를 열 수 없습니다: {video_path}")
    exit(1)

# 비디오 정보
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"비디오 정보: {fps}fps, 총 {total_frames}프레임")

# 10초마다 프레임 캡처 (fps * 10)
frame_interval = fps * 10
frame_count = 0
capture_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("비디오 끝에 도달")
        break

    # 10초마다 캡처
    if frame_count % frame_interval == 0:
        filename = f"frame_{capture_count}_at_{frame_count}.jpg"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, frame)
        print(f"프레임 {frame_count} 캡처: {filename}")
        capture_count += 1

        # 10개만 캡처하고 종료
        if capture_count >= 10:
            break

    frame_count += 1

cap.release()
print(f"총 {capture_count}개 프레임 캡처 완료")