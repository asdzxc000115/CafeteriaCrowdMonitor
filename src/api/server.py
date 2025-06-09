
from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime, timedelta

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.database.operations import get_latest_crowd_data, get_crowd_history

app = Flask(__name__)

# CORS 설정 추가 (Flutter 웹에서 필요)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/api/current', methods=['GET'])
def get_current_crowd():
    """
    현재 혼잡도 정보 API
    """
    place_name = request.args.get('place', '학생식당')
    print(f"\n===== API 요청 =====")
    print(f"요청 시간: {datetime.now()}")
    print(f"요청 장소: '{place_name}'")
    print("===================")

    data = get_latest_crowd_data(place_name)
    if data:
        print(f"응답 데이터: {place_name} - {data.people_count}명")
        return jsonify({
            'timestamp': data.timestamp.isoformat(),
            'people_count': data.people_count,
            'occupancy_rate': data.occupancy_rate,
            'crowd_level': data.crowd_level,
            'place_name': data.place_name
        })
    else:
        print(f"응답: {place_name} - 데이터 없음")
        return jsonify({'error': '데이터가 없습니다'}), 404

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    혼잡도 이력 조회 API
    """
    # URL 파라미터에서 시간 범위 가져오기 (기본 24시간)
    hours = request.args.get('hours', default=24, type=int)

    data = get_crowd_history(hours)
    result = []

    for item in data:
        result.append({
            'timestamp': item.timestamp.isoformat(),
            'people_count': item.people_count,
            'occupancy_rate': item.occupancy_rate,
            'crowd_level': item.crowd_level
        })

    return jsonify(result)

def start_server(host='0.0.0.0', port=5001, debug=True):  # 5001로 변경
    """
    API 서버 시작
    """
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    start_server(port=5001)  # 5001로 변경