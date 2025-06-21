# ✅ instruction_router.py (지시 분기 및 역할 분담자에게 전달하는 핵심 로직)

from agents import pm_agent, dev_agent, design_agent, test_agent, report_agent

# ⛳ 입력값: 사용자가 입력한 목표 또는 auto_runner에서 전달받은 지시문
# ✅ 출력값: 각 Agent의 작업 결과를 통합한 최종 보고서 반환

def route_instruction(goal: str) -> str:
    print("\n📌 [지시 수신] 목표:", goal)

    # 1️⃣ PM Agent가 전체 계획 수립
    task_plan = pm_agent.plan(goal)
    print("\n📋 [PM 계획 수립 완료] 분배된 작업:")
    for role, task in task_plan.items():
        print(f"  └─ {role}: {task}")

    # 2️⃣ 개발자 역할 수행
    dev_result = dev_agent.execute(task_plan)
    print("\n💻 [Dev Agent 완료]", dev_result)

    # 3️⃣ 디자이너 역할 수행
    design_result = design_agent.execute(task_plan)
    print("\n🎨 [Design Agent 완료]", design_result)

    # 4️⃣ QA/Test 역할 수행
    test_result = test_agent.review(dev_result)
    print("\n🧪 [Test Agent 결과]", test_result)

    # 5️⃣ 보고서 요약
    report = report_agent.generate([
        dev_result,
        design_result,
        test_result
    ])
    print("\n📝 [Report Agent 보고서 생성 완료]")

    return report


# 🧪 테스트용 직접 실행
if __name__ == "__main__":
    test_goal = "병원 광고용 유튜브 쇼츠 자동 생성 시스템 구축"
    final_report = route_instruction(test_goal)
    print("\n📤 [최종 보고서 출력]\n", final_report)
