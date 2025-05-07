# src/detection/yolo_detector.py
#YOLOv7 검출 모듈
import sys
import os
from pathlib import Path
import torch
import cv2
import numpy as np

# YOLOv7 디렉토리 경로 (clone 위치에 따라 조정)
YOLO_PATH = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'yolov7'))
sys.path.append(str(YOLO_PATH))

# YOLOv7 모듈 임포트
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.torch_utils import select_device

class YOLODetector:
    def __init__(self, weights='yolov7.pt', device='cpu', img_size=640, conf_thres=0.25, iou_thres=0.45):
        """
        YOLOv7 모델 초기화
        """
        self.device = select_device(device)
        self.model = attempt_load(weights, map_location=self.device)
        self.img_size = check_img_size(img_size, s=self.model.stride.max())
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres

        # 클래스 이름 가져오기
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        print(f"모델 로드 완료. 사용 가능한 클래스: {self.names}")

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
        img = letterbox(img0, new_shape=self.img_size)[0]
        img = img.transpose(2, 0, 1)  # HWC -> CHW
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float() / 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 추론
        with torch.no_grad():
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

                    results.append({
                        'class_id': class_id,
                        'class_name': class_name,
                        'confidence': confidence,
                        'bbox': [x1, y1, x2, y2]
                    })

        return results

    def count_people(self, image_path):
        """
        이미지에서 사람 수 카운팅
        """
        results = self.detect(image_path)
        people_count = sum(1 for obj in results if obj['class_name'] == 'person')
        print(f"사람 수 카운팅 결과: {people_count}명")
        return people_count