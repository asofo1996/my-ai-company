from utils.gpt import call_gpt

def handle_video_task(prompt):
    full_prompt = (
        "당신은 유튜브 영상 스크립트를 기획하는 전문가입니다.\n"
        "다음 주제에 맞는 흥미로운 영상 구성안을 작성해 주세요:\n\n"
        f"{prompt}"
    )
    return call_gpt(full_prompt)
