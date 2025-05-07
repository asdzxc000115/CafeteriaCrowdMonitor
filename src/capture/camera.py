# src/capture/camera.py
#이미지 캡처 모듈
import cv2
import os
import datetime
from pathlib import Path

class CameraCapture:
    def __init__(self, camera_id=0, save_dir='temp_images'):
        """
        카메라 캡처 초기화
        """
        self.camera_id = camera_id
        self.save_dir = save_dir

        # 저장 디렉토리 생성
        os.makedirs(save_dir, exist_ok=True)

    def capture_image(self):
        """
        카메라에서 이미지 캡처
        """
        # 카메라 열기
        cap = cv2.VideoCapture(self.camera_id)

        if not cap.isOpened():
            print(f"카메라 {self.camera_id}를 열 수 없습니다.")
            return None

        # 이미지 캡처
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("이미지 캡처 실패")
            return None

        # 현재 시간으로 파일명 생성
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cafeteria_{timestamp}.jpg"
        filepath = os.path.join(self.save_dir, filename)

        # 이미지 저장
        cv2.imwrite(filepath, frame)
        print(f"이미지 캡처 및 저장 완료: {filepath}")

        return filepath

    def apply_privacy_protection(self, image_path):
        """
        이미지에 프라이버시 보호 처리 적용
        """
        # 이미지 로드
        image = cv2.imread(image_path)
        if image is None:
            print(f"이미지를 불러올 수 없습니다: {image_path}")
            return None

        # 이미지 해상도 낮추기 (50%)
        width = int(image.shape[1] * 0.5)
        height = int(image.shape[0] * 0.5)
        resized_image = cv2.resize(image, (width, height))

        # 이미지 저장
        processed_path = image_path.replace(".jpg", "_processed.jpg")
        cv2.imwrite(processed_path, resized_image)
        print(f"프라이버시 보호 처리 완료: {processed_path}")

        return processed_path