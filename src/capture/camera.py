# # src/capture/camera.py
# #이미지 캡처 모듈
# import cv2
# import os
# import datetime
# from pathlib import Path
#
# class CameraCapture:
#     def __init__(self, camera_id=0, save_dir='temp_images'):
#         """
#         카메라 캡처 초기화
#         """
#         self.camera_id = camera_id
#         self.save_dir = save_dir
#
#         # 저장 디렉토리 생성
#         os.makedirs(save_dir, exist_ok=True)
#
#     def capture_image(self):
#         """
#         카메라에서 이미지 캡처
#         """
#         # 카메라 열기
#         cap = cv2.VideoCapture(self.camera_id)
#
#         if not cap.isOpened():
#             print(f"카메라 {self.camera_id}를 열 수 없습니다.")
#             return None
#
#         # 이미지 캡처
#         ret, frame = cap.read()
#         cap.release()
#
#         if not ret:
#             print("이미지 캡처 실패")
#             return None
#
#         # 현재 시간으로 파일명 생성
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"cafeteria_{timestamp}.jpg"
#         filepath = os.path.join(self.save_dir, filename)
#
#         # 이미지 저장
#         cv2.imwrite(filepath, frame)
#         print(f"이미지 캡처 및 저장 완료: {filepath}")
#
#         return filepath
#
#     def apply_privacy_protection(self, image_path):
#         """
#         이미지에 프라이버시 보호 처리 적용
#         """
#         # 이미지 로드
#         image = cv2.imread(image_path)
#         if image is None:
#             print(f"이미지를 불러올 수 없습니다: {image_path}")
#             return None
#
#         # 이미지 해상도 낮추기 (50%)
#         width = int(image.shape[1] * 0.5)
#         height = int(image.shape[0] * 0.5)
#         resized_image = cv2.resize(image, (width, height))
#
#         # 이미지 저장
#         processed_path = image_path.replace(".jpg", "_processed.jpg")
#         cv2.imwrite(processed_path, resized_image)
#         print(f"프라이버시 보호 처리 완료: {processed_path}")
#
#         return processed_path

#이미지 캡쳐 테스트1
# src/capture/camera.py
# import cv2
# import os
# import datetime
# from pathlib import Path
#
# class CameraCapture:
#     def __init__(self, camera_id=0, save_dir='temp_images'):
#         """
#         카메라 캡처 초기화
#         """
#         self.camera_id = camera_id
#         self.save_dir = save_dir
#
#         # 저장 디렉토리 생성
#         os.makedirs(save_dir, exist_ok=True)
#
#     def capture_image(self):
#         """
#         테스트용: 카메라 대신 샘플 이미지 반환
#         """
#         # 테스트 이미지 경로
#         test_image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'test_images', 'sample_cafeteria.jpg')
#
#         # 저장 디렉토리 확인
#         os.makedirs(self.save_dir, exist_ok=True)
#
#         # 현재 시간으로 파일명 생성
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"cafeteria_{timestamp}.jpg"
#         filepath = os.path.join(self.save_dir, filename)
#
#         # 테스트 이미지 복사
#         import shutil
#         try:
#             shutil.copy(test_image_path, filepath)
#             print(f"테스트 이미지 사용: {filepath}")
#             return filepath
#         except Exception as e:
#             print(f"테스트 이미지 복사 오류: {e}")
#             print(f"테스트 이미지 경로: {test_image_path}")
#             return None
#
#     def apply_privacy_protection(self, image_path):
#         """
#         이미지에 프라이버시 보호 처리 적용
#         """
#         if image_path is None or not os.path.exists(image_path):
#             print(f"이미지를 찾을 수 없습니다: {image_path}")
#             return None
#
#         # 이미지 로드
#         image = cv2.imread(image_path)
#         if image is None:
#             print(f"이미지를 불러올 수 없습니다: {image_path}")
#             return None
#
#         # 이미지 해상도 낮추기 (50%)
#         width = int(image.shape[1] * 0.5)
#         height = int(image.shape[0] * 0.5)
#         resized_image = cv2.resize(image, (width, height))
#
#         # 이미지 저장
#         processed_path = image_path.replace(".jpg", "_processed.jpg")
#         cv2.imwrite(processed_path, resized_image)
#         print(f"프라이버시 보호 처리 완료: {processed_path}")
#
#         return processed_path

# src/capture/camera.py
#이미지/비디오 캡처 모듈
# import cv2
# import os
# import datetime
# from pathlib import Path

# class CameraCapture:
#     def __init__(self, source=0, save_dir='temp_images', is_video=False):
#         """
#         카메라/비디오 캡처 초기화
#
#         Args:
#             source: 카메라 ID (int) 또는 비디오 파일 경로 (str)
#             save_dir: 이미지 저장 디렉토리
#             is_video: 비디오 파일인지 여부
#         """
#         self.source = source
#         self.save_dir = save_dir
#         self.is_video = is_video
#         self.cap = None
#         self.frame_count = 0
#
#         # 저장 디렉토리 생성
#         os.makedirs(save_dir, exist_ok=True)
#
#     def capture_image(self):
#         """
#         카메라/비디오에서 이미지 캡처
#         """
#         # 카메라/비디오 열기
#         if self.cap is None:
#             self.cap = cv2.VideoCapture(self.source)
#
#         if not self.cap.isOpened():
#             print(f"소스 {self.source}를 열 수 없습니다.")
#             return None
#
#         # 프레임 캡처
#         ret, frame = self.cap.read()
#
#         # 비디오 파일의 경우 끝에 도달하면 처음부터 다시
#         if self.is_video and not ret:
#             self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             ret, frame = self.cap.read()
#
#         if not ret:
#             print("프레임 캡처 실패")
#             return None
#
#         # 현재 시간으로 파일명 생성
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"capture_{self.frame_count}_{timestamp}.jpg"
#         filepath = os.path.join(self.save_dir, filename)
#
#         # 이미지 저장
#         cv2.imwrite(filepath, frame)
#         print(f"이미지 캡처 및 저장 완료: {filepath}")
#
#         self.frame_count += 1
#         return filepath
#
#     def apply_privacy_protection(self, image_path):
#         """
#         이미지에 프라이버시 보호 처리 적용
#         """
#         # 이미지 로드
#         image = cv2.imread(image_path)
#         if image is None:
#             print(f"이미지를 불러올 수 없습니다: {image_path}")
#             return None
#
#         # 이미지 해상도 낮추기 (50%)
#         width = int(image.shape[1] * 0.5)
#         height = int(image.shape[0] * 0.5)
#         resized_image = cv2.resize(image, (width, height))
#
#         # 이미지 저장
#         processed_path = image_path.replace(".jpg", "_processed.jpg")
#         cv2.imwrite(processed_path, resized_image)
#         print(f"프라이버시 보호 처리 완료: {processed_path}")
#
#         return processed_path
#
#     def __del__(self):
#         """
#         리소스 정리
#         """
#         if self.cap is not None:
#             self.cap.release()
#
# # 비디오 처리를 위한 추가 클래스
# class VideoProcessor:
#     def __init__(self, video_path):
#         """
#         비디오 처리기 초기화
#         """
#         self.video_path = video_path
#         self.cap = cv2.VideoCapture(video_path)
#
#         # 비디오 정보 가져오기
#         self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
#         self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
#
#     def process_video_frames(self, interval_seconds=5, output_dir='temp_images'):
#         """
#         비디오에서 일정 간격으로 프레임 추출
#
#         Args:
#             interval_seconds: 프레임 추출 간격 (초)
#             output_dir: 출력 디렉토리
#         """
#         os.makedirs(output_dir, exist_ok=True)
#
#         frame_interval = self.fps * interval_seconds
#         frame_count = 0
#         extracted_count = 0
#
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
#
#             if frame_count % frame_interval == 0:
#                 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#                 filename = f"video_frame_{extracted_count}_{timestamp}.jpg"
#                 filepath = os.path.join(output_dir, filename)
#
#                 cv2.imwrite(filepath, frame)
#                 print(f"프레임 추출: {filepath}")
#
#                 extracted_count += 1
#
#             frame_count += 1
#
#         self.cap.release()
#         print(f"총 {extracted_count}개의 프레임 추출 완료")
#
#         return extracted_count

# src/capture/camera.py
#이미지/비디오 캡처 모듈
import cv2
import os
import datetime
from pathlib import Path

class CameraCapture:
    def __init__(self, source=0, save_dir='temp_images', is_video=False):
        """
        카메라/비디오 캡처 초기화

        Args:
            source: 카메라 ID (int) 또는 비디오 파일 경로 (str)
            save_dir: 이미지 저장 디렉토리
            is_video: 비디오 파일인지 여부
        """
        self.source = source
        self.save_dir = save_dir
        self.is_video = is_video
        self.cap = None
        self.frame_count = 0
        self.video_frame_count = 0  # 비디오 프레임 카운터

        # 저장 디렉토리 생성
        os.makedirs(save_dir, exist_ok=True)

    def capture_image(self):
        """
        카메라/비디오에서 이미지 캡처 (연속 재생)
        """
        # 처음 실행시에만 카메라/비디오 열기
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.source)
            if self.is_video:
                self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
                print(f"비디오 열기: {self.source}")
                print(f"비디오 정보: 총 {self.total_frames}프레임, {self.fps}fps")

        if not self.cap.isOpened():
            print(f"소스 {self.source}를 열 수 없습니다.")
            return None

        # 현재 프레임 위치 확인
        if self.is_video:
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            print(f"읽기 전 프레임 위치: {current_frame}/{self.total_frames}")

        # 다음 프레임 읽기
        ret, frame = self.cap.read()

        if self.is_video:
            after_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            print(f"읽기 후 프레임 위치: {after_frame}/{self.total_frames}")

        # 비디오 끝에 도달하면 처음부터 다시
        if not ret:
            if self.is_video:
                print("비디오 끝에 도달, 처음부터 다시 시작")
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            else:
                print("프레임 캡처 실패")
                return None

        if not ret:
            print("프레임 캡처 실패")
            return None

        # 현재 시간으로 파일명 생성
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{self.frame_count}_{timestamp}_frame{self.video_frame_count}.jpg"
        filepath = os.path.join(self.save_dir, filename)

        # 이미지 저장
        cv2.imwrite(filepath, frame)
        print(f"이미지 캡처 및 저장 완료: {filepath}")

        self.frame_count += 1
        self.video_frame_count += 1

        # 프레임 건너뛰기 (30프레임 = 1초)
        if self.is_video:
            skip_frames = self.fps * 5  # 5초마다
            for _ in range(skip_frames - 1):
                self.cap.read()
                self.video_frame_count += 1

            new_pos = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            print(f"프레임 건너뛰기 후 위치: {new_pos}")

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

    def __del__(self):
        """
        리소스 정리
        """
        if self.cap is not None:
            self.cap.release()

# 비디오 처리를 위한 추가 클래스
class VideoProcessor:
    def __init__(self, video_path):
        """
        비디오 처리기 초기화
        """
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        # 비디오 정보 가져오기
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def process_video_frames(self, interval_seconds=5, output_dir='temp_images'):
        """
        비디오에서 일정 간격으로 프레임 추출

        Args:
            interval_seconds: 프레임 추출 간격 (초)
            output_dir: 출력 디렉토리
        """
        os.makedirs(output_dir, exist_ok=True)

        frame_interval = self.fps * interval_seconds
        frame_count = 0
        extracted_count = 0

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"video_frame_{extracted_count}_{timestamp}.jpg"
                filepath = os.path.join(output_dir, filename)

                cv2.imwrite(filepath, frame)
                print(f"프레임 추출: {filepath}")

                extracted_count += 1

            frame_count += 1

        self.cap.release()
        print(f"총 {extracted_count}개의 프레임 추출 완료")

        return extracted_count