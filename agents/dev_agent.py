# ✅ dev_agent.py (GPT 기반 개발자 역할 수행)

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def execute(task_plan: dict) -> str:
    """
    PM이 전달한 개발 관련 작업 지시를 받아 GPT를 통해 코드 생성 요청
    """
    code_task = task_plan.get("dev_task", "")
    print(f"\n💻 [Dev Agent] 작업 지시 수신: {code_task}")

    if not code_task:
        return "❌ 개발 작업 내용이 비어 있습니다."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 매우 숙련된 시니어 개발자입니다."},
                {"role": "user", "content": f"{code_task}에 필요한 코드를 생성해줘. 주석과 함께 설명해줘."}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        code_result = response.choices[0].message.content
        print("✅ [Dev Agent] GPT 코드 생성 완료")
        return code_result

    except Exception as e:
        print("❌ [Dev Agent 오류] GPT 요청 실패:", e)
        return f"[Dev Agent 오류] GPT 생성 실패: {str(e)}"
