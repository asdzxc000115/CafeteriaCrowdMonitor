# src/database/models.py
#데이터베이스 모델 작성하기
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os

# 상위 디렉토리 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.db_config import DB_CONFIG

# 데이터베이스 연결 문자열
connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# 엔진 생성
engine = create_engine(connection_string)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 크라우드 데이터 모델
class CrowdData(Base):
    __tablename__ = 'crowd_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    people_count = Column(Integer, nullable=False)
    occupancy_rate = Column(Float, nullable=False)
    crowd_level = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<CrowdData(id={self.id}, timestamp={self.timestamp}, people_count={self.people_count}, crowd_level={self.crowd_level})>"

# 설정 모델
class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, default=1)
    max_capacity = Column(Integer, nullable=False, default=100)
    capture_interval = Column(Integer, nullable=False, default=300)
    image_retention_hours = Column(Integer, nullable=False, default=24)

    def __repr__(self):
        return f"<Settings(max_capacity={self.max_capacity}, capture_interval={self.capture_interval}, image_retention_hours={self.image_retention_hours})>"

# 데이터베이스 초기화 함수
def init_db():
    Base.metadata.create_all(engine)
    print("데이터베이스 테이블이 생성되었습니다.")

if __name__ == "__main__":
    init_db()