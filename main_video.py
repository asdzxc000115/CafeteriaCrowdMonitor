# main_video.py
# 비디오로 테스트하는 메인 서버
import os
import sys
import time
import schedule
from datetime import datetime
import threading

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 모듈 임포트
from src.capture.camera import CameraCapture
from src.detection.yolo_detector import YOLODetector
from src.database.operations import save_crowd_data, get_settings
from src.utils.cleanup import cleanup_old_images
from src.database.models import init_db

# 전역 변수
YOLO_WEIGHTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yolov7.pt')

# 비디오 소스 설정
VIDEO_SOURCES = {
    '학생식당': 'videos/cafeteria.mp4',
    '3호관 스터디룸': 'videos/studyroom.mp4',  # 이 파일이 없으면 cafeteria.mp4 사용
}

# 카메라 객체 전역 관리 (각 장소별로 유지)
cameras = {}

def process_capture(place_name='학생식당'):
    """
    비디오에서 주기적으로 이미지를 캡처하고 처리하는 함수
    """
    print(f"[{datetime.now()}] {place_name} 이미지 캡처 및 처리 시작...")

    # 설정 가져오기
    settings = get_settings()
    if not settings:
        print("설정을 가져올 수 없습니다. 기본값 사용.")
        max_capacity = 100
        image_retention_hours = 24
    else:
        max_capacity = settings.max_capacity
        image_retention_hours = settings.image_retention_hours

    # 비디오 소스 가져오기
    video_source = VIDEO_SOURCES.get(place_name, VIDEO_SOURCES['학생식당'])

    # 카메라 객체 가져오기 또는 생성 (재사용)
    if place_name not in cameras:
        cameras[place_name] = CameraCapture(source=video_source, is_video=True)
        print(f"{place_name}용 새 비디오 객체 생성")

    camera = cameras[place_name]
    image_path = camera.capture_image()

    if image_path:
        # 프라이버시 보호 처리
        processed_image = camera.apply_privacy_protection(image_path)

        if processed_image:
            # YOLOv7로 사람 수 카운팅
            detector = YOLODetector(weights=YOLO_WEIGHTS)
            people_count = detector.count_people(processed_image)

            # 데이터베이스에 저장 (장소 이름 포함)
            save_crowd_data(people_count, place_name=place_name)

            print(f"[{datetime.now()}] {place_name} 처리 완료: {people_count}명 탐지됨")

    # 오래된 이미지 정리
    cleanup_old_images(hours=image_retention_hours)

def process_all_places():
    """
    모든 장소 처리
    """
    for place_name in VIDEO_SOURCES.keys():
        process_capture(place_name)

def start_api_server():
    """
    API 서버를 별도 스레드로 실행
    """
    from src.api.server import start_server
    start_server(host='0.0.0.0', port=5001, debug=False)

def main():
    """
    메인 함수
    """
    print("대학교 혼잡도 모니터링 시스템 시작 (비디오 모드)")

    # 데이터베이스 초기화
    init_db()

    # API 서버 시작 (별도 스레드)
    server_thread = threading.Thread(target=start_api_server)
    server_thread.daemon = True
    server_thread.start()

    # 설정 가져오기
    settings = get_settings()
    if not settings:
        print("설정을 가져올 수 없습니다. 기본값 사용.")
        capture_interval = 30  # 비디오 테스트는 30초로 짧게
    else:
        capture_interval = 30  # 비디오 테스트는 30초로 짧게

    # 캡처 및 처리 스케줄링 (초 단위로 변환)
    capture_interval_seconds = capture_interval
    schedule.every(capture_interval_seconds).seconds.do(process_all_places)

    print(f"캡처 간격: {capture_interval_seconds}초")

    # 시작 시 한 번 실행
    process_all_places()

    # 메인 루프
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()