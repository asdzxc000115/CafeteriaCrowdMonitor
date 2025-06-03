# # main.py
# #메인 애플리케이션
# import os
# import sys
# import time
# import schedule
# from datetime import datetime
# import threading
#
# # 모듈 경로 추가
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# # 모듈 임포트
# from src.capture.camera import CameraCapture
# from src.detection.yolo_detector import YOLODetector
# from src.database.operations import save_crowd_data, get_settings
# from src.utils.cleanup import cleanup_old_images
# from src.database.models import init_db
#
# # 전역 변수
# CAMERA_ID = 0  # 카메라 ID (필요시 변경)
# YOLO_WEIGHTS = os.path.join('yolov7', 'yolov7.pt')  # YOLOv7 모델 경로
#
# def process_capture():
#     """
#     주기적으로 이미지를 캡처하고 처리하는 함수
#     """
#     print(f"[{datetime.now()}] 이미지 캡처 및 처리 시작...")
#
#     # 설정 가져오기
#     settings = get_settings()
#     if not settings:
#         print("설정을 가져올 수 없습니다. 기본값 사용.")
#         max_capacity = 100
#         image_retention_hours = 24
#     else:
#         max_capacity = settings.max_capacity
#         image_retention_hours = settings.image_retention_hours
#
#     # 카메라 캡처
#     camera = CameraCapture(camera_id=CAMERA_ID)
#     image_path = camera.capture_image()
#
#     if image_path:
#         # 프라이버시 보호 처리
#         processed_image = camera.apply_privacy_protection(image_path)
#
#         if processed_image:
#             # YOLOv7로 사람 수 카운팅
#             detector = YOLODetector(weights=YOLO_WEIGHTS)
#             people_count = detector.count_people(processed_image)
#
#             # 데이터베이스에 저장
#             save_crowd_data(people_count)
#
#             print(f"[{datetime.now()}] 처리 완료: {people_count}명 탐지됨")
#
#     # 오래된 이미지 정리
#     cleanup_old_images(hours=image_retention_hours)
#
# def start_api_server():
#     """
#     API 서버를 별도 스레드로 실행
#     """
#     from src.api.server import start_server
#     start_server(debug=False)
#
# def main():
#     """
#     메인 함수
#     """
#     print("대학교 식당 혼잡도 모니터링 시스템 시작")
#
#     # 데이터베이스 초기화
#     init_db()
#
#     # API 서버 시작 (별도 스레드)
#     server_thread = threading.Thread(target=start_api_server)
#     server_thread.daemon = True
#     server_thread.start()
#
#     # 설정 가져오기
#     settings = get_settings()
#     if not settings:
#         print("설정을 가져올 수 없습니다. 기본값 사용.")
#         capture_interval = 300  # 5분(초 단위)
#     else:
#         capture_interval = settings.capture_interval
#
#     # 캡처 및 처리 스케줄링 (초 단위로 변환)
#     capture_interval_minutes = capture_interval // 60
#     schedule.every(capture_interval_minutes).minutes.do(process_capture)
#
#     print(f"캡처 간격: {capture_interval_minutes}분")
#
#     # 시작 시 한 번 실행
#     process_capture()
#
#     # 메인 루프
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# if __name__ == "__main__":
#     main()


#사진 캡쳐 테스트용
# main.py
# import os
# import sys
# import time
# import schedule
# from datetime import datetime
# import threading
#
# # 모듈 경로 추가
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# # 모듈 임포트
# from src.capture.camera import CameraCapture
# from src.detection.yolo_detector import YOLODetector
# from src.database.operations import save_crowd_data, get_settings
# from src.utils.cleanup import cleanup_old_images
# from src.database.models import init_db
#
# # 전역 변수
# CAMERA_ID = 0  # 카메라 ID (필요시 변경)
# # main.py에서 YOLO_WEIGHTS 변수 수정
# YOLO_WEIGHTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yolov7.pt')
#
# def process_capture():
#     """
#     주기적으로 이미지를 캡처하고 처리하는 함수
#     """
#     print(f"[{datetime.now()}] 이미지 캡처 및 처리 시작...")
#
#     # 설정 가져오기
#     settings = get_settings()
#     if not settings:
#         print("설정을 가져올 수 없습니다. 기본값 사용.")
#         max_capacity = 100
#         image_retention_hours = 24
#     else:
#         max_capacity = settings.max_capacity
#         image_retention_hours = settings.image_retention_hours
#
#     # 카메라 캡처
#     camera = CameraCapture(camera_id=CAMERA_ID)
#     image_path = camera.capture_image()
#
#     if image_path:
#         # 프라이버시 보호 처리
#         processed_image = camera.apply_privacy_protection(image_path)
#
#         if processed_image:
#             # YOLOv7로 사람 수 카운팅
#             detector = YOLODetector(weights=YOLO_WEIGHTS)
#             people_count = detector.count_people(processed_image)
#
#             # 데이터베이스에 저장
#             save_crowd_data(people_count)
#
#             print(f"[{datetime.now()}] 처리 완료: {people_count}명 탐지됨")
#
#     # 오래된 이미지 정리
#     cleanup_old_images(hours=image_retention_hours)
#
# def start_api_server():
#     """
#     API 서버를 별도 스레드로 실행
#     """
#     from src.api.server import start_server
#     start_server(host='0.0.0.0', port=5001, debug=False)
#
# def main():
#     """
#     메인 함수
#     """
#     print("대학교 식당 혼잡도 모니터링 시스템 시작")
#
#     # 데이터베이스 초기화
#     init_db()
#
#     # API 서버 시작 (별도 스레드)
#     server_thread = threading.Thread(target=start_api_server)
#     server_thread.daemon = True
#     server_thread.start()
#
#     # 설정 가져오기
#     settings = get_settings()
#     if not settings:
#         print("설정을 가져올 수 없습니다. 기본값 사용.")
#         capture_interval = 300  # 5분(초 단위)
#     else:
#         capture_interval = settings.capture_interval
#
#     # 캡처 및 처리 스케줄링 (초 단위로 변환)
#     capture_interval_minutes = capture_interval // 60
#     schedule.every(capture_interval_minutes).minutes.do(process_capture)
#
#     print(f"캡처 간격: {capture_interval_minutes}분")
#
#     # 시작 시 한 번 실행
#     process_capture()
#
#     # 메인 루프
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# if __name__ == "__main__":
#     main()

# test_video.py
# 비디오 파일로 테스트하는 스크립트
import os
import sys
import time
from datetime import datetime

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 모듈 임포트
from src.capture.camera import CameraCapture, VideoProcessor
from src.detection.yolo_detector import YOLODetector
from src.database.operations import save_crowd_data
from src.database.models import init_db

# 전역 변수
YOLO_WEIGHTS = os.path.join('yolov7', 'yolov7.pt')

def test_video_capture(video_path, place_name='학생식당'):
    """
    비디오 파일로 테스트
    """
    print(f"[{datetime.now()}] 비디오 파일 테스트 시작: {video_path}")

    # 비디오 캡처 객체 생성
    camera = CameraCapture(source=video_path, is_video=True)
    detector = YOLODetector(weights=YOLO_WEIGHTS)

    # 5초 간격으로 프레임 캡처 및 처리
    frame_count = 0
    while frame_count < 10:  # 10개 프레임만 테스트
        image_path = camera.capture_image()

        if image_path:
            # 프라이버시 보호 처리
            processed_image = camera.apply_privacy_protection(image_path)

            if processed_image:
                # YOLOv7로 사람 수 카운팅
                people_count = detector.count_people(processed_image)

                # 데이터베이스에 저장
                save_crowd_data(people_count, place_name=place_name)

                print(f"[{datetime.now()}] 프레임 {frame_count}: {people_count}명 탐지됨")

        frame_count += 1
        time.sleep(5)  # 5초 대기

def test_live_camera(camera_id=0, place_name='학생식당'):
    """
    실시간 웹캠으로 테스트
    """
    print(f"[{datetime.now()}] 실시간 카메라 테스트 시작")

    # 카메라 캡처 객체 생성
    camera = CameraCapture(source=camera_id)
    detector = YOLODetector(weights=YOLO_WEIGHTS)

    # 지속적으로 캡처
    while True:
        image_path = camera.capture_image()

        if image_path:
            # 프라이버시 보호 처리
            processed_image = camera.apply_privacy_protection(image_path)

            if processed_image:
                # YOLOv7로 사람 수 카운팅
                people_count = detector.count_people(processed_image)

                # 데이터베이스에 저장
                save_crowd_data(people_count, place_name=place_name)

                print(f"[{datetime.now()}] {people_count}명 탐지됨")

        time.sleep(10)  # 10초 간격

def main():
    """
    메인 함수
    """
    # 데이터베이스 초기화
    init_db()

    # 테스트 모드 선택
    mode = input("테스트 모드 선택 (1: 비디오 파일, 2: 실시간 카메라): ")

    if mode == '1':
        video_path = input("비디오 파일 경로 입력: ")
        place_name = input("장소 이름 입력 (기본값: 학생식당): ") or '학생식당'
        test_video_capture(video_path, place_name)
    elif mode == '2':
        camera_id = int(input("카메라 ID 입력 (기본값: 0): ") or '0')
        place_name = input("장소 이름 입력 (기본값: 학생식당): ") or '학생식당'
        test_live_camera(camera_id, place_name)
    else:
        print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()