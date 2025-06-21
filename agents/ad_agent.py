from utils.gpt import call_gpt

def handle_ad_task(prompt):
    full_prompt = (
        "당신은 세계 최고의 마케팅 전문가입니다.\n"
        "다음 요청에 맞춰 설득력 있는 광고 문구를 만들어 주세요:\n\n"
        f"{prompt}"
    )
    return call_gpt(full_prompt)
