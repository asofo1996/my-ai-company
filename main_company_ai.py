import time
import sqlite3
import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- DB 경로 ---
DB_PATH = os.path.join(os.path.dirname(__file__), "db", "company_data.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# --- 데이터베이스 설정 ---
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            file_path TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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

# --- CrewAI Task 수행 로직 ---
def run_crewai_task(project_id, feedback_text):
    print("CrewAI 실행 시작...")

    agent = Agent(
        role="AI 전략가",
        goal="고객의 피드백을 기반으로 전략적 개선 제안서를 작성",
        backstory="전 세계 유수의 전략 컨설팅 회사에서 경험을 쌓은 GPT 기반 AI 전략가입니다.",
        verbose=True,
        allow_delegation=False
    )

    task = Task(
        description=f"다음 피드백을 분석하고 요약 및 개선안을 작성해주세요:\n\n{feedback_text}",
        expected_output="전략 제안서 텍스트",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    return result

# --- 작업 처리 루프 ---
def process_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, project_id, feedback_text FROM feedback WHERE is_processed = 0")
    tasks = cursor.fetchall()

    for task in tasks:
        task_id, project_id, feedback_text = task
        print(f"[피드백 수신] ID: {task_id}, 프로젝트: {project_id}, 내용: {feedback_text[:20]}...")

        try:
            result = run_crewai_task(project_id, feedback_text)

            # 결과 저장
            cursor.execute("INSERT INTO reports (project_id, report_text) VALUES (?, ?)", (project_id, result))

            # 승인 요청 예시
            if "서버" in feedback_text or "비용" in feedback_text:
                cursor.execute(
                    "INSERT INTO approval_requests (project_id, request_text) VALUES (?, ?)",
                    (project_id, f"프로젝트 {project_id} 관련 결제/승인 요청: {feedback_text[:50]}...")
                )

            # 상태 로그 기록
            cursor.execute("INSERT INTO status_logs (project_id, log_text) VALUES (?, ?)", (project_id, "작업 완료됨"))

            # 처리 완료 표시
            cursor.execute("UPDATE feedback SET is_processed = 1 WHERE id = ?", (task_id,))
            conn.commit()
            print(f"[완료] 작업 ID {task_id}에 대한 결과 저장 및 승인 요청 완료.")

        except Exception as e:
            print(f"[오류] 작업 ID {task_id} 처리 중 오류 발생: {e}")
            cursor.execute("INSERT INTO status_logs (project_id, log_text) VALUES (?, ?)", (project_id, f"오류 발생: {str(e)}"))
            conn.commit()

    conn.close()

# --- 메인 루프 ---
if __name__ == "__main__":
    print("🧠 AI 백엔드 엔진을 시작합니다...")
    setup_database()
    print("✅ 데이터베이스 초기화 완료. 10초마다 새 피드백을 확인합니다.\n")

    while True:
        process_tasks()
        time.sleep(10)
