import sqlite3
import os

# 데이터베이스 경로 설정
db_path = os.path.join("app", "db", "company_data.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# 데이터베이스 연결
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ✅ reports 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        report_text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

# ✅ status_logs 테이블도 함께 생성 (추가 오류 방지)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS status_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        log_text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

# ✅ approval_requests 테이블도 함께 생성 (결제 승인 탭용)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS approval_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        request_text TEXT,
        status TEXT DEFAULT '대기 중',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

conn.commit()
conn.close()

print("✅ 모든 테이블 생성이 완료되었습니다.")
