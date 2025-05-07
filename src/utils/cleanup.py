# src/utils/cleanup.py
#유틸리티 모듈
import os
import datetime
from pathlib import Path

def cleanup_old_images(image_dir="temp_images", hours=24):
    """
    지정된 시간보다 오래된 이미지 파일 자동 삭제
    """
    # 현재 시간
    now = datetime.datetime.now()

    # 디렉토리 경로 확인
    if not os.path.exists(image_dir):
        print(f"디렉토리가 존재하지 않습니다: {image_dir}")
        return

    # 삭제 기준 시간
    threshold = now - datetime.timedelta(hours=hours)
    count = 0

    # 디렉토리 내 모든 파일 검사
    for filename in os.listdir(image_dir):
        if filename.endswith('.jpg'):
            file_path = os.path.join(image_dir, filename)

            # 파일 생성 시간 확인
            file_creation_time = datetime.datetime.fromtimestamp(
                os.path.getctime(file_path)
            )

            # 기준 시간보다 오래된 파일 삭제
            if file_creation_time < threshold:
                os.remove(file_path)
                count += 1

    if count > 0:
        print(f"{count}개의 오래된 이미지 파일이 삭제되었습니다.")