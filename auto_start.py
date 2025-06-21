
import time
from auto_runner import run_instruction

def auto_loop():
    print("🚀 Crew AI 자동 실행 시작...")
    while True:
        try:
            run_instruction()  # 사용자가 입력한 지시를 기반으로 작업 시작
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        time.sleep(5)  # 5초 간격으로 작업 반복 확인

if __name__ == "__main__":
    auto_loop()
