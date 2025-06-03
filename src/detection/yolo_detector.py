# # src/detection/yolo_detector.py
# #YOLOv7 검출 모듈
# import sys
# import os
# from pathlib import Path
# import torch
# import cv2
# import numpy as np
#
# # YOLOv7 디렉토리 경로 (clone 위치에 따라 조정)
# YOLO_PATH = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'yolov7'))
# sys.path.append(str(YOLO_PATH))
#
# # YOLOv7 모듈 임포트
# from models.experimental import attempt_load
# from utils.general import check_img_size, non_max_suppression, scale_coords
# from utils.datasets import letterbox
# from utils.torch_utils import select_device
#
# class YOLODetector:
#     def __init__(self, weights='yolov7.pt', device='cpu', img_size=640, conf_thres=0.25, iou_thres=0.45):
#         """
#         YOLOv7 모델 초기화
#         """
#         self.device = select_device(device)
#         self.model = attempt_load(weights, map_location=self.device)
#         self.img_size = check_img_size(img_size, s=self.model.stride.max())
#         self.conf_thres = conf_thres
#         self.iou_thres = iou_thres
#
#         # 클래스 이름 가져오기
#         self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
#         print(f"모델 로드 완료. 사용 가능한 클래스: {self.names}")
#
#     def detect(self, image_path):
#         """
#         이미지에서 객체 탐지 수행
#         """
#         # 이미지 로드
#         img0 = cv2.imread(image_path)
#         if img0 is None:
#             print(f"이미지를 불러올 수 없습니다: {image_path}")
#             return []
#
#         # 이미지 전처리
#         img = letterbox(img0, new_shape=self.img_size)[0]
#         img = img.transpose(2, 0, 1)  # HWC -> CHW
#         img = np.ascontiguousarray(img)
#         img = torch.from_numpy(img).to(self.device)
#         img = img.float() / 255.0
#         if img.ndimension() == 3:
#             img = img.unsqueeze(0)
#
#         # 추론
#         with torch.no_grad():
#             pred = self.model(img)[0]
#
#         # NMS 적용
#         pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)
#
#         results = []
#         for i, det in enumerate(pred):
#             if len(det):
#                 # 좌표 변환
#                 det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
#
#                 # 결과 수집
#                 for *xyxy, conf, cls in det:
#                     x1, y1, x2, y2 = [int(x) for x in xyxy]
#                     class_id = int(cls)
#                     class_name = self.names[class_id]
#                     confidence = float(conf)
#
#                     results.append({
#                         'class_id': class_id,
#                         'class_name': class_name,
#                         'confidence': confidence,
#                         'bbox': [x1, y1, x2, y2]
#                     })
#
#         return results
#
#     def count_people(self, image_path):
#         """
#         이미지에서 사람 수 카운팅
#         """
#         results = self.detect(image_path)
#         people_count = sum(1 for obj in results if obj['class_name'] == 'person')
#         print(f"사람 수 카운팅 결과: {people_count}명")
#         return people_count

# src/detection/yolo_detector.py
import sys
import os
import cv2
import numpy as np
import torch
import torch.nn as nn
from pathlib import Path

# YOLOv7 디렉토리 경로
YOLO_PATH = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'yolov7'))
sys.path.append(str(YOLO_PATH))

# PyTorch 버전 확인
TORCH_VERSION = torch.__version__
print(f"PyTorch 버전: {TORCH_VERSION}")

# YOLOv7 모듈 임포트
try:
    # YOLOv7 모듈을 명시적으로 임포트
    from models.yolo import Model  # 모델 클래스를 안전한 글로벌로 등록하기 위해 필요
    from models.experimental import attempt_load
    from utils.general import check_img_size, non_max_suppression, scale_coords
    from utils.datasets import letterbox
    from utils.torch_utils import select_device

    # PyTorch 2.6+ 호환성: 필요한 클래스를 안전한 글로벌로 등록
    if hasattr(torch.serialization, 'add_safe_globals'):
        safe_classes = [
            Model,
            nn.modules.container.Sequential,
            torch.nn.modules.container.Sequential,
            nn.ModuleList,
            nn.modules.conv.Conv2d,
            torch.nn.modules.conv.Conv2d
        ]
        torch.serialization.add_safe_globals(safe_classes)
        print(f"PyTorch 2.6+ 호환성: 다음 클래스를 안전한 글로벌로 등록했습니다: {safe_classes}")

    print("YOLOv7 모듈 임포트 성공")
except ImportError as e:
    print(f"YOLOv7 모듈 임포트 실패: {e}")
    raise ImportError("YOLOv7 모듈을 임포트할 수 없습니다. YOLOv7 설치를 확인하세요.")

class YOLODetector:
    def __init__(self, weights='yolov7.pt', device='cpu', img_size=640, conf_thres=0.25, iou_thres=0.45):
        """
        YOLOv7 모델 초기화
        """
        self.weights = weights
        self.device = select_device(device)
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres

        print(f"모델 파일 경로: {self.weights}")
        print(f"사용 디바이스: {self.device}")

        # 모델 파일 존재 확인
        if not os.path.exists(self.weights):
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {self.weights}")

        # PyTorch 버전에 따른 모델 로드 방법 결정
        try:
            major, minor = map(int, TORCH_VERSION.split('.')[:2])

            if major >= 2 and minor >= 6:
                print("PyTorch 2.6+ 감지: weights_only=False 옵션으로 모델 로드")

                # 필요한 클래스를 모두 안전한 글로벌로 등록
                all_classes = []
                for module in [torch.nn.modules.container, torch.nn.modules.conv, torch.nn.modules.activation]:
                    for name in dir(module):
                        if not name.startswith('_'):
                            cls = getattr(module, name)
                            if isinstance(cls, type):
                                all_classes.append(cls)

                torch.serialization.add_safe_globals(all_classes)

                # weights_only=False로 모델 직접 로드
                ckpt = torch.load(self.weights, map_location=self.device, weights_only=False)
                print("모델 체크포인트 로드 성공")

                # 체크포인트에서 모델 구성
                if 'model' in ckpt:
                    self.model = ckpt['model'].float()  # 명시적으로 float32로 변환
                else:
                    self.model = ckpt.float()  # 명시적으로 float32로 변환

                print("모델 초기화 완료")
            else:
                # PyTorch 2.6 미만 버전에서는 기존 방식 사용
                print("PyTorch 2.6 미만 버전 감지: 기본 로드 방식 사용")
                self.model = attempt_load(self.weights, map_location=self.device).float()  # float32로 변환

            # 모델을 평가 모드로 설정
            self.model.eval()

            # float32로 명시적 변환
            self.model = self.model.float()

            # 모델 설정
            self.stride = int(self.model.stride.max())
            self.img_size = check_img_size(img_size, s=self.stride)

            # 클래스 이름 가져오기
            self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
            print(f"모델 로드 성공. 사용 가능한 클래스: {self.names}")

        except Exception as e:
            print(f"모델 로드 중 오류 발생: {e}")
            print(f"오류 유형: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"YOLOv7 모델 로드 실패: {e}")

    def detect(self, image_path):
        """
        이미지에서 객체 탐지 수행
        """
        # 이미지 로드
        img0 = cv2.imread(image_path)
        if img0 is None:
            print(f"이미지를 불러올 수 없습니다: {image_path}")
            return []

        # 이미지 전처리
        img = letterbox(img0, new_shape=self.img_size, stride=self.stride)[0]
        img = img.transpose(2, 0, 1)  # HWC -> CHW
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float() / 255.0  # 명시적으로 float32로 변환
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 추론 전 모델이 float32인지 확인
        for param in self.model.parameters():
            if param.dtype != torch.float32:
                print(f"모델 파라미터가 float32가 아님: {param.dtype}")
                param.data = param.data.float()

        # 추론
        with torch.no_grad():
            try:
                pred = self.model(img)[0]

                # NMS 적용
                pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)

                results = []
                for i, det in enumerate(pred):
                    if len(det):
                        # 좌표 변환
                        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

                        # 결과 수집
                        for *xyxy, conf, cls in det:
                            x1, y1, x2, y2 = [int(x) for x in xyxy]
                            class_id = int(cls)
                            class_name = self.names[class_id]
                            confidence = float(conf)

                            # 사람 클래스만 필터링 (클래스 ID 0)
                            if class_id == 0:  # 'person' 클래스
                                results.append({
                                    'class_id': class_id,
                                    'class_name': class_name,
                                    'confidence': confidence,
                                    'bbox': [x1, y1, x2, y2]
                                })
            except Exception as e:
                print(f"추론 중 오류 발생: {e}")
                import traceback
                traceback.print_exc()
                # 오류 발생 시 빈 결과 반환
                return []

        # 탐지 결과 시각화 (디버깅용)
        debug_img = img0.copy()
        for result in results:
            x1, y1, x2, y2 = result['bbox']
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{result['class_name']}: {result['confidence']:.2f}"
            cv2.putText(debug_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 디버그 이미지 저장
        debug_path = image_path.replace('.jpg', '_debug.jpg')
        cv2.imwrite(debug_path, debug_img)
        print(f"디버그 이미지 저장됨: {debug_path}")

        return results

    def count_people(self, image_path):
        """
        이미지에서 사람 수 카운팅
        """
        results = self.detect(image_path)
        people_count = len(results)
        print(f"사람 수 카운팅 결과: {people_count}명")
        return people_count