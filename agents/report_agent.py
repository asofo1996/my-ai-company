# ✅ report_agent.py (GPT 기반 보고서 요약 및 생성 역할)

import openai
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate(results: List[str]) -> str:
    """
    Dev/Design/Test 등의 결과 리스트를 받아 GPT로 요약 보고서 생성
    """
    print("\n📝 [Report Agent] 작업 결과들을 통합 중...")

    combined_results = "\n\n".join([f"[{i+1}] {r}" for i, r in enumerate(results)])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 뛰어난 전략 기획자이며, 복잡한 작업 결과들을 요약하여 보고서를 작성합니다."},
                {"role": "user", "content": f"다음 결과들을 통합 분석해서 요약 보고서를 작성해줘:\n\n{combined_results}"}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        report = response.choices[0].message.content
        print("✅ [Report Agent] 보고서 생성 완료")
        return report

    except Exception as e:
        print("❌ [Report Agent 오류] GPT 요청 실패:", e)
        return f"[Report Agent 오류] GPT 생성 실패: {str(e)}"
