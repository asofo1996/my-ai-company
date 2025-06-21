import os
import traceback
from dotenv import load_dotenv
from supabase import create_client
from utils.auto_instruction import generate_auto_instruction
from utils.router import process_instruction

# ✅ 1. 환경 변수 불러오기
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("❌ Supabase 환경변수가 누락되었습니다.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ 2. 기본 관리자 이메일 설정
ADMIN_EMAIL = "tjryv1996@gmail.com"

def run_auto_job():
    print("\n🚀 [START] Crew 자동 작업을 시작합니다...")

    try:
        # ✅ [1] 지시문 자동 생성
        auto_instruction = generate_auto_instruction()
        print(f"\n📝 [지시 생성 완료]\n{auto_instruction}")

        # ✅ [2] 지시 실행 → 결과 수신
        result = process_instruction(auto_instruction)
        print(f"\n✅ [작업 결과 수신 완료]\n{result}")

        # ✅ [3] 결과 Supabase 기록
        data = {
            "user_id": "system_auto",
            "project_id": 999,
            "feedback_text": auto_instruction,
            "category": "자동지시(Crew SaaS 구축)",
            "result": result,
            "creator_email": ADMIN_EMAIL,
            "is_auto": True
        }

        response = supabase.table("feedbacks").insert(data).execute()
        print(f"\n📦 [Supabase 기록 완료] 응답: {response}")

    except Exception as e:
        print(f"\n❌ [오류 발생] 자동 실행 중 문제가 발생했습니다:\n{e}")
        traceback.print_exc()

    print("\n🎉 [완료] Crew SaaS 자동 지시 실행 종료\n")

if __name__ == "__main__":
    run_auto_job()
