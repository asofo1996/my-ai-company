# ✅ test_agent.py (GPT 기반 QA 및 검토 담당 역할)

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def review(output: str) -> str:
    """
    개발 결과물(output)을 받아 GPT에게 검토 요청 → 개선점, 오류 가능성, 보완 방향 등 제시
    """
    print("\n🧪 [Test Agent] 검토 대상 수신:")
    print(output[:500], "...\n")  # 너무 길 경우 일부만 출력

    if not output:
        return "❌ 검토할 결과물이 없습니다."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 뛰어난 품질관리자(QA)입니다. 코드, 문서, 디자인 등 생성된 결과물을 검토하고 개선점을 제안하세요."},
                {"role": "user", "content": f"다음 내용을 검토하고, 문제점과 개선사항을 알려줘:\n\n{output}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        review_result = response.choices[0].message.content
        print("✅ [Test Agent] GPT 검토 결과 생성 완료")
        return review_result

    except Exception as e:
        print("❌ [Test Agent 오류] GPT 요청 실패:", e)
        return f"[Test Agent 오류] GPT 생성 실패: {str(e)}"
