import subprocess
import threading
import os
import time
import sys
import webbrowser
import shutil
import sqlite3
from dotenv import load_dotenv

load_dotenv()

def get_base_path():
    """PyInstaller 실행 환경 대응"""
    return os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

def setup_database():
    """DB 생성 및 테이블 구조 자동 생성"""
    db_path = os.path.join(get_base_path(), "app", "db", "company_data.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # ✅ DB 경로 환경변수로 등록하여 Streamlit에서 사용 가능하게 함
    os.environ["AI_DB_PATH"] = db_path

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 모든 테이블 생성 보장
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            feedback_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_processed BOOLEAN DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            log_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            report_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS approval_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            request_text TEXT,
            status TEXT DEFAULT '승인 대기',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ DB 및 테이블 자동 생성 완료")

def run_ai_engine():
    """AI 백엔드 엔진 실행"""
    script_path = os.path.join(get_base_path(), "main_company_ai.py")
    try:
        subprocess.Popen(["python", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🧠 AI 백엔드 엔진 실행 중...")
    except Exception as e:
        print(f"❌ AI 엔진 실행 실패: {e}")

def run_dashboard():
    """Streamlit 대시보드 실행"""
    try:
        base_path = get_base_path()
        original_path = os.path.join(base_path, "ceo_dashboard.py")
        temp_path = os.path.join(base_path, "ceo_dashboard_temp.py")

        if not os.path.exists(original_path):
            raise FileNotFoundError(f"❌ Streamlit 원본 없음: {original_path}")

        shutil.copyfile(original_path, temp_path)

        streamlit_path = shutil.which("streamlit")
        if not streamlit_path:
            raise FileNotFoundError("❌ streamlit 명령어를 찾을 수 없습니다 (PATH 문제)")

        # Streamlit 실행 시 환경변수 함께 전달
        env = os.environ.copy()
        cmd = f'"{streamlit_path}" run "{temp_path}" --server.headless true --server.port 8501'
        subprocess.Popen(cmd, shell=True, env=env)

        time.sleep(3)
        webbrowser.open("http://localhost:8501")
        print("📊 Streamlit 대시보드 실행됨")

    except Exception as e:
        print(f"❌ Streamlit 실행 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 AI Command Center를 시작합니다...\n")

    # 1. DB 및 테이블 생성 (+ 경로 환경변수 등록)
    setup_database()

    # 2. AI 백엔드 실행
    threading.Thread(target=run_ai_engine, daemon=True).start()

    # 3. 대시보드 실행
    time.sleep(2)
    run_dashboard()
