from agents.ad_agent import handle_ad_task
from agents.video_agent import handle_video_task
from agents.report_agent import handle_report_task
from agents.dev_agent import handle_dev_task
from utils.gpt import call_gpt

def run_crew_task(category, prompt):
    """
    분류된 카테고리에 따라 해당 에이전트를 실행하여 결과 반환
    """
    if category == "광고":
        return handle_ad_task(prompt)
    elif category == "영상":
        return handle_video_task(prompt)
    elif category == "리포트":
        return handle_report_task(prompt)
    elif category == "개발":
        return handle_dev_task(prompt)
    else:
        return f"🧠 [기타] 직접 응답 생성:\n\n{call_gpt(prompt)}"
