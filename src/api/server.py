# src/api/server.py
#API 서버 모듈
from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime, timedelta

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.database.operations import get_latest_crowd_data, get_crowd_history

app = Flask(__name__)

@app.route('/api/current', methods=['GET'])
def get_current_crowd():
    """
    현재 혼잡도 정보 API
    """
    data = get_latest_crowd_data()
    if data:
        return jsonify({
            'timestamp': data.timestamp.isoformat(),
            'people_count': data.people_count,
            'occupancy_rate': data.occupancy_rate,
            'crowd_level': data.crowd_level
        })
    else:
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

def start_server(host='0.0.0.0', port=5000, debug=True):
    """
    API 서버 시작
    """
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    start_server()