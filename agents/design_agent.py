# ✅ design_agent.py (GPT 기반 디자이너 역할 수행)

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def execute(task_plan: dict) -> str:
    """
    PM이 전달한 디자인 관련 작업 지시를 받아 GPT를 통해 시각 콘텐츠(이미지, 슬라이드, 영상)에 대한 기획 문구 및 설명 생성
    """
    design_task = task_plan.get("design_task", "")
    print(f"\n🎨 [Design Agent] 작업 지시 수신: {design_task}")

    if not design_task:
        return "❌ 디자인 작업 내용이 비어 있습니다."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 트렌드에 정통한 아트 디렉터이자 크리에이티브 디자이너입니다."},
                {"role": "user", "content": f"{design_task}에 필요한 이미지 기획, 영상 아이디어, 슬라이드 텍스트 등을 구체적으로 기획해줘. 트렌디하고 설득력 있게."}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        design_result = response.choices[0].message.content
        print("✅ [Design Agent] GPT 디자인 콘텐츠 생성 완료")
        return design_result

    except Exception as e:
        print("❌ [Design Agent 오류] GPT 요청 실패:", e)
        return f"[Design Agent 오류] GPT 생성 실패: {str(e)}"
