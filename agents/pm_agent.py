# ✅ pm_agent.py (GPT 기반 프로젝트 매니저 역할 수행)

from typing import Dict

def plan(goal: str) -> Dict[str, str]:
    """
    주어진 목표(goal)를 바탕으로 프로젝트 전체 계획 수립
    개발, 디자인, 보고 등 역할별 하위 작업으로 나누어 각 Agent에 전달할 태스크 반환
    """
    print(f"\n📋 [PM Agent] 목표 분석 중: '{goal}'")

    # 기본 분석 (향후 Langchain/GPT API로 연결 가능)
    code_task = f"'{goal}'를 위한 백엔드/프론트엔드 코드 생성"
    design_task = f"'{goal}'에 사용할 이미지, UI, 슬라이드, 영상 생성"
    report_task = f"'{goal}' 관련 작업물 보고서 생성"

    task_plan = {
        "dev_task": code_task,
        "design_task": design_task,
        "report_task": report_task
    }

    print("✅ [PM Agent] 작업 분배 계획 수립 완료")
    return task_plan
