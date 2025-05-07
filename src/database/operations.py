# src/database/operations.py
#데이터베이스 작업 함수 구현
from .models import Session, CrowdData, Settings
from datetime import datetime, timedelta

def save_crowd_data(people_count):
    """
    인원수 데이터를 DB에 저장
    """
    # 세션 생성
    session = Session()

    try:
        # 설정 가져오기
        settings = session.query(Settings).first()
        if not settings:
            settings = Settings()
            session.add(settings)
            session.commit()

        max_capacity = settings.max_capacity

        # 혼잡도 계산
        occupancy_rate = (people_count / max_capacity) * 100

        # 혼잡도 레벨 결정
        if occupancy_rate <= 30:
            crowd_level = "여유"
        elif occupancy_rate <= 70:
            crowd_level = "보통"
        else:
            crowd_level = "혼잡"

        # 데이터 생성
        new_data = CrowdData(
            people_count=people_count,
            occupancy_rate=occupancy_rate,
            crowd_level=crowd_level
        )

        # DB에 저장
        session.add(new_data)
        session.commit()
        print(f"[{datetime.now()}] 데이터 저장 완료: {people_count}명, 혼잡도 {crowd_level}")
        return True
    except Exception as e:
        session.rollback()
        print(f"데이터 저장 오류: {e}")
        return False
    finally:
        session.close()

def get_latest_crowd_data():
    """
    최신 혼잡도 데이터 조회
    """
    session = Session()
    try:
        latest = session.query(CrowdData).order_by(CrowdData.timestamp.desc()).first()
        return latest
    except Exception as e:
        print(f"데이터 조회 오류: {e}")
        return None
    finally:
        session.close()

def get_crowd_history(hours=24):
    """
    지정된 시간 동안의 혼잡도 데이터 조회
    """
    session = Session()
    try:
        start_time = datetime.now() - timedelta(hours=hours)
        history = session.query(CrowdData).filter(
            CrowdData.timestamp >= start_time
        ).order_by(CrowdData.timestamp).all()
        return history
    except Exception as e:
        print(f"데이터 조회 오류: {e}")
        return []
    finally:
        session.close()

def get_settings():
    """
    설정 데이터 조회
    """
    session = Session()
    try:
        settings = session.query(Settings).first()
        if not settings:
            settings = Settings()
            session.add(settings)
            session.commit()
        return settings
    except Exception as e:
        print(f"설정 조회 오류: {e}")
        return None
    finally:
        session.close()